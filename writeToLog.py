import os

def writeToLog(logs_date_path, logging_details):
    with open(os.path.join(logs_date_path, "logs.txt"), "a") as fp:
        fp.write(logging_details + "\n")