#!/usr/bin/env python3
import git
from utils.git_utils import find_git_root
from utils.cli_utils import get_yes_or_no
from utils.general_utils import DictToObject, readArrayEnvVar
import os
import argparse
import sys
sys.path.append('~/.config/doom/scripts')
from git_switch_to_branch import main as switch_to_branch

USERNAME = os.environ["USERNAME"]

def main(script_args=None):
    parser = argparse.ArgumentParser()
    #0. As an arg, we can specify if we want this branch to come out of the current branch, or FROM main
    parser.add_argument("--useCurrentBranch", help="Create the branch from the current branch", action="store_true")
    #1. If JIRA was provided, incorporate it into the ticket name
    parser.add_argument("--jira_issue", type=str, help="Jira Issue ID")

    parser.add_argument("--dir", type=str, help="If defined, look from this directory")
    args = DictToObject(**script_args) if (script_args != None) else parser.parse_args()

    if (args.jira_issue == None):
        print("WARNING: Creating git branch without associated JIRA ticket.")

    branchExists = get_yes_or_no("Does a branch already exist?")

    if (branchExists == 'y'):
        branch_name = input("Branch Name: ")
        #TODO: validate branch existance

        print("printing...")

        #Output the name of the branch
        print(branch_name)
        return

    directory = args.dir if (args.dir != None) else os.getcwd()
    print("Attempting to create branch from: " + str(directory))

    branch_name = input("Enter branch name (will include issue ticket in name!): ")

    repo = git.Repo(directory, search_parent_directories=True)
    current_branch = str(repo.active_branch)

    #if useCurrentBranch isn't true, checkout to main first
    if (args.useCurrentBranch != True):
        switch_to_branch({"target_branch": "main", "dir": args.dir})

    #create the branch
    issueSection = f"{args.jira_issue}--" if (args.jira_issue != None) else ""
    finalName = f"{USERNAME}/{issueSection}{branch_name}"
    repo.git.branch(finalName)

    #4. Also create a symbolic ref to make it easier to switch to on the terminal
    repo.git.symbolic_ref(f"refs/heads/{branch_name}", f"refs/heads/{finalName}")

    #if doing it from main, switch back to the original branch
    if (args.useCurrentBranch != True):
        switch_to_branch({"target_branch": current_branch, "dir": args.dir})

    #Output the name of the branch
    print(finalName)

if __name__ == "__main__":
    main()
