import json
import os
from pathlib import Path
from json import JSONEncoder
from typing import Any


class TestRuns:
    def __init__(self, filename, tests, errors, simtimefile, realtimefile):
        self.filename = filename
        self.tests = tests
        self.errors = errors
        self.simtimefile = simtimefile
        self.realtimefile = realtimefile

class Tests:
    def __init__(self, testname, status, simtime, realtime, logline):
        self.testname = testname
        self.status = status
        self.simtime = simtime
        self.realtime = realtime
        self.logline = logline

class TestRunsEncoder (JSONEncoder):
    def default(self, o):
        return o.__dict__

#returneaza numele fiecarui fisier
def get_filename(file, path):
    file_path = Path(path) / file  # Create a Path object for the file
    return Path(file_path).stem

def get_logline(line):
    parts = line.split()
    if parts[0] == "Description:":
        return 0
    return 1

def get_errors(line):
    parts = line.split()
    if parts[1] == "ERRORS":
        return parts[3]

def get_simtimefile(line):
    parts = line.split()
    if parts[1] == "SIM" and parts[2] == "TIME":
        return parts[4]
    
def get_realtimefile(line):
    parts = line.split()
    if parts[1] == "REAL" and parts[2] == "TIME":
        return parts[4]

def get_listjson(path):
    filename_list = os.listdir(path)
    listjson = []
    testruns = []
    filetestruns = []
    for file in filename_list:
        if file.endswith(".txt"):
            stem = get_filename(file, path)
            file_to_open = Path(path) / file
            tests = []
            testnames=[]
            statuss = []
            simtimes =[]
            realtimes = []
            loglines = []
            with open(file_to_open, "r") as file:
                file_content = file.read()
            components = file_content.split("tests")
            completeloglines = ""
            it = components[0].split('\n')
            logline = ""
            writing = 0
            for each in it:
                logline = ""
                parts = each.split()
                if len(parts)>6 and parts[6] == "Running":
                    logline = parts[3]+" "+parts[4]+" "+parts[5]+" "+parts[6]+" "+parts[7]+" "+parts[8]+" "+parts[9]+'\n'
                    writing = 1
                if writing == 1 and len(parts) > 1:
                    if parts[1] == "INFO":
                        for a in parts:
                              if parts.index(a) > 2:
                                logline = logline + a + " "
                    else:
                        for a in parts:
                            logline = logline + a + " "
                    completeloglines = completeloglines + logline + '\n'
                if len(parts)>7 and parts[7] == "Passed:":
                    writing = 0
                    loglines.append(completeloglines)
            components = file_content.split('"')
            for it in components:
                elements = it.split()
                if len(elements) == 1:
                    testnames.append(elements[0])
            components = file_content.split("** TEST                    PASS/FAIL  SIM TIME(NS)  REAL TIME(S)  RATIO(NS/S) **")
            corectare = components[1].split("********************************************************************************")
            elements = corectare[1].split("\n")
            for element in elements:
                each = element.split()
                if len(each) == 7:
                    statuss.append(each[2])
                    simtimes.append(each[3])
                    realtimes.append(each[4])
            aditional = corectare[3].split()
            errorsfile = aditional[4]
            aditional = corectare[4].split()
            simtimefile = aditional[5]
            realtimefile =aditional[12]
            for testname,status, simtime, realtime, logline in zip(testnames, statuss, simtimes, realtimes, loglines):
                test = Tests(testname, status, simtime, realtime, logline)
                tests.append(test)
            testrun = TestRuns(stem, tests, errorsfile, simtimefile, realtimefile)
            testruns.append(testrun)
        filetestruns.append(testruns)
    
    for file in filetestruns:
        output_testrun = {
            "filename": testrun.filename,
            "tests": [],
            "errors": testrun.errors,
            "simtimefile": testrun.simtimefile,
            "realtimefile": testrun.realtimefile
        }

        for test in testrun.tests:
            output_test = {
                "testname": test.testname,
                "status": test.status,
                "simtime": test.simtime,
                "realtime": test.realtime,
                "logline": test.logline
            }
            output_testrun["tests"].append(output_test)
        listjson.append(output_testrun)
    json_output = TestRunsEncoder().encode(listjson)
    return json_output
    

path ="C://Users//laris//OneDrive//Desktop//AMD//Proiect//Teste"
json_output = get_listjson(path)
# print(json_output)