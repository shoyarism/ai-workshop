package main

import (
	"fmt"
	"io"
	"os"
	"strings"

	"github.com/pinchtab/pinchtab/internal/cli"
	"github.com/pinchtab/pinchtab/internal/config"
)

// printAgentHints renders the bare-landing banner for `pinchtab` with no
// arguments. The probe is bounded by fetchHealthSnapshot's timeout: a live
// listener answers in single-digit milliseconds and a stopped one refuses the
// loopback connect immediately, so only a firewalled port pays the ceiling —
// cheaper than the banner asserting a server state it never checked.
func printAgentHints(cfg *config.RuntimeConfig) {
	snap, state := fetchHealthSnapshot(cfg.Port)
	// Any state but "stopped" means something answered on the port, so a log is
	// being written somewhere: a listener that refused the token is still a running
	// server, and telling its operator "no server running" is how a live log gets
	// reported as absent.
	logs := serverLogWhereForConfig(cfg, state != healthSnapshotStopped)
	renderAgentHints(os.Stdout, projectAgentStatus(cfg, snap, state, logs))
}

func renderAgentHints(out io.Writer, st agentStatus) {
	_, _ = fmt.Fprintln(out, cli.StyleStdout(cli.HeadingStyle, "PinchTab")+" "+cli.StyleStdout(cli.MutedStyle, version))
	_, _ = fmt.Fprintln(out)

	if st.running {
		serverStatus := "running"
		serverStyle := cli.SuccessStyle
		if st.guardsDown {
			serverStatus = "running (YOLO — guards down for this run)"
			serverStyle = cli.WarningStyle
		}
		_, _ = fmt.Fprintf(out, "  %-20s %s\n", "server", cli.StyleStdout(serverStyle, serverStatus))
		_, _ = fmt.Fprintf(out, "  %-20s %s\n", "listen", cli.StyleStdout(cli.ValueStyle, st.listenAddr))
		if len(st.sensitive) > 0 {
			_, _ = fmt.Fprintf(out, "  %-20s %s\n", "sensitive", cli.StyleStdout(cli.WarningStyle, strings.Join(st.sensitive, ", ")))
		}
	} else {
		_, _ = fmt.Fprintf(out, "  %-20s %s\n", "server", cli.StyleStdout(cli.WarningStyle, string(st.state)))
	}

	if st.logDestination != "" {
		_, _ = fmt.Fprintf(out, "  %-20s %s\n", "logs", cli.StyleStdout(cli.ValueStyle, st.logDestination))
	}
	if st.staleLogPath != "" {
		_, _ = fmt.Fprintf(out, "  %-20s %s\n", "", cli.StyleStdout(cli.MutedStyle, st.staleLogPath+" is not being written by this server"))
	}

	formatted := formatAllowedDomains(st.allowedDomains)
	domStyle := cli.ValueStyle
	if formatted == "all" {
		domStyle = cli.WarningStyle
	}
	_, _ = fmt.Fprintf(out, "  %-20s %s\n", "allowedDomains", cli.StyleStdout(domStyle, formatted))

	idpiStatus := "disabled"
	idpiStyle := cli.WarningStyle
	if st.idpiEnabled {
		idpiStatus = "enabled"
		idpiStyle = cli.SuccessStyle
	}
	_, _ = fmt.Fprintf(out, "  %-20s %s\n", "idpi", cli.StyleStdout(idpiStyle, idpiStatus))
	_, _ = fmt.Fprintln(out)

	cli.WriteCommandHints(out, "Next steps:", st.nextSteps, st.nextStepsWidth, true)
	_, _ = fmt.Fprintln(out)

	cli.WriteCommandHints(out, "Configure:", []cli.CommandHint{
		{Command: "pinchtab config show", Comment: "# view current config"},
		{Command: "pinchtab security", Comment: "# review security posture"},
		{Command: "pinchtab --help", Comment: "# full command list"},
	}, 44, true)
}
