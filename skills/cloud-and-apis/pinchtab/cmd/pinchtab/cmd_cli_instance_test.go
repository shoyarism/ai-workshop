package main

import (
	"bytes"
	"sort"
	"strings"
	"testing"

	"github.com/pinchtab/pinchtab/internal/cli"
	"github.com/spf13/cobra"
	"github.com/spf13/pflag"
)

func instanceSubcommand(t *testing.T, name string) *cobra.Command {
	t.Helper()
	for _, sub := range instanceCmd.Commands() {
		if sub.Name() == name {
			return sub
		}
	}
	t.Fatalf("pinchtab instance has no %q subcommand; its subcommands are %v", name, instanceSubcommandNames())
	return nil
}

func instanceSubcommandNames() []string {
	var names []string
	for _, sub := range instanceCmd.Commands() {
		names = append(names, sub.Name())
	}
	return names
}

func TestInstanceOwnsTheListing(t *testing.T) {
	list := instanceSubcommand(t, "list")
	if list.Run == nil {
		t.Error("pinchtab instance list has no Run, so the listing is registered but does nothing")
	}
	if list.Hidden {
		t.Error("pinchtab instance list is hidden, so the command that produces instance ids stays undiscoverable")
	}
}

func TestInstancesStaysRunnableAsADeprecatedAlias(t *testing.T) {
	if instancesCmd.Run == nil {
		t.Fatal("pinchtab instances no longer runs; existing scripts and docs calling it would break")
	}
	if instancesCmd.Deprecated == "" {
		t.Error("pinchtab instances is not marked deprecated, so nothing steers callers to the canonical spelling")
	}
	if !strings.Contains(instancesCmd.Deprecated, "pinchtab instance list") {
		t.Errorf("the deprecation notice does not name the replacement: %q", instancesCmd.Deprecated)
	}
	if !instancesCmd.Hidden {
		t.Error("pinchtab instances is still listed at the root, which keeps two commands one character apart for the same subject")
	}
}

func TestInstanceIDErrorsNameTheListCommand(t *testing.T) {
	for _, name := range []string{"logs", "stop", "restart", "navigate"} {
		t.Run(name, func(t *testing.T) {
			sub := instanceSubcommand(t, name)
			if sub.Args == nil {
				t.Fatalf("pinchtab instance %s has no Args validator", name)
			}
			err := sub.Args(sub, nil)
			if err == nil {
				t.Fatalf("pinchtab instance %s accepted zero arguments", name)
			}
			if !strings.Contains(err.Error(), "pinchtab instance list") {
				t.Errorf("pinchtab instance %s reports %q; an operator told they need an id is not told where ids come from", name, err)
			}
		})
	}
}

func TestInstanceIDValidatorAcceptsTheRightArity(t *testing.T) {
	if err := instanceSubcommand(t, "logs").Args(instanceLogsCmd, []string{"inst_1"}); err != nil {
		t.Errorf("logs rejected a single id: %v", err)
	}
	if err := instanceSubcommand(t, "navigate").Args(instanceNavigateCmd, []string{"inst_1", "https://example.com"}); err != nil {
		t.Errorf("navigate rejected an id plus a URL: %v", err)
	}
	if err := instanceSubcommand(t, "navigate").Args(instanceNavigateCmd, []string{"inst_1"}); err == nil {
		t.Error("navigate accepted an id with no URL")
	}
}

// The usage template renders one shared block for every command, so a heading
// with nothing under it appears on every leaf command in the CLI, not just the
// one it was reported against.
func TestUsageOmitsTheCommandsHeadingWhenThereAreNoSubcommands(t *testing.T) {
	root := &cobra.Command{Use: "root"}
	leaf := &cobra.Command{Use: "leaf", Short: "a leaf", Run: func(*cobra.Command, []string) {}}
	parent := &cobra.Command{Use: "parent", Short: "a parent"}
	parent.AddCommand(&cobra.Command{Use: "child", Short: "a child", Run: func(*cobra.Command, []string) {}})
	root.AddCommand(leaf, parent)
	cli.SetupUsage(root)

	var leafOut bytes.Buffer
	leaf.SetOut(&leafOut)
	if err := leaf.Usage(); err != nil {
		t.Fatal(err)
	}
	if strings.Contains(leafOut.String(), "Commands") {
		t.Errorf("a command with no subcommands still renders a Commands heading with nothing under it:\n%s", leafOut.String())
	}

	var parentOut bytes.Buffer
	parent.SetOut(&parentOut)
	if err := parent.Usage(); err != nil {
		t.Fatal(err)
	}
	if !strings.Contains(parentOut.String(), "Commands") {
		t.Errorf("a command with subcommands lost its Commands heading:\n%s", parentOut.String())
	}
	if !strings.Contains(parentOut.String(), "child") {
		t.Errorf("subcommands are no longer listed:\n%s", parentOut.String())
	}
}

func TestExecutePrintsAnErrorOnlyWhenCobraDidNot(t *testing.T) {
	root := &cobra.Command{Use: "root"}
	for _, tc := range []struct {
		name       string
		cmd        *cobra.Command
		rootSilent bool
		want       bool
	}{
		{"cobra printed it", &cobra.Command{Use: "c"}, false, false},
		{"command silenced it", &cobra.Command{Use: "c", SilenceErrors: true}, false, true},
		{"root silenced it", &cobra.Command{Use: "c"}, true, true},
		{"no command resolved", nil, false, true},
	} {
		t.Run(tc.name, func(t *testing.T) {
			root.SilenceErrors = tc.rootSilent
			if got := shouldPrintCommandError(tc.cmd, root); got != tc.want {
				t.Errorf("shouldPrintCommandError() = %v, want %v; a wrong answer here either prints the error twice or swallows it entirely", got, tc.want)
			}
		})
	}
}

func flagNames(cmd *cobra.Command) []string {
	var names []string
	cmd.Flags().VisitAll(func(f *pflag.Flag) {
		names = append(names, f.Name)
	})
	sort.Strings(names)
	return names
}

// listInstances forwards the INVOKED command to the action, so every flag the
// action reads has to be declared on both spellings — sharing the Run body does
// not share the flags. The --json flag was declared only on the alias, which
// left the documented `pinchtab instance list --json` failing with "unknown
// flag" while the deprecated spelling kept working.
func TestBothInstanceListSpellingsExposeTheSameFlags(t *testing.T) {
	canonical := flagNames(instanceSubcommand(t, "list"))
	alias := flagNames(instancesCmd)

	if len(canonical) == 0 {
		t.Fatal("pinchtab instance list declares no flags at all; this guard would pass vacuously")
	}
	if strings.Join(canonical, ",") != strings.Join(alias, ",") {
		t.Errorf("the two spellings of the listing accept different flags:\n  instance list = %v\n  instances     = %v\nA flag on only one of them breaks whichever spelling the docs tell people to run.",
			canonical, alias)
	}
}
