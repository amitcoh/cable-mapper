import uuid
from graphdb import db
from general import json_to_properties, log

class Rack(object):
    @staticmethod
    def create(name, site, building, room):
        json_props = dict(
            id = uuid.uuid4(),
            name=name,
            site=site,
            building=building,
            room=room
        )
        props = json_to_properties(json_props)
        return db.run("CREATE (a:Rack {}) RETURN a".format(props)).evaluate()
    
    @staticmethod
    def find_one(by_id=None, by_name=None):
        props_json = {}
        if by_id:
            props_json["id"] = by_id
        if by_name:
            props_json["name"] = by_name
        props = json_to_properties(props_json)
        return db.run("MATCH (a:Rack {}) RETURN a".format(props)).evaluate()
    
    @staticmethod
    def find(by_id=None, by_name=None, by_site=None, by_building=None, by_room=None):
        props_json = {}
        if by_id:
            props_json["id"] = by_id
        if by_name:
            props_json["name"] = by_name
        if by_site:
            props_json["site"] = by_site
        if by_building:
            props_json["building"] = by_building
        if by_room:
            props_json["room"] = by_room
        props = json_to_properties(props_json)
        r = db.run("MATCH (a:Rack {}) RETURN a".format(props)).data()
        return [i["a"] for i in r]

    @staticmethod
    def update(rack_id=None, name=None, site=None, building=None, room=None):
        if rack_id:
            if not Rack.find_one(by_id=rack_id):
                log("Rack not found")
                return False
            props = []
            if name:
                props.append("a.name=\"{}\"".format(name))
            if site:
                props.append("a.site=\"{}\"".format(site))
            if building:
                props.append("a.building=\"{}\"".format(building))
            if room:
                props.append("a.room=\"{}\"".format(room))
            props_str = ", ".join(props)
            cypher_query = "MATCH (a: Rack { id: \"" + str(rack_id) + "\"}" + ") SET {} RETURN a".format(props_str)
            return db.run(cypher_query).evaluate()
        log("Must provide rack id")
        return False

    @staticmethod
    def delete(by_id=None, by_name=None):
        props_json = {}
        if by_id:
            props_json["id"] = by_id
        if by_name:
            props_json["name"] = by_name
        props = json_to_properties(props_json)
        db.run("MATCH (a:Rack {}) DETACH DELETE a".format(props)).evaluate()
        return True

    @staticmethod
    def get_all_racks():
        racks = db.run("MATCH (a:Rack) RETURN a.name, a.id").data()
        return [{x["a.id"]: x["a.name"]} for x in racks if x["a.id"]]