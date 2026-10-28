package orchestrator

import (
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"testing"
)

func writeBinary(t *testing.T, path, content string, mode os.FileMode) string {
	t.Helper()
	if err := os.WriteFile(path, []byte(content), mode); err != nil {
		t.Fatalf("cannot write %s: %v", path, err)
	}
	if err := os.Chmod(path, mode); err != nil {
		t.Fatalf("cannot chmod %s: %v", path, err)
	}
	return path
}

func readBinary(t *testing.T, path string) string {
	t.Helper()
	body, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("cannot read %s: %v", path, err)
	}
	return string(body)
}

func stagedTempFiles(t *testing.T, dir string) []string {
	t.Helper()
	entries, err := os.ReadDir(dir)
	if err != nil {
		t.Fatalf("cannot list %s: %v", dir, err)
	}
	var leftovers []string
	for _, entry := range entries {
		if strings.Contains(entry.Name(), ".tmp-") {
			leftovers = append(leftovers, entry.Name())
		}
	}
	return leftovers
}

func TestInstallStableBinaryPublishesTheWholeFileOrNothing(t *testing.T) {
	dir := t.TempDir()
	src := writeBinary(t, filepath.Join(dir, "running"), "the whole binary", 0755)
	dst := filepath.Join(dir, "pinchtab")

	if err := installStableBinary(src, dst); err != nil {
		t.Fatalf("install failed: %v", err)
	}

	if got := readBinary(t, dst); got != "the whole binary" {
		t.Errorf("destination holds %q, want the full source content", got)
	}
	info, err := os.Stat(dst)
	if err != nil {
		t.Fatalf("cannot stat the installed binary: %v", err)
	}
	if runtime.GOOS != "windows" && info.Mode().Perm()&0111 == 0 {
		t.Errorf("installed binary has mode %v, want an executable bit", info.Mode().Perm())
	}
	if leftovers := stagedTempFiles(t, dir); len(leftovers) != 0 {
		t.Errorf("install left staging files behind: %v", leftovers)
	}
}

func TestInstallStableBinarySkipsAnUnchangedDestination(t *testing.T) {
	dir := t.TempDir()
	src := writeBinary(t, filepath.Join(dir, "running"), "the whole binary", 0755)
	dst := filepath.Join(dir, "pinchtab")

	if err := installStableBinary(src, dst); err != nil {
		t.Fatalf("first install failed: %v", err)
	}

	srcInfo, err := os.Stat(src)
	if err != nil {
		t.Fatalf("cannot stat the source: %v", err)
	}
	const marker = "SAME LENGTH MARK"
	writeBinary(t, dst, marker, 0755)
	if err := os.Chtimes(dst, srcInfo.ModTime(), srcInfo.ModTime()); err != nil {
		t.Fatalf("cannot align the destination mtime: %v", err)
	}

	if err := installStableBinary(src, dst); err != nil {
		t.Fatalf("second install failed: %v", err)
	}

	if got := readBinary(t, dst); got != marker {
		t.Errorf("destination holds %q, want the marker: a destination already matching the source must not be recopied on every orchestrator construction", got)
	}
}

func TestInstallStableBinaryLeavesAGoodDestinationIntactWhenTheCopyFails(t *testing.T) {
	for _, tc := range []struct {
		name string
		src  func(t *testing.T, dir string) string
	}{
		{
			name: "source cannot be opened",
			src:  func(_ *testing.T, dir string) string { return filepath.Join(dir, "gone") },
		},
		{
			name: "source fails part-way through the copy",
			src: func(t *testing.T, dir string) string {
				unreadable := filepath.Join(dir, "unreadable")
				if err := os.Mkdir(unreadable, 0755); err != nil {
					t.Fatalf("cannot create %s: %v", unreadable, err)
				}
				return unreadable
			},
		},
	} {
		t.Run(tc.name, func(t *testing.T) {
			dir := t.TempDir()
			dst := writeBinary(t, filepath.Join(dir, "pinchtab"), "the previously installed binary", 0755)

			if err := installStableBinary(tc.src(t, dir), dst); err == nil {
				t.Fatal("install from a broken source reported success")
			}

			if got := readBinary(t, dst); got != "the previously installed binary" {
				t.Errorf("destination holds %q, want the pre-existing binary untouched; a launch binary must never be observed empty or partial", got)
			}
			if leftovers := stagedTempFiles(t, dir); len(leftovers) != 0 {
				t.Errorf("failed install left staging files behind: %v", leftovers)
			}
		})
	}
}

func TestSelectLaunchBinaryRejectsAnUnusableStableCopy(t *testing.T) {
	dir := t.TempDir()
	missingRunning := filepath.Join(dir, "gone")

	for _, tc := range []struct {
		name       string
		stable     func(t *testing.T) string
		wantStable bool
		windows    bool
	}{
		{
			name:       "truncated stable binary",
			stable:     func(t *testing.T) string { return writeBinary(t, filepath.Join(t.TempDir(), "pinchtab"), "", 0755) },
			wantStable: false,
			windows:    true,
		},
		{
			name:       "non-executable stable binary",
			stable:     func(t *testing.T) string { return writeBinary(t, filepath.Join(t.TempDir(), "pinchtab"), "real", 0644) },
			wantStable: false,
		},
		{
			name:       "missing stable binary",
			stable:     func(t *testing.T) string { return filepath.Join(t.TempDir(), "pinchtab") },
			wantStable: false,
			windows:    true,
		},
		{
			name:       "good stable binary",
			stable:     func(t *testing.T) string { return writeBinary(t, filepath.Join(t.TempDir(), "pinchtab"), "real", 0755) },
			wantStable: true,
			windows:    true,
		},
	} {
		t.Run(tc.name, func(t *testing.T) {
			if !tc.windows && runtime.GOOS == "windows" {
				t.Skip("permission bits are not modelled on windows")
			}
			stable := tc.stable(t)
			got := selectLaunchBinary(missingRunning, stable)
			want := missingRunning
			if tc.wantStable {
				want = stable
			}
			if got != want {
				t.Errorf("selectLaunchBinary picked %q, want %q", got, want)
			}
		})
	}
}

func TestSelectLaunchBinaryPrefersTheRunningExecutable(t *testing.T) {
	dir := t.TempDir()
	running := writeBinary(t, filepath.Join(dir, "running"), "running", 0755)
	stable := writeBinary(t, filepath.Join(dir, "pinchtab"), "stable", 0755)

	if got := selectLaunchBinary(running, stable); got != running {
		t.Errorf("selectLaunchBinary picked %q, want the running executable %q", got, running)
	}
}

func TestInstallStableBinaryDoesNotDestroyTheBinaryItWasLaunchedFrom(t *testing.T) {
	dir := t.TempDir()
	binary := writeBinary(t, filepath.Join(dir, "pinchtab"), "the running server image", 0755)

	if err := installStableBinary(binary, binary); err != nil {
		t.Fatalf("installing the binary over itself failed: %v", err)
	}

	if got := readBinary(t, binary); got != "the running server image" {
		t.Errorf("binary holds %q after installing it over itself; a server launched from the stable path must not truncate its own image", got)
	}
	if leftovers := stagedTempFiles(t, dir); len(leftovers) != 0 {
		t.Errorf("self-install left staging files behind: %v", leftovers)
	}
}

func TestInstallStableBinaryLeavesTheDestinationMatchingTheSource(t *testing.T) {
	dir := t.TempDir()
	src := writeBinary(t, filepath.Join(dir, "running"), "the whole binary", 0755)
	dst := filepath.Join(dir, "pinchtab")

	if err := installStableBinary(src, dst); err != nil {
		t.Fatalf("first install failed: %v", err)
	}
	first, err := os.Stat(dst)
	if err != nil {
		t.Fatalf("cannot stat the installed binary: %v", err)
	}

	if err := installStableBinary(src, dst); err != nil {
		t.Fatalf("second install failed: %v", err)
	}
	second, err := os.Stat(dst)
	if err != nil {
		t.Fatalf("cannot stat the reinstalled binary: %v", err)
	}

	if !os.SameFile(first, second) {
		t.Errorf("installing the same source twice replaced %s with a different file; the first install must leave the destination matching the source, otherwise every orchestrator construction recopies the launch binary and the skip never engages in production", dst)
	}
	if leftovers := stagedTempFiles(t, dir); len(leftovers) != 0 {
		t.Errorf("repeated install left staging files behind: %v", leftovers)
	}
}
