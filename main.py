import requests
import json

url = "http://0.0.0.0:8080/api/v1/data"
log_file_path = "log/ereceiver-service.log"
test_cases_path = "test_cases.json"

def check_log_file(test):
    test_status = test["payload"]["status"]
    test_type = test["payload"]["type"]
    test_hash = test["payload"]["hash"]
    search_pattern = f'Input data is not valid: {{"status": "{test_status}", "type": {test_type}, "hash": "{test_hash}"}}'
    with open(log_file_path, "r") as log_file:
        found = any(search_pattern in log_line for log_line in log_file)
        if found:
            return 1
        else:
            return 0

test_cases = []
with open(test_cases_path, "r") as file:
    test_cases = json.load(file)


for test in test_cases:
    try:
        response = requests.post(url, json=test["payload"])
        if response.status_code == test["expected_code"]:
            if test["expected_code"] == 200:
                print(f"[PASSED]: {test["test_case_name"]}")
            else:
                found_in_log = check_log_file(test)
                if found_in_log == 1:
                    print(f"[PASSED]: {test["test_case_name"]}")
                else:
                    print(f"[FAILED]: {test["test_case_name"]} - Error: Test have the same status code, but error was not logged in log file")
        else:
            print(f"[FAILED]: {test["test_case_name"]} - Expected {test["expected_code"]}, got {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"FAILED: {test["test_case_name"]} - Exception occurred: {e}")
