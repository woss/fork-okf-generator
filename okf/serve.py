"""okf serve — launch a local HTTP server for an OKF bundle viz.

Usage:
  okf serve [<bundle_dir>] [options]
  okf serve --stop              Stop a running server
  okf serve --port 8080
"""

import argparse
import http.server
import os
import socketserver
import subprocess
import sys
import webbrowser
from pathlib import Path


from okf.config import load as load_config, _get
_cfg = load_config()
PORT = _get(_cfg, "serve.port", 8000)
HOST = _get(_cfg, "serve.host", "127.0.0.1")
PID_DIR = Path.home() / ".cache" / "okf"
PID_FILE = PID_DIR / "serve.pid"


def write_pid():
    PID_DIR.mkdir(parents=True, exist_ok=True)
    PID_FILE.write_text(str(os.getpid()))


def read_pid() -> int | None:
    if PID_FILE.exists():
        try:
            return int(PID_FILE.read_text().strip())
        except (ValueError, OSError):
            return None
    return None


def stop_server(silent=False):
    pid = read_pid()
    if pid is not None:
        try:
            os.kill(pid, 15)
            if not silent:
                print(f"  Stopped previous server (PID {pid}).")
        except ProcessLookupError:
            pass
    PID_FILE.unlink(missing_ok=True)


class VizzHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" and os.path.exists("viz.html"):
            self.send_response(302)
            self.send_header("Location", "/viz.html")
            self.end_headers()
            return
        super().do_GET()

    def log_message(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Launch a local HTTP server for an OKF bundle visualization.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("bundle_dir", nargs="?", default="./okf_bundle", help="Directory to serve (default: ./okf_bundle)")
    parser.add_argument("--port", "-p", type=int, default=PORT, help=f"Port (default: {PORT})")
    parser.add_argument("--host", default=HOST, help=f"Host (default: {HOST})")
    parser.add_argument("--open", "-o", action="store_true", help="Open browser automatically")
    parser.add_argument("--stop", action="store_true", help="Stop a running server")
    args = parser.parse_args()

    if args.stop:
        stop_server()
        sys.exit(0)

    # Stop any existing server on this port before starting
    stop_server(silent=True)

    directory = Path(args.bundle_dir).resolve()
    if not directory.exists():
        print(f"ERROR: Directory not found: {directory}", file=sys.stderr)
        sys.exit(1)

    os.chdir(directory)

    # Auto-generate viz if missing
    if not os.path.exists("viz.html"):
        bundle_marker = directory / "index.md"
        if bundle_marker.exists():
            print(f"  Generating viz.html from {directory.name}...")
            try:
                result = subprocess.run(["okf", "visualize", str(directory)], capture_output=True, text=True, timeout=120)
                if result.returncode != 0:
                    print(f"  WARNING: visualize failed (run 'okf visualize {directory}' manually)")
                else:
                    print(f"  {result.stdout.strip()}")
            except FileNotFoundError:
                print(f"  WARNING: 'okf' not found on PATH. Run 'okf visualize {directory}' manually.")
            except subprocess.TimeoutExpired:
                print(f"  WARNING: visualize timed out. Run 'okf visualize {directory}' manually.")

    url = f"http://{args.host}:{args.port}/viz.html"
    has_viz = os.path.exists("viz.html")
    if has_viz:
        print(f"  OKF Viz: {url}")
    else:
        print(f"  No viz.html found in {directory.name}.")
        print(f"  {url.replace('/viz.html', '')}")

    write_pid()

    if args.open and has_viz:
        webbrowser.open(url)
    elif args.open:
        webbrowser.open(f"http://{args.host}:{args.port}")

    try:
        with socketserver.TCPServer((args.host, args.port), VizzHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        PID_FILE.unlink(missing_ok=True)
        sys.exit(0)
    except OSError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
