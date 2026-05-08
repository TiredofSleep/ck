"""
ck_sage_remote.py — remote SageMathCell client.

Usage:
    from ck_sage_remote import sage_eval
    out = sage_eval("print(2 + 2); factor(3^10 - 1)")
    print(out['stdout'], out['results'])

Protocol (reverse-engineered from sagecell_client.js):
  1. POST /kernel?CellSessionID=<uuid>&accepted_tos=true
     -> {"ws_url": "wss://.../", "id": "<kernel_id>"}
  2. WS connect to <ws_url>kernel/<kernel_id>/channels
  3. Send Jupyter-style execute_request on shell channel
  4. Collect stream/execute_result/error frames until status:idle matches msg_id

Each call spins up a fresh kernel. For multi-step pipelines, use `SageSession`
which keeps the websocket open and executes multiple requests.
"""
from __future__ import annotations
import json, time, uuid, urllib.request
import websocket  # pip install websocket-client

ENDPOINT = 'https://sagecell.sagemath.org'


def _new_kernel(accept_tos: bool = True):
    cell_id = uuid.uuid4().hex
    url = f'{ENDPOINT}/kernel?CellSessionID={cell_id}&accepted_tos={"true" if accept_tos else "false"}'
    req = urllib.request.Request(
        url, data=b'', method='POST',
        headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        j = json.loads(r.read().decode('utf-8'))
    return cell_id, j['id'], j.get('ws_url', 'wss://sagecell.sagemath.org/')


def _execute_request(session_id: str, code: str) -> tuple[str, dict]:
    msg_id = uuid.uuid4().hex
    msg = {
        'header': {
            'msg_id': msg_id, 'username': 'ck', 'session': session_id,
            'msg_type': 'execute_request', 'version': '5.3',
        },
        'parent_header': {}, 'metadata': {},
        'content': {
            'code': code, 'silent': False, 'store_history': False,
            'user_expressions': {}, 'allow_stdin': False, 'stop_on_error': True,
        },
        'buffers': [], 'channel': 'shell',
    }
    return msg_id, msg


class SageSession:
    """Persistent Sage kernel. Use as context manager."""
    def __init__(self, timeout: float = 60.0, max_idle: float = 300.0):
        self.timeout = timeout
        self.max_idle = max_idle
        self.cell_id = None
        self.kernel_id = None
        self.ws = None

    def __enter__(self):
        self.cell_id, self.kernel_id, ws_url = _new_kernel()
        channel = f"{ws_url.rstrip('/')}/kernel/{self.kernel_id}/channels"
        self.ws = websocket.create_connection(channel, timeout=self.timeout)
        return self

    def __exit__(self, *exc):
        try:
            if self.ws is not None:
                self.ws.close()
        except Exception:
            pass

    def eval(self, code: str, timeout: float | None = None) -> dict:
        """Run `code` in this kernel; return {stdout, stderr, results, errors, elapsed}."""
        if self.ws is None:
            raise RuntimeError('session not open')
        t_limit = timeout if timeout is not None else self.max_idle
        msg_id, msg = _execute_request(self.cell_id, code)
        self.ws.send(json.dumps(msg))

        out = {'stdout': '', 'stderr': '', 'results': [], 'errors': [], 'elapsed': 0.0}
        t0 = time.time()
        self.ws.settimeout(t_limit)
        while True:
            if time.time() - t0 > t_limit:
                out['errors'].append(f'TIMEOUT after {t_limit}s')
                break
            try:
                raw = self.ws.recv()
            except Exception as e:
                out['errors'].append(f'RECV {type(e).__name__}: {e}')
                break
            try:
                m = json.loads(raw)
            except Exception:
                continue
            mt = m.get('header', {}).get('msg_type', '')
            c = m.get('content', {})
            if mt == 'stream':
                name = c.get('name', 'stdout')
                text = c.get('text', '')
                if name == 'stderr':
                    out['stderr'] += text
                else:
                    out['stdout'] += text
            elif mt == 'execute_result':
                out['results'].append(c.get('data', {}))
            elif mt == 'display_data':
                out['results'].append(c.get('data', {}))
            elif mt == 'error':
                out['errors'].append({
                    'ename': c.get('ename'), 'evalue': c.get('evalue'),
                    'traceback': c.get('traceback', []),
                })
            elif mt == 'status':
                if (c.get('execution_state') == 'idle'
                        and m.get('parent_header', {}).get('msg_id') == msg_id):
                    break
        out['elapsed'] = time.time() - t0
        return out


def sage_eval(code: str, timeout: float = 60.0) -> dict:
    """One-shot: spin up a kernel, run code, tear down."""
    with SageSession(timeout=timeout, max_idle=timeout) as s:
        return s.eval(code, timeout=timeout)


def print_errors(r: dict, prefix: str = 'ERR') -> None:
    """Robust error printer: handles both string timeouts and dict exceptions."""
    for e in r.get('errors', []):
        if isinstance(e, str):
            print(f'{prefix} (transport): {e}')
        else:
            ename = e.get('ename', '?')
            evalue = (e.get('evalue') or '')[:800]
            print(f'{prefix} {ename}:: {evalue}')


if __name__ == '__main__':
    # Smoke test
    r = sage_eval('''
print("K =", QQ)
R.<x> = PolynomialRing(QQ)
f = x^5 - 2
print("factor over Q:", factor(f))
K.<a> = NumberField(f)
print("degree:", K.degree())
print("disc:", K.discriminant())
''', timeout=45.0)
    print('STDOUT:')
    print(r['stdout'])
    if r['stderr']:
        print('STDERR:', r['stderr'])
    print_errors(r)
    print(f"elapsed: {r['elapsed']:.2f}s")
