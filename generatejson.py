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

#returneaza numarul erorilor continutului fisierului introdus
def get_errors(file_content):
    parts = file_content.split("*************************************************************************************")
    part = parts[1].split()
    noerrors = part[3]
    return noerrors

#returneaza simtime-ul continutului fisierului introdus
def get_simtimefile(file_content):
    parts = file_content.split("*************************************************************************************")
    part = parts[2].split()
    simtimefile = part[4]
    return simtimefile

#returneaza realtime-ul continutului fisierului introdus
def get_realtimefile(file_content):
    parts = file_content.split("*************************************************************************************")
    part = parts[2].split()
    realtimefile = part[11]
    return realtimefile
    

#returneaza numele autorului continutului fisierului introdus
def get_autorsname(file_content):
    lines = file_content.split('\n')
    words = lines[2].split()
    autorsname = words[2]
    return autorsname

#returneaza numele testului sau None pentru prima linie din fisier
def get_testname(part_tests, autorsname):
    words = part_tests.split()
    testname = words[2]    
    if testname.split(".")[0] != autorsname:
        return testname

#returneaza o lista cu status testelor dintr-un fisier
def get_testsstatus(file_content):
    testsstatuslist = []
    justneededpart = file_content.split("********************************************************************************")[2]
    lines = justneededpart.split('\n')
    for line in lines:
        words = line.split()
        if len(words) == 7:
            testsstatuslist.append(words[2])
    return testsstatuslist

#returneaza o lista cu simtime-ul testelor dintr-un fisier
def get_testssimtime(file_content):
    testssimtimelist = []
    justneededpart = file_content.split("********************************************************************************")[2]
    lines = justneededpart.split('\n')
    for line in lines:
        words = line.split()
        if len(words) == 7:
            testssimtimelist.append(words[3])
    return testssimtimelist

#returneaza o lista cu realtime-ul testelor dintr-un fisier
def get_testsrealtime(file_content):
    testsrealtimelist = []
    justneededpart = file_content.split("********************************************************************************")[2]
    lines = justneededpart.split('\n')
    for line in lines:
        words = line.split()
        if len(words) == 7:
            testsrealtimelist.append(words[4])
    return testsrealtimelist




def get_logline(part_tests):
    return part_tests
 

def get_listjson(path):
    filename_list = os.listdir(path)
    testsrun = []
    filetestname = []
    filetests = []
    errorsfile = []
    simtimefile = []
    realtimefile = []
    listjson = []
 
    for file in filename_list:
        if file.endswith(".txt"):
            stem = get_filename(file, path)
            file_to_open = Path(path) / file
            with open(file_to_open, "r") as file:
                file_content = file.read()
            filetestname.append(stem)
            errorsfile.append(get_errors(file_content))
            simtimefile.append(get_simtimefile(file_content))
            realtimefile.append(get_realtimefile(file_content))
            # file_to_write = stem + ".json"
            tests = []
            testsname = []
            testslogline = []
            
            autorsname = get_autorsname(file_content)

            justneededpart = file_content.split("tests")
            lineslist = justneededpart[0].split('\n')
            logline = ""
            startedwriting = 0
            for line in lineslist:
                parts = line.split()
                if len(parts)>6 and parts[6] == "Running":
                    logline = parts[3] + " " + parts[4] + " " + parts[5] + " " + parts[6] + " " + parts[7] + " " + parts[8] + " " + parts[9] + '\n'
                    startedwriting = 1
                if startedwriting == 1 and len(parts)>1 :
                    logline = logline + " "
            testparts = justneededpart[0].split("Running")
            for eachtestpart in testparts:
                if get_testname(eachtestpart, autorsname) != None:
                    testsname.append(get_testname(eachtestpart, autorsname))
                    testslogline.append("a ")
            testsstatus = get_testsstatus(file_content)
            testssimtime = get_testssimtime(file_content)
            testsrealtime = get_testsrealtime(file_content)
            
            for testname, teststatus, testsimtime, testrealtime, testlogline in zip(testsname, testsstatus, testssimtime, testsrealtime, testslogline):
                test = Tests(testname, teststatus, testsimtime, testrealtime, testlogline)
                tests.append(test)
            filetests.append(tests)
    
    for name, testlist, errors, simtime, realtime in zip(filetestname, filetests, errorsfile, simtimefile, realtimefile):
        testrun = TestRuns(name, testlist, errors, simtime, realtime)
        testsrun.append(testrun)
    
    for testrun in testsrun:
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
    return json.loads(json_output)

path ="C://Users//laris//OneDrive//Desktop//AMD//Proiect//Teste"
json_output = get_listjson(path)
output_json_file = "output5.json"

# Write the JSON content to the output file
with open(output_json_file, "w") as outfile:
    json.dump(json_output, outfile, indent=4) 