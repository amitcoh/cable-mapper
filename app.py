from flask import Flask, request, jsonify, render_template
from panel import Panel
from rack import Rack
from general import find_shortest_path
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

### 
### API Starts Here
###

@app.route('/shortest-path', methods=["GET", "POST"])
def shortest_path():
    if request.method == "GET":
        return jsonify(error="This route should be accessed by POST only."), 400
    if request.method == "POST":
        if request.headers.get('Content-Type', '') == "application/json":
            received_data = request.json
        else:
            received_data = request.form
        r1 = received_data.get("rack1", "")
        r2 = received_data.get("rack2", "")
        media_type = received_data.get("mediaType", "")
        print received_data
        if r1 and r2 and media_type:
            return jsonify(find_shortest_path(r1, r2, media_type))
        return jsonify(error="Could not parse request"), 400


@app.route('/panel', methods=["GET", "POST"])
@app.route('/panel/<id>', methods=["GET", "PUT", "DELETE"])
def panel(id=None):
    if request.method == "GET":
        if id:
            return jsonify(Panel.find(id=id))
        return jsonify(Panel.find())
    if request.method == "POST":
        if request.headers.get('Content-Type', '') == "application/json":
            received_data = request.json
        else:
            received_data = dict(request.form)
            for key in received_data:
                if type(received_data[key]) == list and len(received_data[key]) == 1:
                    received_data[key] = received_data[key][0]
                else:
                    return jsonify(error="Unable to parse json"), 400
        mandatory_fields = ["source_id", "destination_id", "name", "panel_type", "num_of_ports", "connector"]
        if all(elem in received_data.keys()  for elem in mandatory_fields):
            return jsonify(Panel.create(**received_data)), 201
        else:
            return jsonify(error="Mandatory keys are missing",
            mandatory_fields=mandatory_fields
            ), 400
    if request.method == "PUT":
        if request.headers.get('Content-Type', '') == "application/json":
            received_data = request.json
        else:
            received_data = dict(request.form)
            for key in received_data:
                if type(received_data[key]) == list and len(received_data[key]) == 1:
                    received_data[key] = received_data[key][0]
                else:
                    return jsonify(error="Unable to parse json"), 400
        if id:
            return jsonify(Panel.update(id, **received_data))
        return jsonify(error="Must provide panel id for PUT method"), 400
    if request.method == "DELETE":
        if id:
            return jsonify(deleted=Panel.delete(id))


@app.route('/panel/<id>/deactivate')
def deactivate_panel(id):
    return jsonify(Panel.deactivate(id))


@app.route('/panel/<id>/activate')
def activate_panel(id):
    return jsonify(Panel.activate(id))


@app.route('/rack', methods=["GET", "POST"])
@app.route('/rack/<id>', methods = ["GET", "PUT", "DELETE"])
def rack(id=None):
    if request.method == "GET":
        if id:
            return jsonify(Rack.find(by_id=id))
        return jsonify(Rack.free_find())
    if request.method == "POST":
        if request.headers.get('Content-Type', '') == "application/json":
            received_data = request.json
        else:
            received_data = dict(request.form)
            for key in received_data:
                if type(received_data[key]) == list and len(received_data[key]) == 1:
                    received_data[key] = received_data[key][0]
                else:
                    return jsonify(error="Unable to parse json"), 400
        mandatory_fields = ["name", "site", "building", "room"]
        if all(elem in received_data.keys()  for elem in mandatory_fields):
            return jsonify(Rack.create(**received_data)), 201
        else:
            return jsonify(error="Mandatory keys are missing",
            mandatory_fields=mandatory_fields
            ), 400
    if request.method == "PUT":
        if request.headers.get('Content-Type', '') == "application/json":
            received_data = request.json
        else:
            received_data = dict(request.form)
            for key in received_data:
                if type(received_data[key]) == list and len(received_data[key]) == 1:
                    received_data[key] = received_data[key][0]
                else:
                    return jsonify(error="Unable to parse json"), 400
        return jsonify(Rack.update(rack_id=id, 
        name=received_data.get("name", None),
        site=received_data.get("site", None),
        building=received_data.get("building", None),
        room=received_data.get("room", None)
        )), 200
    if request.method == "DELETE":
        if id:
            return jsonify(Rack.delete(by_id=id))
        else:
            return jsonify(error="Must provide ID for DELETE method"), 400

###
### API Ends Here
###

###
### Web FE Starts Here
###



###
### Web FE Ends Here
### 

if __name__ == "__main__":
    app.run(debug=True)