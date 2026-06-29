"""okf — unified CLI for the OKF toolkit.

Commands:
  okf generate   <source_dir> [output_dir]   Generate OKF bundle from codebase
  okf lookup     <query> [options]            Look up a concept in a bundle
  okf pairs      <bundle_dir> [output_file]  Convert bundle to training pairs
  okf summarize  <bundle_dir>                Regenerate SUMMARY.md only

Run `okf <command> --help` for per-command options.
"""

import sys


def main():
    if len(sys.argv) < 2 or sys.argv[1] in {"-h", "--help"}:
        print(__doc__)
        print("Usage: okf <command> [args]")
        print("")
        print("Commands:")
        print("  generate   Generate OKF bundle from a codebase")
        print("  lookup     Look up concepts in a bundle")
        print("  pairs      Convert bundle to JSONL training pairs")
        print("  summarize  Regenerate SUMMARY.md from existing bundle")
        sys.exit(0)

    cmd, rest = sys.argv[1], sys.argv[2:]
    sys.argv = [f"okf {cmd}"] + rest   # rewrite argv for sub-parsers

    if cmd == "generate":
        # Handle --summarize flag routed here too
        if rest and rest[0] == "--summarize":
            sys.argv = ["okf generate", "--summarize"] + rest[1:]
        from okf.generator import main as _main
        _main()

    elif cmd == "summarize":
        # Sugar: `okf summarize <bundle>` → generator --summarize <bundle>
        sys.argv = ["okf generate", "--summarize"] + rest
        from okf.generator import main as _main
        _main()

    elif cmd == "lookup":
        from okf.lookup import main as _main
        _main()

    elif cmd == "pairs":
        from okf.pairs import main as _main
        _main()

    else:
        print(f"Unknown command: {cmd!r}", file=sys.stderr)
        print("Run `okf --help` for available commands.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
