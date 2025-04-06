from ossfuzz_tooling import query
import json
import argparse

def helper_parse() -> str:
    print("No project name provided.")
    print("Here are some available projects:\n")

    # List projects
    all_projects = query.list_projects()
    for proj in all_projects[:20]:  # Show a subset
        print(f"  - {proj}")

    print("\nType the project name to view its crashes, or type 'exit' to cancel.")
    project = input("Project name: ").strip()
    return project

def main():

    parser = argparse.ArgumentParser(description="OSS-Fuzz Tooling CLI")
    subparsers = parser.add_subparsers(dest="command")

    # list-projects
    parser_projects = subparsers.add_parser("list-projects")

    # get-project-info
    parser_info = subparsers.add_parser("get-project-info")
    parser_info.add_argument("project", help="OSS-Fuzz project name")

    # list-crashes
    parser_crashes = subparsers.add_parser("list-crashes")
    parser_crashes.add_argument("project", nargs="?", default=None, help="OSS-Fuzz project name")
    
    # get-fuzzers
    parser_fuzzers = subparsers.add_parser("get-fuzzers")
    parser_fuzzers.add_argument("project", nargs="?", default=None, help="OSS-Fuzz project name")

    # get-coverage
    parser_coverage = subparsers.add_parser("get-coverage")
    parser_coverage.add_argument("project", nargs="?", default=None, help="OSS-Fuzz project name")

    args = parser.parse_args()

    if args.command == "list-projects":
        projects = query.list_projects()
        print(json.dumps(projects, indent=2))
        sample = projects[0]
        info = query.get_project_info(sample)
        print(f"Found {len(projects)} projects.")
        print(f"\nSample project: {sample}")
        print(json.dumps(info, indent=2))

    elif args.command == "get-project-info":
        print("Printing available info for project " + args.project + ":")
        print(json.dumps(query.get_project_info(args.project), indent=2))

    elif args.command == "list-crashes":
        project = args.project
        while not project:
            project = helper_parse()

        if project.lower() == "exit":
            print("Exiting.")
            return
        crashes = query.list_crashes(project)
        print(json.dumps(crashes, indent=2))

    elif args.command == "get-fuzzers":
        project = args.project
        while not project:
            project = helper_parse()

        if project.lower() == "exit":
            print("Exiting.")
            return
        
        fuzzers = query.get_fuzzers(project)
        print(json.dumps(fuzzers, indent=2))

    elif args.command =="get-coverage":
        project = args.project
        while not project:
            project = helper_parse()

        if project.lower() == "exit":
            print("Exiting.")
            return
        coverage = query.get_coverage(project)
        print(json.dumps(coverage, indent=2))


    # projects = query.list_projects()
    # print(f"Found {len(projects)} projects.")
    
    # sample = projects[0]
    # info = query.get_project_info(sample)
    # print(f"\nSample project: {sample}")
    # print(json.dumps(info, indent=2))

if __name__ == "__main__":
    main()