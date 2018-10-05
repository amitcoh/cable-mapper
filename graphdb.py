from py2neo import Graph
from conf import neodb

db = Graph(host=neodb["host"], password=neodb["passw"])

if __name__ == "__main__":
    pass
    