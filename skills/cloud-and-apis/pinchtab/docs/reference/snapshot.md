# Snapshot

Get an accessibility snapshot of the current page, including element refs that can be reused by action commands.

Iframe content is detected automatically during snapshot capture. Same-origin iframe descendants are included beneath the iframe owner element, and their refs can be reused directly with action commands. Cross-origin iframes currently remain as owner nodes only.

Selector scoping is explicit. `selector=...` only searches the current frame scope, which defaults to `main`. To scope selector-based snapshots into an iframe, set the frame first with [`/frame`](./frame.md) or `pinchtab frame`.

```bash
curl "http://localhost:9867/snapshot?filter=interactive"
# CLI Alternative (defaults to compact text output)
pinchtab snap -i
# Output
[e5] link "More information..."

# Use --full or --compact=false for JSON
pinchtab snap --full
```

## CLI Flags

| Flag | Description |
|------|-------------|
| `-i`, `--interactive` | Filter to interactive elements + headings (default: true) |
| `-c`, `--compact` | Compact text output (default: true) |
| `-d`, `--diff` | Show diff from previous snapshot |
| `--full` | Full JSON output (shorthand for `--interactive=false --compact=false`) |
| `--text` | Text output format |
| `-s`, `--selector` | CSS selector to scope snapshot |
| `--max-tokens` | Maximum token budget |
| `--depth` | Tree depth limit |
| `--tab` | Target specific tab |

## Examples

```bash
pinchtab snap                           # Interactive compact (default)
pinchtab snap -i -c                     # Same as above
pinchtab snap --full                    # Full JSON with all nodes
pinchtab snap -d                        # Show changes since last snapshot
pinchtab snap --selector "#main"        # Scope to element
pinchtab snap --max-tokens 2000         # Limit output size
```

## API Parameters

| Parameter | Description |
|-----------|-------------|
| `filter` | `interactive` for interactive + headings, `all` (default) for the whole tree |
| `interactive` | Boolean alias for `filter`: `true` is `filter=interactive`, `false` is `filter=all`. Contradicting an explicit `filter` is a 400 |
| `format` | `compact`, `text`, `yaml`, or default JSON. The CLI and the MCP tool both ask for `compact`; the HTTP default is unchanged |
| `diff` | `true` for diff mode |
| `selector` | CSS selector to scope |
| `maxTokens` | Token budget limit |
| `depth` | Tree depth limit |

## What a format costs, and what it carries

The same 40 realistic interactive nodes, rendered through each output path:

```
  compact     1644 bytes  ~ 411 tokens   1.0x
  text        2060 bytes  ~ 515 tokens   1.3x
  json        8211 bytes  ~2052 tokens   5.0x
  yaml       17467 bytes  ~4366 tokens  10.6x
```

55% of that JSON body is the DOM-derived descriptor fields — `tag`, `label`, `placeholder`,
`alt`, `title`, `testid`, `text` — which exist to feed the server-side semantic matcher.
`compact` and `text` render `ref`, `role`, `name`, `value` and the state flags and nothing
else, so those fields cannot appear there at all. The DOM pass that fills them is therefore
skipped for `compact` and `text`, which also drops one CDP round trip per node from the
cheapest path.

Skipping it changes nothing the caller can see: the fields are absent from those formats
either way, and `find` and the semantic selectors enrich the cached nodes themselves before
matching, so a `compact` snapshot leaves them exactly as capable as a JSON one.

## What `maxTokens` guarantees

`maxTokens` is a ceiling, not a hint. The nodes returned are the longest prefix whose
rendered output fits the budget in the format you asked for, so the response never exceeds
what you asked for and stops one node short of it at worst. Measured across `compact`,
`text`, `json` and `yaml` on a page of realistic interactive nodes, a budget that actually
constrains the result delivers 87–100% of it.

The cost is measured, not modelled: each node is charged the bytes its own format emits —
rendered for `compact` and `text`, marshalled for `json` and `yaml` — so a change to a
formatter changes the budget with it. Tokens are estimated at four bytes each.

Formats are not interchangeable for a given budget. `yaml` is roughly three times the size
of `json` for the same nodes, because the node struct carries JSON field tags and no YAML
ones, so YAML emits every field including the empty ones. The same `maxTokens` therefore
returns far fewer nodes in `yaml` than in `json` — which is the budget working, not a
regression. Prefer `compact` when the budget is tight: it fits several times more nodes
into the same tokens than either structured format.

## Control state on a node

A snapshot reports the state of a control, not just its identity, so an agent can
verify its own action and read a page it did not set up:

- `value` — the current text of an input or the selection of a `select`
- `focused`, `disabled`, `hidden` — booleans, present only when true
- `checked` — `"true"`, `"false"` or `"mixed"` for a checkbox, radio,
  `menuitemcheckbox`, `menuitemradio`, or any element carrying `aria-checked`

`checked` is a three-value string rather than a boolean because `"mixed"` is a real
state: both a native indeterminate checkbox and `aria-checked="mixed"` report it.

**An absent `checked` means the node has no checkedness — never that it is off.**
Ordinary nodes do not carry the key at all, so a missing value must not be read as
unchecked. A control that is off says so explicitly with `"false"`.

The rendered formats carry all three states, so an unchecked option never looks
like a node the field does not apply to:

| State | `format=text` | `format=compact` |
|-------|---------------|------------------|
| checked | `[checked]` | `[x]` |
| unchecked | `[unchecked]` | `[ ]` |
| mixed | `[mixed]` | `[/]` |

A radio group is therefore readable from a single snapshot:

```
e4 radio "Standard shipping" [checked]
e5 radio "Express shipping" [unchecked]
e6 radio "Pickup" [unchecked]
```

Diff mode treats a change of `checked` as a change, so `pinchtab snap -d` after a
`check` shows the node as `[~]`.

## Related Pages

- [Click](./click.md)
- [Frame](./frame.md)
- [Tabs](./tabs.md)
