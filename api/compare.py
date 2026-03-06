from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse

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

            API_KEY    = 'Px5XFD780ms_LyhqYFDwtAdEE7acyG67'
            API_SECRET = 'i_51i3D7FgruSn6eqgk8ROXMc_saXKsh'

            data = urllib.parse.urlencode({
                'api_key': API_KEY,
                'api_secret': API_SECRET,
                'image_base64_1': image1.split(',')[-1],
                'image_base64_2': image2.split(',')[-1],
            }).encode()

            req = urllib.request.Request(
                'https://api-us.faceplusplus.com/facepp/v3/compare',
                data=data
            )
            res = urllib.request.urlopen(req, timeout=8)
            result = json.loads(res.read())
            score = result.get('confidence', 0)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'score': round(score, 1)}).encode())

        except Exception as e:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'score': 0, 'error': str(e)}).encode())
            
