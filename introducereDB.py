import pymongo
import json

class DatabaseLoader:
    def __init__(self, db_url, db_name):
        self.client=pymongo.MongoClient(db_url)
        self.db=self.client[db_name]
        self.tests_collection=self.db["tests"]
        self.testruns_collection=self.db["testruns"]

    def load_from_json(self, json_name):
        with open(json_name) as f:
            data_list=json.load(f)["testruns"]
        
        for data in data_list:
            run_id=data["filename"]

            testruns_data={"run_id":run_id,
                           "run_time":data["realtimefile"],
                           "sim_time":data["simtimefile"],
                           "errors":data["errors"]}
            self.testruns_collection.insert_one(testruns_data)

            for test in data["tests"]:
                test_data={"run_id":run_id,
                           "test_name":test["testname"],
                           "status":test["status"],
                           "run_time":test["realtime"],
                           "sim_time":test["simtime"],
                           "loglines":test["logline"]}
                self.tests_collection.insert_one(test_data)

if __name__=="__main__":
    db_url="mongodb://localhost:27017/"
    db_name="test_bench_database"
    loader=DatabaseLoader(db_url,db_name)
    json_name="test_data.json"
    loader.load_from_json(json_name)