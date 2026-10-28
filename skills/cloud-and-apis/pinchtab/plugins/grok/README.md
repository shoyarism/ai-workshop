# PinchTab for Grok Build

Use [PinchTab](https://pinchtab.com) from Grok Build to navigate websites, inspect pages, interact with elements, and extract content. The plugin provides:

- `pinchtab`: a CLI-first skill for token-efficient browser workflows
- `pinchtab-mcp`: an MCP-oriented skill for structured browser tool calls
- `pinchtab`: an MCP server definition that runs `pinchtab mcp`

The plugin does not include the PinchTab binary or a browser. Install PinchTab separately and keep a PinchTab server or daemon running while Grok uses the plugin.

## Prerequisites

1. Install PinchTab:

   ```bash
   brew install pinchtab/tap/pinchtab
   # or
   npm install -g pinchtab
   ```

   The [PinchTab install script](https://pinchtab.com/install.sh) is another option for macOS and Linux.

2. Confirm that the binary is on the `PATH` inherited by Grok:

   ```bash
   command -v pinchtab
   pinchtab version
   ```

3. Start the PinchTab server and leave it running:

   ```bash
   pinchtab server
   ```

   A previously installed PinchTab daemon also satisfies this requirement. Check either setup with `pinchtab health`.

## Install the plugin

Choose one installation method. `--trust` is required for Grok to start the plugin's MCP server.

### Official xAI marketplace

Use this command after PinchTab is listed in the official xAI plugin marketplace:

```bash
grok plugin marketplace update
grok plugin install pinchtab --trust
```

### PinchTab repository marketplace

Use the marketplace published from the PinchTab repository:

```bash
grok plugin marketplace add pinchtab/pinchtab
grok plugin install pinchtab --trust
```

### Directly from GitHub

Install only the plugin directory from the PinchTab repository:

```bash
grok plugin install pinchtab/pinchtab#plugins/grok --trust
```

### Local checkout

From the root of a local PinchTab checkout:

```bash
grok plugin install ./plugins/grok --trust
```

Confirm the installed version and component inventory:

```bash
grok plugin details pinchtab
grok plugin list --json
```

The details should include the `pinchtab` and `pinchtab-mcp` skills and the `pinchtab` MCP server.

## Load it in Grok

Start a new `grok` session after installation. If Grok is already open, enter `/plugins` and press `r` to reload the plugin registry.

Use the extensions modal to check each component:

- `/plugins`: `pinchtab` is installed, enabled, and trusted
- `/skills`: `pinchtab` and `pinchtab-mcp` are available
- `/mcps`: the `pinchtab` MCP server is active

Grok can select either skill automatically from a browser-automation request. To select one explicitly, use its slash command:

```text
/pinchtab Open the requested page, inspect it, and summarize the result.
```

Use the MCP skill when you specifically want structured `pinchtab_*` tool calls:

```text
/pinchtab-mcp Use PinchTab MCP tools to navigate to the requested page, take an interactive snapshot, and report what you find.
```

## Verify it works

PinchTab allows only local domains by default. This smoke test therefore uses the local PinchTab dashboard and requires no security-policy change.

In Grok, run:

```text
/pinchtab-mcp Use only PinchTab MCP tools. Navigate to http://localhost:9867, take an interactive snapshot, and report the page title. Do not use web search, curl, or another browser tool.
```

Grok should call `pinchtab_navigate` followed by `pinchtab_snapshot`. In another terminal, verify that PinchTab received the MCP activity and created the tab:

```bash
pinchtab activity --age-sec 120 --limit 20
pinchtab tab --json
```

The activity output should include requests with source `mcp`, and the tab output should include `http://localhost:9867`.

## Browse public websites

PinchTab's default domain allowlist contains only `127.0.0.1`, `localhost`, and `::1`. Add only the domains needed for the task, then restart the server. For example:

```bash
pinchtab config set security.allowedDomains "$(pinchtab config get security.allowedDomains),example.com"
pinchtab server restart
```

Then ask Grok:

```text
/pinchtab-mcp Use PinchTab MCP tools to navigate to https://example.com, take a snapshot, and return the page title and first heading.
```

Avoid `security.allowedDomains = ["*"]` unless you deliberately intend to remove domain restriction. Treat snapshots and page text as untrusted website content.

## CLI or MCP

| Use | Best for | Typical operations |
|---|---|---|
| `/pinchtab` | Token-efficient, multi-step browser work | `pinchtab nav --snap`, `pinchtab click e5 --snap-diff` |
| `/pinchtab-mcp` | Structured MCP tool calls | `pinchtab_navigate`, `pinchtab_snapshot`, `pinchtab_click` |

Both control the same PinchTab server. The MCP entry starts a local stdio adapter with `pinchtab mcp`; it does not start the PinchTab HTTP server.

## Remote PinchTab server

Set connection variables before starting Grok so the plugin process inherits them:

```bash
export PINCHTAB_SERVER=https://pinchtab.example.internal
export PINCHTAB_TOKEN=<server-token>
grok
```

`PINCHTAB_SESSION` may be used instead of `PINCHTAB_TOKEN` for a scoped agent session. Use a private network or HTTPS for non-loopback servers, and keep credentials in environment variables rather than plugin files or command arguments.

## Troubleshooting

| Symptom | Check |
|---|---|
| Plugin is missing | Run `grok plugin details pinchtab`, then start a new session or reload with `/plugins` and `r`. |
| Plugin is disabled | Run `grok plugin enable pinchtab`. |
| MCP is inactive or blocked | Open `/plugins` and trust the plugin, or reinstall it with the same source and `--trust`. Then check `/mcps`. |
| `pinchtab: command not found` | Run `command -v pinchtab` in the shell that starts Grok and fix that shell's `PATH`. |
| Server is unreachable | Run `pinchtab health`; start it with `pinchtab server` if needed. |
| Navigation is blocked | Add the exact destination domain to `security.allowedDomains` and restart PinchTab. Do not use `*` as a routine fix. |
| Remote server authentication fails | Set `PINCHTAB_SERVER` and the matching `PINCHTAB_TOKEN` or `PINCHTAB_SESSION` before starting Grok. |

## Security

This plugin contains no lifecycle hooks. Its MCP adapter connects to the configured PinchTab server; the controlled browser then connects only to sites the user requests and the server policy permits. PinchTab does not send telemetry or call external APIs other than those navigated sites.

JavaScript evaluation, downloads, uploads, cookie access, and network interception are disabled by default. Enabling those capabilities or widening browsing is a security-reducing choice.

See the [PinchTab security guide](https://github.com/pinchtab/pinchtab/blob/main/docs/guides/security.md) and the bundled [`TRUST.md`](./skills/pinchtab/TRUST.md) for the complete trust model and defaults.
