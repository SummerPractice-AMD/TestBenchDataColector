import json
import os
from pathlib import Path
from json import JSONEncoder
from typing import Any
import uuid


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
    return int(noerrors)

#returneaza simtime-ul continutului fisierului introdus
def get_simtimefile(file_content):
    parts = file_content.split("*************************************************************************************")
    part = parts[2].split()
    simtimefile = part[4]
    return float(simtimefile)

#returneaza realtime-ul continutului fisierului introdus
def get_realtimefile(file_content):
    parts = file_content.split("*************************************************************************************")
    part = parts[2].split()
    realtimefile = part[11]
    return float(realtimefile)
    

#returneaza numele autorului continutului fisierului introdus
def get_autorsname(file_content):
    lines = file_content.split('\n')
    words = lines[2].split()
    autorsname = words[2]
    return autorsname

#returneaza numele testului sau None pentru prima linie din fisier
def get_testname(part_tests):
    autorsname = get_autorsname(part_tests)
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
            testssimtimelist.append(float(words[3]))
    return testssimtimelist

#returneaza o lista cu realtime-ul testelor dintr-un fisier
def get_testsrealtime(file_content):
    testsrealtimelist = []
    justneededpart = file_content.split("********************************************************************************")[2]
    lines = justneededpart.split('\n')
    for line in lines:
        words = line.split()
        if len(words) == 7:
            testsrealtimelist.append(float(words[4]))
    return testsrealtimelist

#returneaza o lista cu logline-urile testelor dintr-un fisier
def get_logline(file_content):
    autorsname = get_autorsname(file_content)
    loglinelist = []
    startwriting = 0
    lines = file_content.split('\n')
    for line in lines:
        words = line.split()
        if len(words) == 10 and words[5] == "execute":
            logline = ""
            startwriting = 1
        if startwriting == 1 :
            if len(words)>2 and words[2].split('.')[0] == autorsname:
                for word in range(3, len(words)):
                    logline = logline + words[word] + " "
                logline = logline + '\n'
            else:
                for word in words:
                    logline = logline + word + " "
                logline = logline + '\n'
        if len(words) == 11 and startwriting == 1 and words[10] == "packets":
            logline = logline + words[3] + " " + words[4] + " " + words[5] + " " + words[6] + " " + words[7] + " " + words[8] + " " + words[9] + " " + words[10] + "\n"
            startwriting = 0
            loglinelist.append(logline)
        if len(words) == 12 and startwriting == 1 and words[7] == "Failed:":
            logline = logline + words[3] + " " + words[4] + " " + words[5] + " " + words[6] + " " + words[7] + " " + words[8] + " " + words[9] + " " + words[10] + " " + words[11] + "\n"
            startwriting = 0
            loglinelist.append(logline)
    return loglinelist


#primeste un string si returneaza un obiect tip Json
def parse(string, filename):
    name = filename
    errors = get_errors(string)
    simtime = get_simtimefile(string)
    realtime = get_realtimefile(string)
    tests = []
    testsname = []
    testslogline = []
    justneededpart = string.split("tests")
    testparts = justneededpart[0].split("Running")
    for eachtestpart in testparts:
        if get_testname(eachtestpart) != None:
            testsname.append(get_testname(eachtestpart))
    testsstatus = get_testsstatus(string)
    testssimtime = get_testssimtime(string)
    testsrealtime = get_testsrealtime(string)
    testslogline = get_logline(string)
            
    for testname, teststatus, testsimtime, testrealtime, testlogline in zip(testsname, testsstatus, testssimtime, testsrealtime, testslogline):
        test = Tests(testname, teststatus, testsimtime, testrealtime, testlogline)
        tests.append(test)

    testrun = TestRuns(name, tests, errors, simtime, realtime)
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
    json_output = TestRunsEncoder().encode(output_testrun)
    return json.loads(json_output)

#primeste un file si returneaza un obiect tip Json
# def parsefile(filename):
#     name = get_filename(filename)
#     with open(file_to_open, "r") as file:
#         file_content = file.read()
#     json_output = parse(file_content)
#     return json_output
    

#returneaza o lista de obiecte json
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

            justneededpart = file_content.split("tests")
            testparts = justneededpart[0].split("Running")
            for eachtestpart in testparts:
                if get_testname(eachtestpart) != None:
                    testsname.append(get_testname(eachtestpart))
            testsstatus = get_testsstatus(file_content)
            testssimtime = get_testssimtime(file_content)
            testsrealtime = get_testsrealtime(file_content)
            testslogline = get_logline(file_content)
            
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
# stem = get_filename(file, path)
file_to_open = Path("C://Users//laris//OneDrive//Desktop//AMD//Proiect//Teste//12.txt")
# file_to_open = Path(path) / file
filename = "12"
with open(file_to_open, "r") as file:
    file_content = file.read()

json_output = parse(file_content, filename)
output_json_file = "output111.json"

# Write the JSON content to the output file
with open(output_json_file, "w") as outfile:
    json.dump(json_output, outfile, indent=4)