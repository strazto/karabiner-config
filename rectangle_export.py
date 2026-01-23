#!/usr/bin/env python3
from __future__ import annotations

import argparse
import plistlib
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping


DOMAIN: str = "com.knollsoft.Rectangle"


def run_defaults_export(domain: str) -> bytes:
    """Export a macOS NSUserDefaults domain as raw plist bytes."""
    proc = subprocess.run(
        ["defaults", "export", domain, "-"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"defaults export failed for {domain}: {err}")
    if not proc.stdout:
        raise RuntimeError(f"defaults export returned empty output for {domain}")
    return proc.stdout


def load_plist(data: bytes) -> Any:
    """Load plist bytes into Python objects."""
    try:
        return plistlib.loads(data)
    except Exception as e:
        raise RuntimeError(f"Failed to parse exported plist: {e}") from e


def write_sorted_plist(value: Any, out_path: Path) -> None:
    """
    Write plist as XML with stable key ordering.

    Note: This sorts dict keys deterministically. List ordering is preserved.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as f:
        plistlib.dump(value, f, fmt=plistlib.FMT_XML, sort_keys=True)


def lint_plist(out_path: Path) -> None:
    """Validate the written plist using plutil if available."""
    proc = subprocess.run(
        ["plutil", "-lint", str(out_path)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        out = proc.stdout.decode("utf-8", errors="replace").strip()
        err = proc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"plutil -lint failed:\n{out}\n{err}")


def ensure_dict_root(value: Any) -> None:
    if not isinstance(value, Mapping):
        raise RuntimeError(f"Unexpected plist root type: {type(value).__name__}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Export Rectangle (com.knollsoft.Rectangle) preferences to a stable-sorted XML plist."
    )
    p.add_argument(
        "--out",
        type=Path,
        default=Path("./Rectangle.plist"),
        help="Output path (relative to current working directory). Default: ./Rectangle.plist",
    )
    p.add_argument(
        "--no-lint",
        action="store_true",
        help="Skip plutil -lint validation.",
    )
    return p.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    try:
        raw = run_defaults_export(DOMAIN)
        data = load_plist(raw)
        ensure_dict_root(data)
        write_sorted_plist(data, args.out)
        if not args.no_lint:
            lint_plist(args.out)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(f"Wrote: {args.out.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
