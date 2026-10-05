"""Local browser interface for the existing validated replication workflow."""
import argparse
import csv
import importlib.util
import io
import json
import mimetypes
import secrets
import socket
import subprocess
import sys
import threading
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent
TOKEN = secrets.token_urlsafe(32)
LOCK = threading.Lock()
STATE = {'status': 'idle', 'lines': [], 'verification': None, 'error': None}
FILES = {
    'figure1.png', 'figure1.svg', 'extension_ownership_changes.png',
    'extension_ownership_effects.png', 'extension_ownership_effects.svg',
    'table2_replication.md', 'table2_audit_中文.md', 'figure1_中文说明.md',
    'table3_replication.md', 'table4_replication.md', 'extension_ownership_report.md',
    'table2_numeric.csv', 'table3_numeric.csv', 'table4_numeric.csv',
    'extension_ownership_effects.csv', 'figure1_bin_counts.csv',
    'workflow_summary.md', 'workflow_run.json',
}


def default_data():
    candidates = [ROOT/'01_DID/data/public.csv', ROOT.parent/'data/public.csv']
    found = [p for p in candidates if p.is_file()]
    return str(found[0]) if len(found) == 1 else ''


def verify(data):
    helper = ROOT/'skills/minimum-wage-replication/scripts/summarize_run.py'
    spec = importlib.util.spec_from_file_location('workflow_summary', helper)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.summarize(ROOT, data)


def execute(data, check_only=False):
    try:
        if not check_only:
            process = subprocess.Popen(
                [sys.executable, '-u', str(ROOT/'run_all.py'), '--data', str(data)],
                cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                text=True, encoding='utf-8', errors='replace',
                env=__import__('os').environ | {'PYTHONUTF8': '1'},
            )
            for line in process.stdout:
                with LOCK:
                    STATE['lines'].append(line.rstrip())
            if process.wait() != 0:
                raise RuntimeError('Analysis did not finish. Check the execution log and logs/workflow.log.')
        result = verify(data)
        with LOCK:
            STATE.update(status='verified', verification=result)
    except Exception as exc:
        with LOCK:
            STATE.update(status='failed', error=str(exc), verification=None)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_):
        pass

    def send(self, status, body, mime='application/json; charset=utf-8'):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False).encode('utf-8')
        elif isinstance(body, str):
            body = body.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', mime)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        self.wfile.write(body)

    def valid_host(self):
        return self.headers.get('Host') in {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}

    def do_GET(self):
        if not self.valid_host():
            return self.send(403, {'error': 'Only local host addresses are accepted.'})
        route = unquote(urlparse(self.path).path)
        if route == '/':
            return self.send(200, (ROOT/'ui/index.html').read_bytes(), 'text/html; charset=utf-8')
        if route == '/api/state':
            with LOCK:
                snapshot = json.loads(json.dumps(STATE))
            snapshot.update(token=TOKEN, default_data=default_data(), project=str(ROOT))
            return self.send(200, snapshot)
        if route.startswith('/reports/'):
            name = route[len('/reports/'):]
            if name not in {'table2_notes.md', 'figure1_notes.md', 'table3_notes.md', 'table4_notes.md', 'ownership_notes.md'}:
                return self.send(404, {'error': 'Stage notes not found.'})
            return self.send(200, (ROOT/'ui/reports'/name).read_bytes(), 'text/plain; charset=utf-8')
        if route.startswith('/results/'):
            name = route[len('/results/'):]
            if name not in FILES or not (ROOT/'results'/name).is_file():
                return self.send(404, {'error': 'File not found or not in the aggregate output allowlist.'})
            mime = mimetypes.guess_type(name)[0] or 'application/octet-stream'
            if name.endswith(('.csv', '.md', '.json')):
                mime = 'text/plain; charset=utf-8'
            return self.send(200, (ROOT/'results'/name).read_bytes(), mime)
        return self.send(404, {'error': 'Page not found.'})

    def do_POST(self):
        origin = self.headers.get('Origin')
        allowed = {f'http://127.0.0.1:{self.server.server_port}', f'http://localhost:{self.server.server_port}'}
        if not self.valid_host() or (origin and origin not in allowed) or self.headers.get('X-Workflow-Token') != TOKEN:
            return self.send(403, {'error': 'The request must come from the local operation page.'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 < length <= 2_000_000:
                raise ValueError('Choose a course CSV smaller than 2 MB.')
            body = self.rfile.read(length)
            route = urlparse(self.path).path
            if route == '/api/upload':
                # Browser-selected input is kept locally, under Git-ignored logs.
                folder = ROOT/'logs/ui_inputs'/uuid.uuid4().hex
                folder.mkdir(parents=True)
                target = folder/'public.csv'
                target.write_bytes(body)
                return self.send(200, {'data': str(target)})
            if route not in ('/api/run', '/api/verify'):
                return self.send(404, {'error': 'Unknown operation.'})
            request = json.loads(body)
            data = Path(request.get('data', '')).expanduser()
            if not data.is_absolute():
                raise ValueError('Enter the full CSV path or use Choose CSV file.')
            data = data.resolve()
            if not data.is_file() or data.suffix.lower() != '.csv':
                raise ValueError('CSV file not found. Check the path or choose the file again.')
            with LOCK:
                if STATE['status'] == 'running':
                    return self.send(409, {'error': 'A task is already running. Wait for it to finish.'})
                STATE.update(status='running', lines=[], verification=None, error=None, data=str(data))
            threading.Thread(target=execute, args=(data, route == '/api/verify'), daemon=True).start()
            return self.send(202, {'status': 'running'})
        except Exception as exc:
            return self.send(400, {'error': str(exc)})


class LocalServer(ThreadingHTTPServer):
    allow_reuse_address = False

    def server_bind(self):
        if sys.platform == 'win32':
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        super().server_bind()


def main():
    parser = argparse.ArgumentParser(description='Open the local minimum wage analysis page')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    try:
        server = LocalServer(('127.0.0.1', args.port), Handler)
    except OSError:
        print('The page port is in use. Close the existing service or choose another port with --port.')
        return 1
    address = f'http://127.0.0.1:{server.server_port}'
    print(f'Local workflow page: {address}', flush=True)
    print('Keep this terminal open. Press Ctrl+C to stop.', flush=True)
    if not args.no_browser:
        webbrowser.open(address)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
