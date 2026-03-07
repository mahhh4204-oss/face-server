from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse
import random

FAST2SMS_KEY = 'c7vqZWIAUo6tHSYJXLe83OlmzPKxg52dTs0ipay9GkFEhwrQMNh8m5FlMHfSsqtETC4nQIGjJV9DwW7z'

# Simple in-memory OTP store (resets on server restart — thoda sa limitation)
otp_store = {}

class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length))
            action = body.get('action', '')
            mobile = body.get('mobile', '')

            if not mobile or len(mobile) != 10:
                self._respond(400, {'success': False, 'message': '10 digit mobile chahiye'})
                return

            # ── SEND OTP ──
            if action == 'send':
                otp = str(random.randint(100000, 999999))
                import time
                otp_store[mobile] = {'otp': otp, 'expiry': time.time() + 600}  # 10 min

                url = (
                    'https://www.fast2sms.com/dev/bulkV2'
                    '?authorization=' + FAST2SMS_KEY +
                    '&route=otp'
                    '&variables_values=' + otp +
                    '&flash=0'
                    '&numbers=' + mobile
                )
                req = urllib.request.Request(url, headers={'cache-control': 'no-cache'})
                result = json.loads(urllib.request.urlopen(req, timeout=10).read())

                if result.get('return') == True:
                    self._respond(200, {'success': True, 'message': 'OTP bheja gaya!'})
                else:
                    self._respond(200, {'success': False, 'message': result.get('message', 'Failed')})

            # ── VERIFY OTP ──
            elif action == 'verify':
                entered = body.get('otp', '')
                import time
                stored = otp_store.get(mobile)

                if not stored:
                    self._respond(200, {'success': False, 'message': 'Pehle OTP bhejo!'})
                    return

                if time.time() > stored['expiry']:
                    del otp_store[mobile]
                    self._respond(200, {'success': False, 'message': 'OTP expire ho gaya — dobara bhejo'})
                    return

                if entered == stored['otp']:
                    del otp_store[mobile]
                    self._respond(200, {'success': True, 'message': 'Mobile verified!'})
                else:
                    self._respond(200, {'success': False, 'message': 'Galat OTP — dobara daalo'})

            else:
                self._respond(400, {'success': False, 'message': 'Invalid action'})

        except Exception as e:
            self._respond(500, {'success': False, 'message': str(e)})

    def _respond(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass
