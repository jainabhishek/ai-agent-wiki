# Making private MCP servers reachable without making them public — OpenAI (raw capture)

> Source: https://developers.openai.com/blog/connect-private-mcp-servers-to-openai-products
> Publisher: OpenAI (Developers blog) · Date: 2026-06-26
> Captured: 2026-10-12 via the OpenAI blog full-text export plus curl of the page for byline (condensed).

Author: Denys Kurylenko. Category tag: General. Subtitle: preserving private
network boundaries while supporting MCP streaming, authentication, and an
inspectable client.

## Introduction

OpenAI built **Secure MCP Tunnel** because the most valuable MCP servers
(inside enterprise networks, private service meshes, developer laptops) are
the ones teams least want on the public internet. Connecting them to hosted
AI products used to require public endpoints, extra proxy infrastructure, or
new network operators in sensitive paths. Mechanism: a small customer-run
client inside the private environment opens an outbound HTTPS connection to
OpenAI, then (1) receives MCP requests, (2) forwards them to an approved local
server, (3) returns responses and notifications over the same connection.
ChatGPT, Codex, and other OpenAI products use the standard MCP request model.
Design principles: outbound-only connectivity; explicit destination
configuration; compatibility with MCP streaming and notifications; a
customer-run, inspectable client.

## The wrong defaults

Three common ways to reach a private service, each criticized:
- a public endpoint — easy access by weakening the boundary;
- a third-party tunnel provider — adds a vendor to security review,
  procurement, runbooks, and the metadata surface;
- VPN or network peering — broad connectivity, too much machinery for a narrow
  MCP integration.
Secure MCP Tunnel "turns reachability inside out": products send MCP requests
to an OpenAI-hosted tunnel endpoint; the tunnel service queues work per
tunnel; the customer-run client next to the server picks it up over outbound
HTTPS, forwards locally, and returns the response the same way (Figure 1:
request lifecycle).

## Why start with long-poll?

Transport chosen to be operationally boring: outbound HTTPS is familiar to
firewalls, proxies, and platform teams. Long-polling lets the client ask only
for as much work as it can process, giving natural backpressure instead of
unbounded buffering. Shipped flow: (1) a product sends MCP JSON-RPC to the
OpenAI-hosted endpoint; (2) the tunnel service holds or streams the request
until the client returns a final response; (3) for streamed results, the
tunnel forwards intermediate server-sent events. Requests, responses, and
events are relayed through the hosted endpoint; the server and its address
stay private.

## Keeping the security boundary explicit

The tunnel makes the boundary explicit rather than erasing it. The client
authenticates to the tunnel control plane; products use the hosted endpoint;
the private MCP address is used only inside the customer environment. Access
is tied to the customer's existing OpenAI organization and workspace context
plus a configured tunnel identity, not a separate access model. The client
must be inspectable and narrow: customers should know what code runs, what
outbound path it opens, and which private services it may reach (Figure 2).

## Making MCP development feel local

Goal: a developer tool, not a network project. Run an MCP server on a laptop,
start the tunnel client beside it, connect to ChatGPT or Codex — no public
endpoint, VPN, firewall rule, or peering change. The same model carries to
Kubernetes, a VM, or other customer-controlled environments: run the client
near the server, validate reachability, let the client initiate the
OpenAI-facing path. Health checks, readiness, logs, and a local admin UI make
the loop inspectable. The tunnel client ships a Codex plugin (`tunnel-mcp`)
that turns setup into a guided workflow and produces the same configuration
shape used in production. A packaged assistant workflow can read local tunnel
context (active profile, generated config, local server reachability, startup
stage), so troubleshooting reasons from the real setup rather than generic
instructions (Figure 3: laptop to production).

## Why an open-source tunnel client matters

The client (`openai/tunnel-client` on GitHub) is open-source, customer-run,
and sits inside the customer boundary. Reviewers can inspect what it does,
what outbound connection it opens, how it forwards requests locally, and what
configuration bounds its reach. OpenAI hosts the tunnel service; the code
inside the customer environment is small, reviewable, and customer-controlled.

## Enterprise auth without broad network access

Private MCP servers may need OAuth, private certificate authorities, outbound
proxies, or client certificates. OAuth discovery for the MCP server travels
through the tunnel, so the hosted product learns how to authenticate without
the server listening publicly. Client-side config supports custom CA bundles,
proxy settings, and MCP-side mTLS. The boundary stays explicit: the tunnel
does not make related enterprise endpoints reachable; a private authorization
server must still be reachable by whichever component performs the OAuth
flow. Secure MCP Tunnel is a narrow path to configured tools, not a
general-purpose network bridge.

## Beyond MCP

Alpha customers also had private REST APIs not packaged as MCP servers.
**Harpoon** extends the model to approved REST targets: the customer registers
labeled targets on the tunnel client; OpenAI-side callers invoke labels
through the tunnel; the HTTP request originates inside the customer
environment. Calls are bounded by customer-owned target registration, allowed
methods, response-size limits, timeouts, redirect behavior, and tunnel access
controls — no inbound access and no VPN-like identity for OpenAI.

## Resources

tunnel-client on GitHub; the Secure MCP Tunnel guide in the OpenAI API docs.
