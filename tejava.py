from flask import Flask, jsonify, g
from flask import request, Response, redirect

import endpoints.caltrain_api as caltrain
import endpoints.tejava_api as tejava

app = Flask(__name__)
app.register_blueprint(caltrain.api_blueprint, url_prefix="/caltrain")
app.register_blueprint(tejava.api_blueprint, url_prefix="/tejava")


@app.route("/helloworld")
def helloworld():
    return "hello world!!!!!!"



