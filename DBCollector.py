import argparse
from generatejson import get_listjson
from introducereDB import DatabaseLoader
import json
import yaml

def load_config(config_file):
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    return config

def connect_to_database(config):
    database_host = config["regression_details"]["database_host"]
    database_port = config["regression_details"]["database_port"]
    database_name = config["regression_details"]["database_name"]
    connection_string = "mongodb://" + database_host + ":" + str(database_port)
    return DatabaseLoader(connection_string, database_name)

def parse_command_line():
    parser = argparse.ArgumentParser(description="Collect and load test run data into MongoDB")
    parser.add_argument("--dir", required=True, help="Specify the directory containing test run files")
    #linie de comanda dau file
    return parser.parse_args()

def main():
    args=parse_command_line()
    json_output = get_listjson(args.dir)
    config=load_config("config.yml")
    loader=connect_to_database(config)
    loader.load_from_json(json_output)
    #json_output=get_listjson("C:\\Users\\adina\\Downloads\\regression-runs")
    #json_output=get_listjson("C://Users//adina//Downloads//PracticaAMD-Proiect")
    #output_json_file = "json_data.json"
    #with open(output_json_file, "w") as outfile:
        #json.dump(json_output, outfile, indent=4) 
if __name__ == "__main__":
    main()
