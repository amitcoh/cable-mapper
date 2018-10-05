import datetime

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
    