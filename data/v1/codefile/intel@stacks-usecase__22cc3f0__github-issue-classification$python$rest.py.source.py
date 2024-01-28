#!usr/bin/env python
#
# Copyright (c) 2019 Intel Corporation
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""a rest api for github issue classification"""
import flask
from flask_cors import CORS
from infer import infer

app = flask.Flask("github issue classifier")
CORS(app)

banner = {"what": "github issue classifier",
          "usage": {
              "client": "curl -i -X POST -d '{'issue':'use experimental_jit_scope to enable XLA:CPU.' }' http://localhost:5059/github_issues/infer",
              "server": "docker run -d -p 5000:5000 stacks_img_recog"
          }
          }


@app.route('/github_issues/', methods=["GET"])
def index():
    return flask.jsonify(banner), 201


@app.route('/github_issues/infer', methods=["POST"])
def pred():
    issue = list()
    issue.append(flask.request.json["issue"])
    if not flask.request.json or not "issue" in flask.request.json:
        flask.abort(400)
    labels = infer(issue)
    return flask.jsonify({"label": labels}), 201


@app.errorhandler(404)
def not_found(error):
    return flask.make_response(flask.jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5059)
