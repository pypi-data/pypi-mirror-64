from ..protocols import http

DATA = "http://ld.zdb-services.de/data"
RESOURCE = "http://ld.zdb-services.de/resource/"

SCHEMA = ["html", "rdf", "ttl", "jsonld"]


def address(identifier, schema, base):
    # return DATA + identifier + "." + schema
    return "{0}/{1}.{2}".format(base, identifier, schema)


def retrieve(idn, schema, base=DATA):
    url = address(idn, schema, base)
    res = http.get_request(url)
    if schema == "jsonld":
        return http.response_json(res)
    else:
        return res
