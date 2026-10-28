package observe

import (
	"encoding/json"
	"strings"

	"gopkg.in/yaml.v3"
)

// All THREE states are annotated, not just the checked one: absent means the control
// has no checkedness and false means it is off, so rendering only [checked] would make
// an unchecked option look like a node the field does not apply to.
var checkedAnnotations = map[CheckedState]string{
	CheckedTrue:  " [checked]",
	CheckedFalse: " [unchecked]",
	CheckedMixed: " [mixed]",
}

// [~] is NOT available here: the compact diff renderer already uses it for
// "changed", and the same token meaning two things on one line is unreadable.
var checkedCompactAnnotations = map[CheckedState]string{
	CheckedTrue:  " [x]",
	CheckedFalse: " [ ]",
	CheckedMixed: " [/]",
}

// nodeStyle is everything that differs between the text and compact layouts. The field
// ORDER and the quoting are not in here because they do not differ — they live once, in
// appendNode. A style that could reorder fields would be a second layout model, which is
// the thing this file used to have three of.
type nodeStyle struct {
	indent   string
	refSep   string
	focused  string
	disabled string
	hidden   string
	checked  map[CheckedState]string
}

var textNodeStyle = nodeStyle{
	indent:   "  ",
	refSep:   " ",
	focused:  " [focused]",
	disabled: " [disabled]",
	hidden:   " [hidden]",
	checked:  checkedAnnotations,
}

var compactNodeStyle = nodeStyle{
	refSep:   ":",
	focused:  " *",
	disabled: " -",
	hidden:   " [hidden]",
	checked:  checkedCompactAnnotations,
}

// appendNode writes one node exactly as the caller's format emits it. It is the single
// source of truth for what a node costs, because the truncator charges the caller for
// what this writes rather than for a second hand-maintained model of it.
func appendNode(b *strings.Builder, n A11yNode, style nodeStyle, marker string) {
	for i := 0; i < n.Depth; i++ {
		b.WriteString(style.indent)
	}
	b.WriteString(n.Ref)
	b.WriteString(style.refSep)
	b.WriteString(n.Role)
	if n.Name != "" {
		b.WriteString(` "`)
		b.WriteString(n.Name)
		b.WriteByte('"')
	}
	if n.Value != "" {
		b.WriteString(` val="`)
		b.WriteString(n.Value)
		b.WriteByte('"')
	}
	if n.Focused {
		b.WriteString(style.focused)
	}
	if annotation, ok := style.checked[n.Checked]; ok {
		b.WriteString(annotation)
	}
	if n.Disabled {
		b.WriteString(style.disabled)
	}
	if n.Hidden {
		b.WriteString(style.hidden)
	}
	b.WriteString(marker)
	b.WriteByte('\n')
}

func formatNodes(nodes []A11yNode, style nodeStyle, marker func(A11yNode) string) string {
	var b strings.Builder
	for _, n := range nodes {
		suffix := ""
		if marker != nil {
			suffix = marker(n)
		}
		appendNode(&b, n, style, suffix)
	}
	return b.String()
}

func FormatSnapshotText(nodes []A11yNode) string {
	return formatNodes(nodes, textNodeStyle, nil)
}

func FormatSnapshotCompact(nodes []A11yNode) string {
	return formatNodes(nodes, compactNodeStyle, nil)
}

// FormatSnapshotCompactDiff outputs all current nodes in compact format with
// change markers: [+] for added, [~] for changed. Removed refs are listed at
// the end as [- ref]. This gives agents the full valid ref set plus change info.
func FormatSnapshotCompactDiff(nodes []A11yNode, added, changed, removed []A11yNode) string {
	addedRefs := make(map[string]bool, len(added))
	for _, n := range added {
		addedRefs[n.Ref] = true
	}
	changedRefs := make(map[string]bool, len(changed))
	for _, n := range changed {
		changedRefs[n.Ref] = true
	}

	var b strings.Builder
	b.WriteString(formatNodes(nodes, compactNodeStyle, func(n A11yNode) string {
		switch {
		case addedRefs[n.Ref]:
			return " [+]"
		case changedRefs[n.Ref]:
			return " [~]"
		default:
			return ""
		}
	}))

	if len(removed) > 0 {
		b.WriteString("# removed:")
		for _, n := range removed {
			b.WriteByte(' ')
			b.WriteString(n.Ref)
		}
		b.WriteByte('\n')
	}

	return b.String()
}

// estimateTokens is the one place bytes become tokens. Four bytes per token is the
// approximation the whole budget rests on, so it lives here rather than being spelled
// out per format — a format that divides by its own constant is a second model of the
// same thing, which is how the old estimator drifted.
func estimateTokens(bytes int) int {
	return bytes / 4
}

// nodeCost reports what one node costs the caller in the format it asked for. Every
// branch MEASURES: the text layouts by rendering through appendNode, the structured ones
// by marshalling the node with the same encoder the handler uses. Nothing here models a
// layout, so nothing here can drift away from one.
func nodeCost(format string) func(A11yNode) int {
	switch format {
	case "compact":
		return renderedNodeCost(compactNodeStyle)
	case "text":
		return renderedNodeCost(textNodeStyle)
	case "yaml":
		return func(n A11yNode) int {
			out, err := yaml.Marshal([]A11yNode{n})
			if err != nil {
				return 0
			}
			return len(out)
		}
	default:
		return func(n A11yNode) int {
			out, err := json.Marshal(n)
			if err != nil {
				return 0
			}
			// +1 for the comma or closing bracket this node brings with it once it is
			// an element of the nodes array rather than a value on its own.
			return len(out) + 1
		}
	}
}

func renderedNodeCost(style nodeStyle) func(A11yNode) int {
	var b strings.Builder
	return func(n A11yNode) int {
		b.Reset()
		appendNode(&b, n, style, "")
		return b.Len()
	}
}

// TruncateToTokens keeps the longest prefix of nodes whose rendered output fits in
// maxTokens. The budget is a ceiling, never a target to overshoot: it stops at the last
// node that fits, so the only shortfall possible is the one node that did not.
func TruncateToTokens(nodes []A11yNode, maxTokens int, format string) ([]A11yNode, bool) {
	cost := nodeCost(format)
	bytesUsed := 0
	for i, n := range nodes {
		bytesUsed += cost(n)
		if estimateTokens(bytesUsed) > maxTokens {
			return nodes[:i], true
		}
	}
	return nodes, false
}
