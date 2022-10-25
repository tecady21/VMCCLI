from datetime import datetime

import requests

COURSES_URL = "https://vmchecker.cs.pub.ro/services/services.py/getCourses"
ASSIGNMENTS_URL = "https://vmchecker.cs.pub.ro/services/services.py/getAssignments?courseId="
RESULTS_URL_1 = "https://vmchecker.cs.pub.ro/services/services.py/getResults?courseId="
RESULTS_URL_2 = "&assignmentId="


def make_assignments_url(course_id):
    return ASSIGNMENTS_URL + course_id


def make_result_url(course_id, assignment_id):
    return RESULTS_URL_1 + course_id + RESULTS_URL_2 + assignment_id


def list_courses(args, cookie):
    headers = {'Cookie': cookie}
    courses_request = requests.get(COURSES_URL, headers=headers)
    courses = courses_request.json()

    if len(courses) == 0:
        print("No courses returned!")
        return

    match = False

    if args.course_id is None and args.title is None:
        print("{:<5}  {:<30}".format("ID", "Title"))

        for course in courses:
            print("{:<5}  {:<30}".format(course["id"], course["title"]))
    else:
        for course in courses:
            if (args.course_id is not None and args.course_id in course["id"]) or (
                    args.title is not None and args.title in course["title"]):
                match = True
                break

        if match is False:
            print("No match found!")
            return

        print("{:<5}  {:<30}".format("ID", "Title"))

        for course in courses:
            # Searching for matching results by course_id and/or title
            if (args.course_id is not None and args.course_id in course["id"]) or (
                    args.title is not None and args.title in course["title"]):
                print("{:<5}  {:<30}".format(course["id"], course["title"]))


def list_assignments(args, cookie):
    assignments_url = make_assignments_url(args.course_id)
    headers = {'Cookie': cookie}

    assignments_request = requests.get(assignments_url, headers=headers)
    assignments = assignments_request.json()

    if type(assignments) is dict:
        print("Wrong course id!")
        return

    if len(assignments) == 0:
        print("No assignments yet!")
        return

    # Finding max length of assignmentId and assignmentTitle for a more readable format
    max_id = 0
    max_title = 0

    for assignment in assignments:
        if len(assignment["assignmentId"]) > max_id:
            max_id = len(assignment["assignmentId"])

        if len(assignment["assignmentTitle"]) > max_title:
            max_title = len(assignment["assignmentTitle"])

    format_string = "{:<" + str(max_id + 2) + "}  {:<" + str(max_title + 2) + "}  {:<15}"

    print(format_string.format("ID", "Title", "Deadline"))
    for assignment in assignments:
        date = datetime.strptime(assignment["deadline"], "%Y.%m.%d %H:%M:%S").strftime("%d.%m.%Y %H:%M")

        print(format_string.format(assignment["assignmentId"], assignment["assignmentTitle"],
                                   date))


def list_results(args, cookie):
    results_url = make_result_url(args.course_id, args.assignment)

    headers = {'Cookie': cookie}
    results_request = requests.get(results_url, headers=headers)

    results_json = results_request.json()

    for entry in results_json:
        for content in entry:
            print('\033[1m' + content + "\n")
            print(entry[content])
            print("-" * 50)

    return
