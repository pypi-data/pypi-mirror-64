import requests
import uncurl
import re
import urllib.parse
import pprint
import json
from .requrl import LurlRequest

class TkpStruct(object):

    def __init__(self, curl):
        self.request = LurlRequest(curl)
        self.base = None

    def get_as_tkp(self):
        self.construct()
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.base)
        self.print_to_file()

    def print_to_file(self):
        path_split = self.request.path.split("/")
        path_for_file = ""
        for sub_path in path_split :
            path_for_file = path_for_file + sub_path.capitalize()
        f = open("test_SERVICENAME_"+path_for_file+".json", "w")
        f.write(json.dumps(self.base, indent=4, sort_keys=True))
        f.close()

    def construct(self) :
        self.construct_base()
        self.base["structure"].append(self.get_production_structure())
        self.base["structure"].append(self.get_staging_structure())

    def construct_base(self) :
        self.base = {
            "queryName": self.get_queryName(),
            "serviceName":"REPLACE_TO_SERVICE_NAME",
            "apiName": self.get_apiName(),
            "alertSlackGroup":"@REPLACE_TO_SLACK_GROUP",
            "testCaseDescription": "call " + self.request.path,
            "testCasePriority": "P0 P1 P2 P3 P4",
            "httpMethod":self.request.method,
            "headerMap":self.request.headers,
            "query":"",
            "filterKeys": [],
            "structure": []
        }

    def get_apiName(self):
        api_name = self.request.path
        if len(self.request.query) > 0 :
            get_param_tuple = urllib.parse.parse_qsl(self.request.query)
            get_param_dict = dict()
            for field, value in get_param_tuple :
                get_param_dict[field] = "{" + field + "}"
            api_name = api_name + "?" + "&".join("{}={}".format(*i) for i in get_param_dict.items())
        return api_name
    
    def get_apiParamMap_from_query(self):
        query_tuple = urllib.parse.parse_qsl(self.request.query)
        query_dict = dict((x, y) for x, y in query_tuple)
        return query_dict

    def get_queryName(self):
        return self.request.method + " : " + self.request.path

    def get_variables(self):
        return dict(self.request.parsed.data)

    def get_production_structure(self):
        env_name = "production"
        return self.set_structure(env_name)

    def get_staging_structure(self):
        env_name = "staging"
        return self.set_structure(env_name)
    
    def set_structure(self, env_name) :
        self.request.call()
        structure = { 
            "env":env_name,
            "apiParamMap":self.get_apiParamMap_from_query(),
            "variables": self.get_variables(),
            "responseString":self.request.response_content,
            "responseCode":self.request.response.status_code
        }
        return structure





