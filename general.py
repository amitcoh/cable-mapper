import datetime
from graphdb import db

def json_to_properties(json_props):
    r = []
    for prop in json_props:
        if type(json_props[prop]) in [int, float]:
            r.append("{}: {}".format(prop, json_props[prop]))
        else:
            r.append("{}: \"{}\"".format(prop, json_props[prop]))
    return "{ " + ", ".join(r) + " }"

def log(log_meesage):
    msg = "%{}: {}".format(datetime.datetime.now(), log_meesage)
    print msg
    return True

def find_shortest_path(rack1_props_json, rack2_props_json, media_type):
    r1_props_str = json_to_properties(rack1_props_json)
    r2_props_str = json_to_properties(rack2_props_json)
    cypher_query = """
    MATCH (a:Rack {}),(b:Rack {}), path = shortestPath((a)-[:{}*]-(b))  RETURN Nodes(path)
    """.format(r1_props_str, r2_props_str, media_type.upper())
    r = db.run(cypher_query).data()
    return [x["Nodes(path)"] for x in r]

    