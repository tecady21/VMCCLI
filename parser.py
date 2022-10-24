import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Command line interface to send homeworks to VMChecker")

    subparsers = parser.add_subparsers(help="Option", dest="option", required=False)

    username_parser = subparsers.add_parser("setname", help="Set username to log in")
    username_parser.add_argument("username", help="The username to use when logging in to vmchecker.cs.pub.ro")

    list_parser = subparsers.add_parser("courses", help="List courses.")
    list_parser.add_argument("-i", "--course_id", nargs="?", default=None,
                             help="Course id to be searched. Can be only a part of it.")
    list_parser.add_argument("-t", "--title", nargs="?", default=None,
                             help="Title to be searched. Can be only a part of it.")

    assignments_parser = subparsers.add_parser("assignments", help="List assignments of a course.")
    assignments_parser.add_argument("-i", "--course_id", required=True,
                                    help="The id of the course to list assignments.")

    result_parser = subparsers.add_parser("results", help="Get result of given assignment of a course.")
    result_parser.add_argument("-i", "--course_id", required=True)
    result_parser.add_argument("-a", "--assignment", required=True,
                               help="It needs to be exact assignment name. Use assignments command first to check all assignments of a course.")

    args = parser.parse_args()

    return parser, args
