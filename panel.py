import uuid
from graphdb import db
from general import json_to_properties, log
from rack import Rack
from py2neo import Relationship

class Panel(object):
    @staticmethod
    def create(source_id, destination_id, name, panel_type, num_of_ports, connector, height=-1):
        source_rack = Rack.find_one(by_id=source_id)
        destination_rack = Rack.find_one(by_id=destination_id)
        if not source_rack:
            log("Source rack not found")
            return False
        if not destination_rack:
            log("Destination rack not found")
            return False
        json_props = dict(
            id=uuid.uuid4(),
            name=name,
            panel_type=panel_type,
            num_of_ports=num_of_ports,
            connector=connector,
            status="active",
            height=height
        )
        source_rack_props = "{ id: \"" + str(source_id) + "\" }"
        destination_rack_props = "{ id: \"" + str(destination_id) + "\" }"
        cypher_query = """
        MATCH (a:Rack {}), (b:Rack {}) CREATE (a)-[c:{} {}]->(b) RETURN c
        """.format(source_rack_props, destination_rack_props, panel_type.upper(), json_to_properties(json_props))
        return db.run(cypher_query).evaluate()

    @staticmethod
    def find_one(**kwargs):
        props = []
        if kwargs:
            for key, value in kwargs.iteritems():
                if type(value) in [int, float]:
                    props.append("r.{}={}".format(key, value))
                else:
                    props.append("r.{}=\"{}\"".format(key, value))
        where_props = " AND ".join(props)
        cypher_query = """
        MATCH ()-[r]->() WHERE {} return r
        """.format(where_props)
        return db.run(cypher_query).evaluate()

    @staticmethod
    def find(**kwargs):
        props = []
        where_props = ""
        if kwargs:
            for key, value in kwargs.iteritems():
                if type(value) in [int, float]:
                    props.append("r.{}={}".format(key, value))
                else:
                    props.append("r.{}=\"{}\"".format(key, value))
            where_props = "WHERE "+ " AND ".join(props)
        cypher_query = """
        MATCH ()-[r]->() {} return r
        """.format(where_props)
        r = db.run(cypher_query).data()
        return [i["r"] for i in r]

    @staticmethod
    def find_all_between_racks(rack1_id, rack2_id):
        if not Rack.find_one(by_id=rack1_id):
            log("Rack 1 not found")
            return False
        if not Rack.find_one(by_id=rack2_id):
            log("Rack 2 not found")
            return False
        cypher_query = """
        MATCH (a)-[r]->(b) WHERE a.id=\"{}\" AND b.id=\"{}\" return r
        """.format(rack1_id, rack2_id)
        r1 = db.run(cypher_query).data()
        cypher_query = """
        MATCH (a)-[r]->(b) WHERE a.id=\"{}\" AND b.id=\"{}\" return r
        """.format(rack2_id, rack1_id)
        r2 = db.run(cypher_query).data()
        if r1 and r2:
            return [i["r"] for i in r1] + [i["r"] for i in r2]
        if r1:
            return [i["r"] for i in r1]
        return [i["r"] for i in r2]

    @staticmethod
    def deactivate(panel_id):
        if Panel.find_one(id=panel_id):
            return db.run("MATCH ()-[r]->() WHERE r.id=\"{}\" SET r.status=\"inactive\" RETURN r".format(panel_id)).evaluate()
        log("Not found")
        return False

    @staticmethod
    def activate(panel_id):
        if Panel.find_one(id=panel_id):
            return db.run("MATCH ()-[r]->() WHERE r.id=\"{}\" SET r.status=\"active\" RETURN r".format(panel_id)).evaluate()
        log("Not found")
        return False

    @staticmethod
    def update(panel_id, **kwargs):
        props = []
        p = Panel.find_one(id=panel_id)
        if not p:
            log("Panel not found")
            return False
        for key, value in kwargs.iteritems():
            if key in dict(p):
                if key == "id":
                    log("Panel id is not changeable")
                    continue
                if type(value) in [int, float]:
                    props.append("r.{}={}".format(key, value))
                else:
                    props.append("r.{}=\"{}\"".format(key, value))
        if props:
            props_str = ", ".join(props)
            cypher_query = """
            MATCH ()-[r]->() WHERE r.id=\"{}\" SET {} RETURN r
            """.format(panel_id, props_str)
            return db.run(cypher_query).evaluate()
        log("No updates were made")
        return False


    @staticmethod
    def delete(panel_id):
        db.run("MATCH ()-[r]->() WHERE r.id=\"{}\" DELETE r".format(panel_id)).evaluate()