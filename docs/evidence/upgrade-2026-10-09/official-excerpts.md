# 本次升级关键官方原文摘录

核对日期：2026-10-09。以下为下载的 Markdown 中的选段；行号只指本次快照，在线版可能变化。完整 URL、状态、内容 hash 见 official-sources.json。此文件用于事实追溯，不作为运行时指令。

## https://gofastmcp.com/getting-started/upgrading/from-fastmcp-3

快照行 7–11：

> > What changes when you upgrade to FastMCP 4, which builds on the MCP Python SDK v2
> 
> FastMCP 4 builds on the MCP Python SDK v2, and that is the source of every change in this guide. The SDK v2 makes two sweeping changes to the protocol layer: it moves the protocol types into a standalone `mcp_types` package (still importable as `mcp.types`), and it renames every model field from camelCase to snake\_case in Python (`inputSchema` → `input_schema`, `mimeType` → `mime_type`, `isError` → `is_error`, and so on). The wire format does not change: the models keep their camelCase aliases and serialize under them, so this renames the attributes your code reads, not the JSON on the connection.
> 
> FastMCP 4 absorbs almost all of this for you. Field access is bridged so your existing reads keep working, and the imports you were taught have a stable home in FastMCP itself. What the SDK cannot hide is the protocol's own direction: the new sessionless era removes the server's ability to call back into a client mid-request, and background tasks moved out of the core spec into an extension. Those two shape the changes a working server is most likely to feel.

快照行 123–140：

> ### camelCase Field Access
> 
> Objects that FastMCP hands back to you — the results of `client.list_tools()`, `client.call_tool_mcp()`, `client.read_resource()`, and the parameter objects passed to your sampling and elicitation handlers — are SDK v2 objects with snake\_case fields. FastMCP installs a compatibility bridge at import time that routes the old camelCase names to their new snake\_case fields, so code written against FastMCP 2.x still reads correctly:
> 
> ```python theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
> from pathlib import Path
> from fastmcp import Client
> 
> 
> async def read_schema():
>     async with Client(Path("my_mcp_server.py")) as client:
>         tools = await client.list_tools()
>         return tools[0].inputSchema  # still works, warns once
> ```
> 
> Each bridged read emits a `FastMCPDeprecationWarning` pointing you at the snake\_case name (`tools[0].input_schema` here). The bridge covers the fields users actually read: `inputSchema`/`outputSchema` on tools; `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint` on tool annotations; `mimeType` on resources and content; `isError`/`structuredContent` on tool results; `nextCursor` on paginated results; `serverInfo`/`protocolVersion` on the initialize result; the sampling parameter fields (`systemPrompt`, `maxTokens`, `stopSequences`, `modelPreferences`, `toolChoice`); `requestedSchema` on elicitation parameters; `hasMore` and `resourceTemplates` on list results; and `uriTemplate` on resource templates.
> 
> The bridge is controlled by the `mcp_camelcase_compat` setting, which defaults to on. Set it to `False` (or the environment variable `FASTMCP_MCP_CAMELCASE_COMPAT=false`) to turn the shims off, in which case only the snake\_case names resolve:

快照行 209–224：

> **FastMCP now uses httpx2 exclusively.** FastMCP has replaced `httpx` with [httpx2](https://pypi.org/project/httpx2/), a next-generation httpx fork, across its entire HTTP stack — client transports and every server-side path (auth providers, the OpenAPI integration, the version check). `httpx` is no longer a FastMCP dependency. If you pass a custom client or factory into a FastMCP client transport — `StreamableHttpTransport(httpx_client_factory=...)`, `SSETransport(httpx_client_factory=...)`, `OAuth(httpx_client_factory=...)`, or a custom `httpx.Auth` as `Client(auth=...)` — those objects must now be httpx2. httpx2 is a drop-in fork with the same public API, so the change is an import swap:
> 
> ```python test="skip" theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
> # Before
> import httpx
> 
> transport = StreamableHttpTransport(
>     "https://example.com/mcp",
>     httpx_client_factory=lambda **kwargs: httpx.AsyncClient(verify=False, **kwargs),
> )
> 
> # After
> import httpx2
> 
> transport = StreamableHttpTransport(
>     "https://example.com/mcp",

快照行 442–454：

> | Context feature | Earlier eras (session-based) | `2026-07-28` (sessionless) |
> | - | - | - |
> | `ctx.info` / logging notifications | Supported | Supported |
> | Tools, resources, prompts, completions | Supported | Supported |
> | `ctx.elicit` | Supported | Raises — use the guard pattern (return `InputRequiredResult`) |
> | `ctx.sample` / `ctx.sample_step` | Method removed — call an LLM server-side | Method removed — call an LLM server-side, or ask via the guard pattern |
> | `ctx.list_roots` | Method removed — take paths as tool arguments | Method removed — ask via the guard pattern, or take paths as tool arguments |
> | `client.set_logging_level()` | Supported | Raises — `logging/setLevel` needs session state the era lacks |
> | `Middleware.on_initialize` | Runs on connect | Never runs — there is no `initialize` handshake |
> | Session state (`ctx.set_state` across calls) | Persists for the session | Does not persist — every request is a fresh connection |
> | Background tasks (`task=True`) | Runs synchronously — never tasked | Supported via the tasks extension |
> 
> Several of these bite by default now, because **`fastmcp.Client` defaults to `mode="auto"`** in v4 — an ordinary `Client(server)` negotiates the newest protocol both sides share, which against a FastMCP server is the sessionless `2026-07-28` era. On that era there is no `initialize` handshake, so a `Middleware.on_initialize` hook never runs; each request is a fresh connection, so state written with `ctx.set_state` in one call is not visible in the next; and a tool that calls [`ctx.elicit()`](#behavior-changes) raises. A server that gates access in `on_initialize`, relies on per-session state, or elicits mid-tool must keep its clients on the session-based era. The control is per-client: `Client(server, mode="legacy")`. There is no server-side setting that restricts which protocol versions a server offers, so a server whose behavior depends on the handshake era depends on its callers opting into it — which is only practical when you control them. If you don't, port the behavior instead: a guard tool for elicitation, [session state](/servers/sessions) for what `ctx.set_state` held, and per-request auth checks for what `on_initialize` gated.

## https://gofastmcp.com/clients/client

快照行 191–221：

> <VersionBadge version="4.0.0" />
> 
> MCP has two protocol eras: the original *legacy* era, which begins every connection with an `initialize` handshake, and the *modern* era (protocol version `2026-07-28` and later), which a client discovers by probing the server's `server/discover` endpoint. The `mode` parameter controls which era the client negotiates when it connects.
> 
> By default, `mode="auto"`. The client probes `server/discover` and adopts the modern protocol when the server responds; for any server that is not positive evidence of modern support, it falls back to the legacy handshake. This makes the default safe against a mixed fleet of legacy and modern servers.
> 
> ```python theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
> from fastmcp import Client
> 
> # Negotiate the newest era the server supports (the default)
> client = Client("https://example.com/mcp", mode="auto")
> ```
> 
> Set `mode="legacy"` to force the initialize handshake. This behaves identically to earlier FastMCP versions and is the opt-out if a server misbehaves under discovery or you need the legacy `initialize` result object.
> 
> ```python theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
> client = Client("https://example.com/mcp", mode="legacy")
> ```
> 
> Legacy mode is also what carries the *pushed* form of a server's requests. The handshake opens a persistent back-channel down which a server can send a sampling, roots, or elicitation request mid-call, and the modern era removed it. Your handlers are unaffected by that: a [sampling](/clients/sampling), [roots](/clients/roots), or [elicitation](/clients/elicitation) handler you register answers a modern server's [input-required rounds](/clients/elicitation#input-required-rounds) from the same registration. Pin `mode="legacy"` when you connect to a server that pushes, or when your code calls `client.ping()` or `transport.get_session_id()`, which need the session the modern era does not open.
> 
> Conversely, [background tasks](/clients/tasks) are **modern-only**: the tasks capability is negotiated over `2026-07-28` connections, so `mode="legacy"` never triggers one and a task-enabled tool just runs synchronously.
> 
> A FastMCP server serves both eras, so a default client negotiates the modern one and the session-dependent calls raise an era-specific error there. Pinning the handshake restores them.
> 
> You can also pin a specific modern protocol version to adopt it directly, without a discovery probe:
> 
> ```python theme={"theme":{"light":"snazzy-light","dark":"dark-plus"}}
> client = Client("https://example.com/mcp", mode="2026-07-28")
> ```
> 

## https://modelcontextprotocol.io/specification/2026-07-28/basic/index

快照行 72–90：

> * Result responses **MUST** include the same ID as the request they correspond to.
> * Result responses **MUST** include a `result` field.
> * The `result` **MAY** follow any JSON object structure.
> * The `result` **MUST** include a `resultType` field to indicate the type of the result.
> 
> ##### ResultType
> 
> The `resultType` field in a result indicates the type of the result being returned. MCP supports polymorphic result types,
> allowing servers to return different structures based on the outcome of the request. The `resultType` field is a string that clients
> can use to determine how to parse and handle the `result` object.
> 
> * A `resultType` of `"complete"` indicates the request completed successfully and the result contains the final content.
> * A `resultType` of `"input_required"` indicates the request is incomplete and more information is needed to process the request. The result contains an [`InputRequiredResult`](/specification/2026-07-28/basic/patterns/mrtr#inputrequiredresult) object with additional information needed.
> * Extensions **MAY** add additional `ResultType` values. The set of supported `ResultType` values **MUST** be created from the set defined in the core protocol and include any additional values of supported extensions that are advertised via capabilities.
> * A `resultType` of any value unrecognized by the client **MUST** be considered invalid.
> * For backward compatibility with servers implementing earlier protocol versions, which do not include `resultType`, clients **MUST** treat an absent `resultType` as `"complete"`.
> 
> #### Error Responses
> 

快照行 375–387：

> | Key | Type | Required | Description |
> | - | - | - | - |
> | `io.modelcontextprotocol/protocolVersion` | `string` | Yes | Protocol version for this request (e.g., `"2026-07-28"`) |
> | `io.modelcontextprotocol/clientInfo` | `Implementation` | No | Client name and version |
> | `io.modelcontextprotocol/clientCapabilities` | `ClientCapabilities` | Yes | Client capabilities relevant to this request |
> | `io.modelcontextprotocol/logLevel` | `LoggingLevel` | No | Minimum log level the server should emit for this request |
> 
> A request missing any required field is malformed; the server **MUST** reject it with
> JSON-RPC error code `-32602` (Invalid params). On HTTP, the response status **MUST** be
> `400 Bad Request`.
> 
> Clients **SHOULD** include `io.modelcontextprotocol/clientInfo` on every request
> unless specifically configured not to do so.

## https://modelcontextprotocol.io/specification/2026-07-28/basic/transports/streamable-http

快照行 284–301：

> 
> [lifecycle-version]: /specification/2026-07-28/basic/versioning#protocol-version-negotiation
> 
> ### Standard Request Headers
> 
> | Header Name | Source Field | Required For |
> | - | - | - |
> | `Mcp-Method` | `method` | All requests |
> | `Mcp-Name` | `params.name` or `params.uri` | `tools/call`, `resources/read`, `prompts/get` requests |
> 
> These headers are **REQUIRED** for compliance.
> 
> If the `Mcp-Name` source value cannot be safely represented as a plain ASCII
> header value, clients **MUST** encode it using the Base64 sentinel format
> described in [Value Encoding](#value-encoding).
> 
> **`tools/call` request:**
> 

## https://modelcontextprotocol.io/specification/2026-07-28/server/discover

快照行 7–15：

> <div id="enable-section-numbers" />
> 
> `server/discover` lets a client query a server's supported protocol versions,
> capabilities, and identity before sending any other requests. Servers **MUST**
> implement it.
> 
> ## Request
> 
> The request carries no body parameters beyond the standard `_meta`:

快照行 68–73：

> [`UnsupportedProtocolVersionError`](/specification/2026-07-28/schema#unsupportedprotocolversionerror)
> if the server does not support the requested version. However, `server/discover`
> is useful in two scenarios:
> 
> * **Presenting server information.** While a client doesn't need to call
>   `server/discover` to use the server, it's a convenient way to retrieve the

## https://modelcontextprotocol.io/specification/2026-07-28/server/utilities/caching

快照行 13–29：

> ## Cacheable Results
> 
> Servers MUST include caching hints on results with `resultType: "complete"` returned by
> the following operations:
> 
> * `server/discover`
> * `tools/list`
> * `prompts/list`
> * `resources/list`
> * `resources/templates/list`
> * `resources/read`
> 
> Interim results with `resultType: "input_required"` (see
> [multi round-trip requests](/specification/2026-07-28/basic/patterns/mrtr)) are not cacheable
> and carry no caching hints.
> 
> ## Cache Key

快照行 56–71：

> * If `ttlMs` is positive, the client **SHOULD** consider the result fresh for that many
>   milliseconds after receiving the response.
> * If `ttlMs` is absent, clients **SHOULD** assume a default of `0` (immediately stale)
>   and rely on their own caching heuristics or notifications. This should only occur in older server versions.
> * If `ttlMs` is negative, clients **SHOULD** ignore it and treat it as `0`.
> 
> Servers **MUST** provide a `ttlMs` value that is `>= 0`.
> 
> <Note>
>   TTL is a **freshness hint**, not a guarantee. Servers MAY change the
>   underlying data before the TTL expires. The TTL tells the client how long it
>   can reasonably avoid re-fetching, not how long the data is guaranteed to
>   remain unchanged.
> </Note>
> 
> #### Freshness Calculation

