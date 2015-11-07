from flask import Flask, jsonify, g
from flask import request, Response, redirect

import endpoints.caltrain_api as caltrain_api

app = Flask(__name__)
app.register_blueprint(caltrain_api.api_blueprint, url_prefix="/caltrain")


@app.route("/helloworld")
def helloworld():
    return "hello world!!!!!!"



