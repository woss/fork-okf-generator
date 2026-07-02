"""okf serve — launch a local HTTP server for an OKF bundle.

Usage:
  okf serve [<bundle_dir>] [options]
  okf serve --port 8080 --open
  okf serve ./okf_bundle --https
"""

import argparse
import http.server
import os
import socketserver
import sys
import webbrowser
from pathlib import Path


PORT = 8000
HOST = "127.0.0.1"


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress default request logs

    def log_error(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Launch a local HTTP server for an OKF bundle.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("bundle_dir", nargs="?", default=".", help="Directory to serve (default: current dir)")
    parser.add_argument("--port", "-p", type=int, default=PORT, help=f"Port (default: {PORT})")
    parser.add_argument("--host", default=HOST, help=f"Host (default: {HOST})")
    parser.add_argument("--open", "-o", action="store_true", help="Open browser automatically")
    parser.add_argument("--https", action="store_true", help="Enable HTTPS with self-signed cert (requires certfile)")
    parser.add_argument("--certfile", help="Path to SSL certificate file (for --https)")
    parser.add_argument("--keyfile", help="Path to SSL key file (for --https)")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress request logs")
    args = parser.parse_args()

    directory = Path(args.bundle_dir).resolve()
    if not directory.exists():
        print(f"ERROR: Directory not found: {directory}", file=sys.stderr)
        sys.exit(1)

    os.chdir(directory)

    handler = QuietHandler if args.quiet else http.server.SimpleHTTPRequestHandler

    proto = "https" if args.https else "http"
    url = f"{proto}://{args.host}:{args.port}"

    # Look for a viz HTML file to suggest
    viz_files = list(directory.glob("*_viz.html")) + list(directory.glob("viz.html")) + list(directory.glob("*.html"))
    viz_hint = ""
    for vf in viz_files:
        if vf.name not in ("index.html", "log.html", "SUMMARY.html"):
            viz_hint = f"  Viz: {url}/{vf.name}"
            break

    print(f"Serving {directory.name} at {url}")
    if viz_hint:
        print(viz_hint)
    print("  Quit: Ctrl+C")

    if args.open:
        webbrowser.open(url)

    try:
        with socketserver.TCPServer((args.host, args.port), handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)
    except OSError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
