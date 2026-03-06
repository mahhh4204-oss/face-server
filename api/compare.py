import json
import urllib.request
import urllib.parse

def handler(request):
    if request.method == 'OPTIONS':
        return Response('', headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type',
        })

    try:
        body = json.loads(request.body)
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

        return Response(
            json.dumps({'success': True, 'score': round(score, 1)}),
            headers={
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            }
        )

    except Exception as e:
        return Response(
            json.dumps({'success': False, 'score': 0, 'error': str(e)}),
            headers={
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            }
      )
      
