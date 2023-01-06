# Accessing files from git repo for processing

from github import Github
import os
from pprint import pprint
import glob

# clones and returns files of a certain extension from github repo
def GetFiles():
    token = os.getenv('GITHUB_TOKEN', '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')
    g = Github(token)
    repo = g.get_repo("spanninglabs/spanning")
    issues = repo.get_issues(state="open")
    pprint(issues.get_page(0)[1].number)    # getting the latest issue number

    # clone repo
    cmd = "git clone {}".format(repo.ssh_url)
    print("Starting to clone {}".format(repo.name))
    print("Running command '{}'".format(cmd))
    os.system(cmd)
    print("Finished cloning {}".format(repo.name))
    print("---------------------------------")
    print('\n')

    # now go through all files and collect file types we want to use (currently .sol)
    files = glob.glob('spanning' + '/**/*.sol', recursive=True)
    print(files[0])

files = GetFiles()


