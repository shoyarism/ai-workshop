# Testing

## Quick Start with dev

The `dev` developer toolkit is the easiest way to run checks and tests:

```bash
./dev                    # Interactive picker
./dev test               # All tests (unit + E2E)
./dev test unit          # Unit tests only
./dev e2e                # Extended suite (all extended tests)
./dev e2e basic          # Basic suite (api + cli + infra)
./dev e2e extended       # Extended suite
./dev e2e smoke          # Smoke suite (smoke scenarios + Docker smoke)
./dev e2e smoke-docker   # Host Docker smoke only
./dev e2e api            # API basic tests
./dev e2e cli            # CLI basic tests
./dev e2e infra          # Infra basic tests
./dev e2e api-extended   # API extended, multi-instance
./dev e2e cli-extended   # CLI extended tests
./dev e2e infra-extended # Infra extended, multi-instance
./dev e2e infra-extended --filter auth  # Extended infra suite filtered to "auth"
./dev check              # All checks (format, vet, build, lint)
./dev check go           # Go checks only
./dev check security     # Gosec security scan
./dev format dashboard   # Run Prettier on dashboard sources
./dev doctor             # Setup dev environment
```

E2E summaries and markdown reports prefix each test with its scenario filename, for example `[auth-extended] auth: login sets session cookie`, so it is easy to see which filename filter to use.

## Unit Tests

```bash
go test ./...
# or
./dev test unit
```

Unit tests are standard Go tests that validate individual packages and functions without launching a full server.

## E2E Tests

End-to-end tests launch a real pinchtab server with Chrome and run e2e-level tests against it. Tests are organized into three parallel groups:

- **api** — Browser control and page interaction (tabs, actions, files)
- **cli** — CLI command tests
- **infra** — System, network, security, stealth, orchestration

### E2E Boundary

The Go runner is the execution boundary for E2E. `go run ./tests/tools/runner e2e ...` owns suite expansion, scenario discovery, manifest metadata, compose service selection, readiness waits, container arguments, host Docker smoke checks, logs, reports, failure accounting, and GitHub Actions outputs. Scenario files and helpers own the actual assertions and API or CLI interactions.

`tests/e2e/scenarios/manifest.json` is metadata, not a scenario list. It only overrides tier, helper, required compose services, readiness targets, and tags. Filename suffixes provide the default tier: `*-basic.sh` is `basic`, `*-smoke.sh` is `smoke`, and every other scenario is `extended`.

Tier meanings:
- `basic` is the fast PR happy path
- `extended` is deeper coverage and includes matching `basic` scenarios
- `smoke` is separate high-setup coverage and does not include `basic` or `extended`

Add new scenarios under `tests/e2e/scenarios/<group>/`, choose the tier by filename, add manifest metadata only for non-default service/readiness/helper/tags, and verify selection with `go run ./tests/tools/runner e2e --suite <suite> --filter <name> --dry-run`.

`--filter` is a case-sensitive scenario selector over file name, manifest key, group, tier, helper, and tags. It runs before compose planning, so unmatched suites are skipped and only required services start. `--test` is narrower: it runs one matching `start_test` block inside the already-selected scenarios.

CI uses `.github/workflows/reusable-e2e.yml` and `.github/workflows/reusable-smoke.yml`, both calling the Go runner directly. The workflow layer decides when to run; the Go layer decides what to run and how to report it.

### What a pull request runs

Every pull request runs the three basic suites. Which extended and smoke suites join them comes from `scripts/ci/e2e-escalation.map`, evaluated against the diff by `scripts/ci/detect-e2e-suites.sh` in the `detect-changes` job of `.github/workflows/ci-e2e.yml`. One rule per line maps a path expression to the suites that cover that path; the first rule matching a changed path decides, and a path matching no rule adds nothing.

The map reads product paths as well as test paths:

| Changed path | Suites added |
| --- | --- |
| `tests/e2e/scenarios/<group>/*-basic.sh` | none — the basic suites already run |
| `tests/e2e/scenarios/<group>/*-smoke.sh` | `smoke` |
| any other `*.sh` under `tests/e2e/scenarios/api/`, `cli/` or `infra/` | that group's extended suite |
| `Dockerfile`, `.dockerignore`, `scripts/docker-*smoke.sh`, the smoke Dockerfile and workflows | `smoke` |
| audit implementation — `internal/audit/`, `pkg/pinchtabaudit/`, the audit handlers, `internal/cli/actions/actions_audit*`, `cmd/pinchtab/cmd_audit*` | `api-extended`, `cli-extended` |
| compare implementation — `internal/cli/actions/actions_compare*`, `cmd/pinchtab/cmd_compare*` (`internal/audit/compare.go` is already audit) | `cli-extended` |

Covering a new product area is one line in the map. `go test ./internal/devtools/` drives the script over synthetic file lists, so a mapping is verified by running it rather than by reading the YAML. Extended coverage the map does not claim is not lost — it runs after merge, on the lane below.

Audit and compare are also declared there as *enrolled areas*: every tracked source file matching an area must escalate that area's suites, with a short exclusion list for files that only share the word (`internal/authn/audit.go` is security audit logging). So a new file in an enrolled family cannot quietly miss the map — which is how the CLI audit implementation went unenrolled while its cobra wrapper was covered. Enrolling another area is one entry in `enrolledAreas`.

The multi-page audit runs — `api/audit-extended.sh`, `cli/audit-cli-extended.sh`, `cli/audit-seaportal-extended.sh`, `cli/compare-extended.sh` — sit in the extended tier rather than the basic one, so a pull request pays for them only when it touches audit or compare. The PR path keeps the single-page audit signal: `api/audit-page-basic.sh`, `api/a11y-audit-basic.sh`, `api/audit-fixtures-basic.sh`, `cli/audit-auth-basic.sh` and `cli/audit-report-basic.sh`.

### What a merge and the nightly run

Every push to `main` runs the three extended suites without consulting the map, so coverage a pull request skipped is exercised at merge rather than never. Extended suites include the matching `*-basic.sh` scenarios, so the merge lane does not repeat the basic suites.

Smoke is the expensive lane — it builds images — so it runs nightly on the `schedule` trigger in `.github/workflows/ci-smoke.yml` rather than per merge, on top of the pull requests whose diff the map escalates to `smoke`.

| Lane | Trigger | Suites |
| --- | --- | --- |
| pull request | `pull_request` on `main` | the three basic suites, plus whatever the escalation map claims |
| merge | `push` on `main` | `api-extended`, `cli-extended`, `infra-extended` |
| nightly | `schedule` in `ci-smoke.yml` | `smoke` |
| manual | `workflow_dispatch` | whichever suite is chosen |

`go test ./internal/devtools/` reads both workflows and fails if a suite the map can escalate has no automatic trigger, so a suite cannot quietly fall back to `workflow_dispatch` only. It also fails when a trigger exists but cannot fire — a `schedule` holding no cron, or a `push` whose branch or path filters are narrower than the `pull_request` filters over the same paths the map claims.

### Basic Suites

```bash
./dev e2e basic
./dev e2e api
./dev e2e cli
./dev e2e infra
```

Use these on pull requests and during normal development:

- `basic` runs all three basic suites (same as CI PR workflow)
- `api` runs the API `*-basic.sh` groups on the single-instance stack
- `cli` runs the CLI `*-basic.sh` groups on the single-instance stack
- `infra` runs the Infra `*-basic.sh` groups on the single-instance stack

### Extended Suites

```bash
./dev e2e api-extended
./dev e2e cli-extended
./dev e2e infra-extended
```

Extended suites run both `*-basic.sh` and `*-extended.sh` scenarios plus standalone scripts. `api-extended` and `infra-extended` use the multi-instance stack for orchestration coverage.

### Extended Meta-Suite

```bash
./dev e2e
./dev e2e extended
```

Runs `api-extended`, `cli-extended`, `infra-extended`, and `plugin` in sequence. Extended suites include both `*-basic.sh` and `*-extended.sh` scenarios.

### Smoke Suite

```bash
./dev e2e smoke
./dev e2e smoke-orchestrator
./dev e2e smoke-security
./dev e2e smoke-docker
```

Smoke is its own tier: it runs `*-smoke.sh` scenarios plus host-level Docker smoke checks, and it does not include basic or extended scenarios. Use the filtered smoke suites when you only need one smoke lane.

#### Docker image reuse

The two images the host Docker checks need are tagged by a digest of what they are built
from — the Dockerfile, the platform it is pinned to, and the content of every file in the
build context. So an image whose inputs are unchanged is already on the host under the tag
this run is asking for, and the lane reuses it; an image whose inputs changed answers a
different tag, misses, and is rebuilt. Reuse is therefore never "a tag exists, skip it":
the tag cannot exist unless it was built from exactly these bytes.

The digest is over content, mode and symlink targets — not timestamps — so a checkout or a
`touch` does not force a rebuild, an edit reverted byte-for-byte returns to the original
tag, and a `chmod +x` or a retargeted link does not slip through unnoticed.

`.dockerignore` decides what counts as context, and the digest reads it the way docker
does: patterns match the context-root-relative path, so `node_modules/` excludes the root
one and **not** `npm/node_modules` — each nested tree needs its own line. That is why the
file lists `dashboard/node_modules/`, `npm/node_modules/` and `plugins/openclaw/node_modules/`
separately. Keeping those trees out is worth doing for its own sake: they are not build
inputs for the Go binary, and every file in the context is a file docker hashes for its
own `COPY` layer. `.alp/` is excluded for the same reason — it is rewritten every few
minutes and would otherwise invalidate the image on every write.

The digest deliberately errs towards rebuilding: anything the `.dockerignore` reader
cannot decide exactly stays IN. Hashing a file docker ignores costs one rebuild that the
run announces; missing a file docker sends is a stale image passing a run it should have
failed.

Every run states its decision per image before the checks run, so a stale-image suspicion
is answerable from the log rather than by deleting tags:

```
  image pinchtab-release-smoke:9df635add9f96cea    reusing: build inputs unchanged since this image was built
  image pinchtab-chrome-cft-smoke:c20b4da906e78fdf building: no local image for these build inputs
```

Pass `--rebuild` to build regardless — that is what CI should use when it wants a cold
build. `PINCHTAB_DOCKER_SMOKE_RELEASE_IMAGE` and `PINCHTAB_DOCKER_SMOKE_CHROME_IMAGE`
still override an image outright, and such an image is never built.

**What the lane costs.** Measured locally on an arm host: the host Docker checks are ~5-6s
when both images are reused, against 70-125s when both have to be built — the spread on a
build depends on how much of docker's own layer cache survived the change. A full `./dev
e2e smoke` on reused images is 75-85s wall for 43 tests, the balance being the compose
stack and the smoke scenarios. The Chrome-for-Testing image is pinned `--platform linux/amd64`
and so builds under emulation on arm, which is what made the rebuild worth avoiding.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `CI` | _(unset)_ | Set to `true` for longer health check timeouts (60s vs 30s) |

### Temp Directory Layout

Each E2E test run creates a single temp directory under `/tmp/pinchtab-test-*/`:

```
/tmp/pinchtab-test-123456789/
├── pinchtab          # Compiled test binary
├── state/            # Dashboard state (profiles, instances)
└── profiles/         # Chrome user-data directories
```

Everything is cleaned up automatically when tests finish.

## Test File Structure

E2E tests are organized by group and feature:

```
tests/e2e/scenarios/
├── api/           # Browser control, tabs, actions, files
│   ├── browser-basic.sh
│   ├── browser-extended.sh
│   ├── tabs-basic.sh
│   └── ...
├── cli/           # CLI command tests
│   ├── browser-basic.sh
│   ├── browser-extended.sh
│   └── ...
└── infra/         # System, network, security, stealth
    ├── system-basic.sh
    ├── system-extended.sh
    ├── stealth-basic.sh
    ├── orchestrator-extended.sh
    └── ...
```

- `*-basic.sh` is the PR happy-path layer
- `*-extended.sh` adds extra and edge-case coverage
- `*-smoke.sh` covers slow or high-setup production smoke checks
- Standalone scripts (no suffix) run only in extended mode

Docker Compose files:
- `tests/e2e/docker-compose.yml` — single-instance stack for basic tests
- `tests/e2e/docker-compose-multi.yml` — multi-instance stack for extended tests

## E2E Results

The Go e2e runner captures suite output, prints the final suite summary, and writes each suite's summary and markdown report under `tests/e2e/results/`:

- `summary-api.txt` / `report-api.md`
- `summary-api-extended.txt` / `report-api-extended.md`
- `summary-cli.txt` / `report-cli.md`
- `summary-cli-extended.txt` / `report-cli-extended.md`
- `summary-infra.txt` / `report-infra.md`
- `summary-infra-extended.txt` / `report-infra-extended.md`
- `summary-api-smoke.txt` / `report-api-smoke.md`
- `summary-cli-smoke.txt` / `report-cli-smoke.md`
- `summary-infra-smoke.txt` / `report-infra-smoke.md`
- `summary-plugin-smoke.txt` / `report-plugin-smoke.md`
- `summary-docker-smoke.txt` / `report-docker-smoke.md`

Each suite also writes `timings-<suite>.json` beside its markdown report: one record per test with its scenario, name, duration in ms and status, plus per-scenario and suite totals. The records come from the same `E2E_RESULT` stream the markdown report is built from, so the two always agree on test count and total.

Every record carries the suite, the stack (`singleCompose` or `multiCompose`) and the browser, because a comparison that mixes those is measuring contention rather than the change under test.

Read a run back without re-running it:

```bash
go run ./tests/tools/runner e2e --suite api-extended --slowest 10
```

That prints the ten slowest tests and the per-scenario totals from the JSON. It starts nothing and does not need Docker.

Gate suite-speed claims on the per-scenario and per-suite totals, not on per-test durations: measured run-to-run swing is around 16%, so aggregates over 20+ tests are the only stable signal. Tests under 100ms should be left out of any ratio entirely — a 10ms to 20ms move reads as +100% and means nothing. The threshold travels with the data as `comparisonFloorMs`.

The runner clears the target suite files before each run so stale results do not survive into the next suite. It also saves the captured suite output as `output-*.log`, captures compose service logs on failure, and writes GitHub Actions outputs and step summaries when running in CI.

## Writing New E2E Tests

Add new coverage directly to a grouped entrypoint in `tests/e2e/scenarios/api/`, `tests/e2e/scenarios/cli/`, `tests/e2e/scenarios/infra/`, or `tests/e2e/scenarios/plugin/`. Keep `*-basic.sh` focused on the PR happy path, put deeper coverage in the matching `*-extended.sh`, and put slow/high-setup checks in `*-smoke.sh`. Add manifest metadata only when the scenario needs non-default services, readiness targets, helper, tier, or tags.

### Example: Grouped API Entrypoint

```bash
#!/bin/bash

# tests/e2e/scenarios/api/tabs-basic.sh
GROUP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${GROUP_DIR}/../../helpers/api.sh"

start_test "tab-scoped snapshot"
# ...

start_test "tab focus"
# ...
end_test
```

### Scenario Files Are Isolated

Each scenario file is sourced into its own subshell, so its variables, functions
and traps die with the file. A scenario must not rely on state another scenario
left behind — not a variable, not a helper function, not an open tab, and not
the value of `E2E_SERVER`. Anything two scenarios both need belongs in
`tests/e2e/helpers/`, and anything a scenario sets up it must be able to set up
itself.

Failure accounting crosses the subshell boundary through exit status: a scenario
that ends with any failed test exits non-zero and the executor fails the suite.
That holds however the file ends — a guard that records a failure and then calls
`exit 0` to stop the file still fails it. The `E2E_RESULT` lines the Go runner
parses are unaffected — they are printed, not accumulated in a variable.

To clean up after a scenario, define `scenario_cleanup`; the executor calls it
when the file finishes, including when the file exits early:

```bash
scenario_cleanup() {
  rm -f "$AUTH_COOKIE_FILE"
}
```

Do not install `trap ... EXIT` in a scenario — bash keeps exactly one EXIT trap,
so a second `trap` silently replaces the first.

### Assertions Must Be Able to Fail

Every branch of a scenario ends in `pass_assert`, `fail_assert`, or a named skip
(`skip_assert` / `skip_test`) — never in a pass that stands in for a failure. A
helper that reports "the thing I was checking is not there" as a pass makes the
scenario green for every input, which is indistinguishable in the report from
working code. Use a skip only when the property genuinely cannot be observed on
this server or provider, and say in the message which condition is missing.

### Waiting

Do not `sleep` for state to arrive. `wait_until <predicate> [timeout] [interval]`
(in `helpers/base.sh`) polls the predicate, returns as soon as it holds, and
fails the current test loudly if the timeout passes — so a wait is bounded on a
slow machine and costs nothing on a fast one:

```bash
BEFORE_TS=$(newest_activity_event /navigate | jq -r '.timestamp // empty')
pt_post /navigate -d "{\"url\":\"${FIXTURES_URL}/buttons.html\"}"
assert_ok "navigate"

if wait_until "activity_event_landed /navigate '$BEFORE_TS'" 10; then
  assert_json_eq "$ACTIVITY_EVENT" '.status' "200" "activity event status=200"
fi
```

`wait_for_instance_ready` stays separate: it gates a suite before any test is
running, so it reports a readiness failure to its caller instead of failing a
test that has not started.

### Targeting Another Server

Never assign `E2E_SERVER` directly. `with_server <base_url> <command...>` points
it at another server in the stack for the duration of one command and restores
the previous value whatever the command returns, passing the command's exit
status back:

```bash
with_server "$E2E_SECURE_SERVER" secure_only_checks
with_server "http://127.0.0.1:1" pt health
```

`pt_on <base_url> <token> <command...>` is the same thing when the second server
also has its own token — it retargets `E2E_SERVER` and `E2E_SERVER_TOKEN`
together and restores both.

## Coverage

Generate coverage for unit tests:

```bash
go test ./... -coverprofile=coverage.out
go tool cover -html=coverage.out
```

Note: E2E tests are black-box tests and don't contribute to code coverage metrics directly.
