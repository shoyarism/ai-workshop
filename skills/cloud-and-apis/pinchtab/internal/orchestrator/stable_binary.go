package orchestrator

import (
	"io"
	"log/slog"
	"os"
	"path/filepath"
	"runtime"
)

func resolveStableBinary(baseDir string) string {
	binDir := filepath.Join(filepath.Dir(baseDir), "bin")
	stableBin := filepath.Join(binDir, "pinchtab")
	exe, _ := os.Executable()
	running := exe
	if running == "" {
		running = os.Args[0]
	}

	if err := os.MkdirAll(binDir, 0755); err != nil {
		slog.Warn("failed to create bin directory", "path", binDir, "err", err)
	}

	if exe != "" {
		if err := installStableBinary(exe, stableBin); err != nil {
			slog.Warn("failed to install pinchtab binary", "path", stableBin, "err", err)
		} else {
			slog.Debug("installed pinchtab binary", "path", stableBin)
		}
	}

	return selectLaunchBinary(running, stableBin)
}

func selectLaunchBinary(running, stable string) string {
	if isUsableBinary(running) {
		return running
	}
	if isUsableBinary(stable) {
		return stable
	}
	slog.Warn("stable pinchtab binary is missing, empty or not executable; launching from the running path instead",
		"path", stable, "running", running)
	return running
}

func isUsableBinary(path string) bool {
	info, err := os.Stat(path)
	if err != nil || !info.Mode().IsRegular() || info.Size() == 0 {
		return false
	}
	return runtime.GOOS == "windows" || info.Mode().Perm()&0111 != 0
}

func installStableBinary(src, dst string) error {
	srcInfo, err := os.Stat(src)
	if err != nil {
		return err
	}
	if matchesInstalledBinary(srcInfo, dst) {
		return nil
	}

	tmp, err := stageStableBinary(src, srcInfo, dst)
	if err != nil {
		return err
	}
	if err := os.Rename(tmp, dst); err != nil {
		_ = os.Remove(tmp)
		return err
	}
	return nil
}

func matchesInstalledBinary(srcInfo os.FileInfo, dst string) bool {
	dstInfo, err := os.Stat(dst)
	if err != nil {
		return false
	}
	return dstInfo.Size() == srcInfo.Size() && dstInfo.ModTime().Equal(srcInfo.ModTime())
}

func stageStableBinary(src string, srcInfo os.FileInfo, dst string) (staged string, err error) {
	in, err := os.Open(src)
	if err != nil {
		return "", err
	}
	defer func() { _ = in.Close() }()

	out, err := os.CreateTemp(filepath.Dir(dst), filepath.Base(dst)+".tmp-*")
	if err != nil {
		return "", err
	}
	tmp := out.Name()
	defer func() {
		if err != nil {
			_ = os.Remove(tmp)
		}
	}()

	if err = copyAndSeal(out, in); err != nil {
		return "", err
	}
	if err = os.Chmod(tmp, 0755); err != nil {
		return "", err
	}
	if err = os.Chtimes(tmp, srcInfo.ModTime(), srcInfo.ModTime()); err != nil {
		return "", err
	}
	return tmp, nil
}

func copyAndSeal(out *os.File, in io.Reader) (err error) {
	defer func() {
		if closeErr := out.Close(); err == nil {
			err = closeErr
		}
	}()
	if _, err = io.Copy(out, in); err != nil {
		return err
	}
	return out.Sync()
}
