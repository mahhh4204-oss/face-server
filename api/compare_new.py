from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse

FACE_KEY    = 'Px5XFD780ms_LyhqYFDwtAdEE7acyG67'
FACE_SECRET = 'i_51i3D7FgruSn6eqgk8ROXMc_saXKsh'
FACE_URL    = 'https://api-us.faceplusplus.com/facepp/v3/compare'

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

            image1 = body.get('image1', '')
            image2 = body.get('image2', '')

            if not image1 or not image2:
                self._respond(400, {'success': False, 'message': 'image1 aur image2 chahiye'})
                return

            data = urllib.parse.urlencode({
                'api_key'        : FACE_KEY,
                'api_secret'     : FACE_SECRET,
                'image_base64_1' : image1.split(',')[-1],
                'image_base64_2' : image2.split(',')[-1],
            }).encode()

            req = urllib.request.Request(
                FACE_URL,
                data=data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            result = json.loads(urllib.request.urlopen(req, timeout=10).read())
            score = result.get('confidence', 0)

            self._respond(200, {'success': True, 'score': round(score, 1)})

        except Exception as e:
            self._respond(500, {'success': False, 'score': 0, 'message': str(e)})

    def _respond(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass
      
