package mcp

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"testing"

	"github.com/mark3labs/mcp-go/mcp"
	"gopkg.in/yaml.v3"
)

const preambleBudgetPath = "testdata/preamble_budget.json"

const ciWorkflowPath = ".github/workflows/ci-go.yml"

const toolPayloadSurface = "mcp:allTools"

var fileSurfaces = []string{"skills/pinchtab-mcp/SKILL.md", "skills/pinchtab/SKILL.md"}

type preambleBudget struct {
	Surface  string `json:"surface"`
	MinBytes int    `json:"minBytes"`
	MaxBytes int    `json:"maxBytes"`
	TakenOn  string `json:"takenOn"`
	Commit   string `json:"commit"`
}

type toolComposition struct {
	tools            int
	descriptionBytes int
	repeatedBytes    int
}

type preambleMeasurement struct {
	surface     string
	bytes       int
	composition *toolComposition
}

func (m preambleMeasurement) approxTokens() int { return m.bytes / 4 }

func percentOf(part, whole int) string {
	if whole == 0 {
		return "-"
	}
	return fmt.Sprintf("%d%%", part*100/whole)
}

type propertyCensus struct {
	bodyBytes int
	copies    int
}

func repeatedPropertyBytes(tools []mcp.Tool) (int, error) {
	census := map[string]*propertyCensus{}
	for _, tool := range tools {
		for name, value := range tool.InputSchema.Properties {
			body, err := json.Marshal(value)
			if err != nil {
				return 0, err
			}
			key := strconv.Quote(name) + ":" + string(body)
			entry := census[key]
			if entry == nil {
				entry = &propertyCensus{bodyBytes: len(body)}
				census[key] = entry
			}
			entry.copies++
		}
	}

	repeated := 0
	for _, entry := range census {
		repeated += entry.bodyBytes * (entry.copies - 1)
	}
	return repeated, nil
}

func toolDescriptionBytes(tools []mcp.Tool) int {
	total := 0
	for _, tool := range tools {
		total += len(tool.Description)
	}
	return total
}

func measureToolPayload(t *testing.T) preambleMeasurement {
	t.Helper()
	tools := allTools()
	payload, err := json.Marshal(tools)
	if err != nil {
		t.Fatalf("cannot serialize %s, so the preamble an MCP agent loads is unmeasurable: %v", toolPayloadSurface, err)
	}
	repeated, err := repeatedPropertyBytes(tools)
	if err != nil {
		t.Fatalf("cannot serialize the input-schema properties of %s: %v", toolPayloadSurface, err)
	}
	return preambleMeasurement{
		surface: toolPayloadSurface,
		bytes:   len(payload),
		composition: &toolComposition{
			tools:            len(tools),
			descriptionBytes: toolDescriptionBytes(tools),
			repeatedBytes:    repeated,
		},
	}
}

func measureFile(t *testing.T, surface string) preambleMeasurement {
	t.Helper()
	body, err := os.ReadFile(filepath.Join("..", "..", surface))
	if err != nil {
		t.Fatalf("cannot read %s, so the preamble it costs is unmeasurable: %v", surface, err)
	}
	return preambleMeasurement{surface: surface, bytes: len(body)}
}

func loadPreambleBudgets(t *testing.T) map[string]preambleBudget {
	t.Helper()
	body, err := os.ReadFile(preambleBudgetPath)
	if err != nil {
		t.Fatalf("cannot read %s, so nothing holds the preamble to a recorded number: %v", preambleBudgetPath, err)
	}
	var recorded []preambleBudget
	if err := json.Unmarshal(body, &recorded); err != nil {
		t.Fatalf("cannot parse %s: %v", preambleBudgetPath, err)
	}
	budgets := make(map[string]preambleBudget, len(recorded))
	for _, budget := range recorded {
		budgets[budget.Surface] = budget
	}
	return budgets
}

func renderPreambleReport(measurements []preambleMeasurement, budgets map[string]preambleBudget) string {
	const row = "%-30s %6s %8s %8s %8s %8s %8s %8s\n"
	var report strings.Builder
	report.WriteString("agent preamble\n")
	fmt.Fprintf(&report, row, "surface", "tools", "bytes", "~tokens", "desc", "repeat", "floor", "budget")
	for _, measurement := range measurements {
		tools, description, repeat := "-", "-", "-"
		if composition := measurement.composition; composition != nil {
			tools = strconv.Itoa(composition.tools)
			description = percentOf(composition.descriptionBytes, measurement.bytes)
			repeat = percentOf(composition.repeatedBytes, measurement.bytes)
		}
		fmt.Fprintf(&report, row,
			measurement.surface,
			tools,
			strconv.Itoa(measurement.bytes),
			strconv.Itoa(measurement.approxTokens()),
			description,
			repeat,
			strconv.Itoa(budgets[measurement.surface].MinBytes),
			strconv.Itoa(budgets[measurement.surface].MaxBytes),
		)
	}
	return report.String()
}

func TestAgentPreambleStaysWithinBudget(t *testing.T) {
	payload := measureToolPayload(t)
	if payload.composition.tools == 0 {
		t.Fatalf("allTools() returned no tools, so every budget below would pass while measuring an empty surface")
	}

	measurements := []preambleMeasurement{payload}
	for _, surface := range fileSurfaces {
		measurements = append(measurements, measureFile(t, surface))
	}

	budgets := loadPreambleBudgets(t)
	t.Log("\n" + renderPreambleReport(measurements, budgets))

	for _, measurement := range measurements {
		budget, recorded := budgets[measurement.surface]
		if !recorded {
			t.Errorf("%s is measured but carries no budget in %s; record today's number there so the surface can only ratchet down", measurement.surface, preambleBudgetPath)
			continue
		}
		if budget.MinBytes <= 0 {
			t.Errorf("%s carries a budget but no floor in %s; a missing minBytes reads as 0, which silently disables the deletion guard for this surface — record a floor beside its budget", measurement.surface, preambleBudgetPath)
		}
		if measurement.bytes > budget.MaxBytes {
			over := measurement.bytes - budget.MaxBytes
			t.Errorf("%s is %d bytes (~%d tokens), %d bytes (~%d tokens) over the budget of %d recorded on %s at %s; shrink the surface, or raise the budget as a deliberate line in this diff",
				measurement.surface, measurement.bytes, measurement.approxTokens(), over, over/4, budget.MaxBytes, budget.TakenOn, budget.Commit)
		}
		if measurement.bytes < budget.MinBytes {
			t.Errorf("%s is %d bytes, under the floor of %d recorded on %s at %s; a preamble surface does not shrink this far by optimisation, so this reads as the surface being deleted or truncated rather than improved — if the shrink is real, lower the floor in the same diff",
				measurement.surface, measurement.bytes, budget.MinBytes, budget.TakenOn, budget.Commit)
		}
	}
}

type ciTriggerFilter struct {
	Paths       []string `yaml:"paths"`
	PathsIgnore []string `yaml:"paths-ignore"`
}

type ciWorkflowTriggers struct {
	On struct {
		Push        ciTriggerFilter `yaml:"push"`
		PullRequest ciTriggerFilter `yaml:"pull_request"`
	} `yaml:"on"`
}

type ciTrigger struct {
	name   string
	filter ciTriggerFilter
}

func loadCITriggers(t *testing.T) []ciTrigger {
	t.Helper()
	body, err := os.ReadFile(filepath.Join("..", "..", ciWorkflowPath))
	if err != nil {
		t.Fatalf("cannot read %s, so nothing checks that CI runs on the surfaces this file measures: %v", ciWorkflowPath, err)
	}
	var workflow ciWorkflowTriggers
	if err := yaml.Unmarshal(body, &workflow); err != nil {
		t.Fatalf("cannot parse %s: %v", ciWorkflowPath, err)
	}
	return []ciTrigger{
		{name: "push", filter: workflow.On.Push},
		{name: "pull_request", filter: workflow.On.PullRequest},
	}
}

func TestEveryMeasuredFileSurfaceTriggersCI(t *testing.T) {
	if len(fileSurfaces) == 0 {
		t.Fatalf("fileSurfaces is empty, so this guard has nothing to look for in %s", ciWorkflowPath)
	}
	for _, trigger := range loadCITriggers(t) {
		if len(trigger.filter.PathsIgnore) > 0 {
			t.Errorf("%s filters its %s trigger with paths-ignore, which cannot re-include a measured surface once a broad pattern excludes it — that is how skills/** kept a SKILL.md growth from ever reaching the Go suite; express the filter as paths so every measured surface is named",
				ciWorkflowPath, trigger.name)
			continue
		}
		if len(trigger.filter.Paths) == 0 {
			continue
		}
		listed := make(map[string]bool, len(trigger.filter.Paths))
		for _, pattern := range trigger.filter.Paths {
			listed[pattern] = true
		}
		for _, surface := range fileSurfaces {
			if !listed[surface] {
				t.Errorf("%s is measured here but is not listed in the %s paths filter of %s; the filter excludes documentation by default, so a PR touching only that file skips the Go suite entirely and its budget goes unchecked on exactly the change that can breach it — add the surface to both triggers whenever it is added here",
					surface, trigger.name, ciWorkflowPath)
			}
		}
	}
}
