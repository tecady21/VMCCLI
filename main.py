#!/usr/bin/python3

import list
import parser
import login


def main():
    # Parse arguments
    commands, args = parser.get_args()

    # Setting up username then leaving program
    if args.option == "setname":
        login.set_name(args.username)
        return

    # Get cookie
    cookie = login.login_session()

    if cookie is False:
        commands.print_help()

    if args.option == "courses":
        list.list_courses(args, cookie)
    elif args.option == "assignments":
        list.list_assignments(args, cookie)
    elif args.option == "results":
        list.list_results(args, cookie)


if __name__ == '__main__':
    main()
