from os import environ
import logging
import requests
import json
import csv
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

def hex_2_str(hex_str: str) -> str:
    return bytes.fromhex(hex_str[2:]).decode("utf-8")

def str_2_hex(str_input: str) -> str:
    return "0x" + str_input.encode("utf-8").hex()

csv_file = "students.csv"

def load_students():
    """Load students from the CSV file into a dictionary."""
    if not os.path.exists(csv_file):
        return {}
    with open(csv_file, mode='r') as infile:
        reader = csv.reader(infile)
        students = {rows[0]: {"courses": json.loads(rows[1])} for rows in reader}
    return students

def save_students(students):
    """Save the students dictionary to the CSV file."""
    with open(csv_file, mode='w') as outfile:
        writer = csv.writer(outfile)
        for email, data in students.items():
            writer.writerow([email, json.dumps(data["courses"])])

students = load_students()

def handle_advance(data):
    logger.info(f"Received advance request data {data}")

    payload = data["payload"]
    message = hex_2_str(payload)
    parts = message.split("|")

    if len(parts) == 2 and parts[0] == "register":
        email = parts[1]
        if email in students:
            report_payload = {"payload": str_2_hex("Email already registered")}
            requests.post(rollup_server + "/report", json=report_payload)
            return "reject"
        students[email] = {"courses": {}}
        save_students(students)
        notice_payload = {"payload": str_2_hex(f"Student {email} registered successfully")}
        requests.post(rollup_server + "/notice", json=notice_payload)

    elif len(parts) == 3 and parts[0] == "add_course":
        email, course_grade = parts[1], parts[2].split(":")
        course, grade = course_grade[0], course_grade[1]
        if email not in students:
            report_payload = {"payload": str_2_hex("Email not registered")}
            requests.post(rollup_server + "/report", json=report_payload)
            return "reject"
        if len(students[email]["courses"]) >= 5:
            report_payload = {"payload": str_2_hex("Cannot add more than 5 courses")}
            requests.post(rollup_server + "/report", json=report_payload)
            return "reject"
        students[email]["courses"][course] = grade
        save_students(students)
        notice_payload = {"payload": str_2_hex(f"Course {course} with grade {grade} added for {email}")}
        requests.post(rollup_server + "/notice", json=notice_payload)

    else:
        report_payload = {"payload": str_2_hex("Invalid message format")}
        requests.post(rollup_server + "/report", json=report_payload)
        return "reject"

    return "accept"

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")

    payload = data["payload"]
    email = hex_2_str(payload)

    if email in students:
        responseObject = json.dumps(students[email])
    else:
        responseObject = json.dumps({"error": "Student not found"})

    report_payload = {"payload": str_2_hex(responseObject)}
    requests.post(rollup_server + "/report", json=report_payload)

    return "accept"

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
