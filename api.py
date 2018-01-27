from flask import Flask, request
from flask import send_file
from flask_restful import Resource, Api

import unmark
import urllib

app = Flask(__name__)
api = Api(app)


class BadRequest(Exception):
    status_code = 400
    detail = 'Provide query parameter ?image_url='


class RemoveWatermarkEndpoint(Resource):
    def get(self):
        image_url = request.args.get('image_url')

        if image_url is None:
            raise BadRequest()

        filename = image_url.split("/")[-1]
        urllib.urlretrieve(image_url, filename)
        unmark.unmark(filename)
        return send_file(filename, mimetype='image/png')


api.add_resource(RemoveWatermarkEndpoint, '/unmark')

if __name__ == '__main__':
    app.run(port=5002)
