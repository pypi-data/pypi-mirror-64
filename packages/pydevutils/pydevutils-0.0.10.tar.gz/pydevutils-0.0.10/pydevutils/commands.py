import sys
import os
import shutil
import github 
import argparse
from pathlib import Path

try:
    from pydevutils import wingdbstub
except Exception as e:
    print('Failed to load wingdbstub. Wing debugging will not be available')

from pydevutils.gittools import GitHubRepo


def bump_package_patch_version():
    """
    Updates the VERSION=a.x.y patch version in the setup.py found 
    in the current directory. 
    """
    
    package_dir = os.getcwd()
    setup_filename = Path(package_dir, "setup.py")    
    tmp_setup_filename = Path(package_dir, "setup.py.tmp")
    
    try:
        setup_file = open(setup_filename, "r+")
    except FileNotFoundError as e:
        print("Could not read setup.py in current dir: {}".format(setup_filename))
        sys.exit(1)
    
    
    lines = setup_file.readlines()
    
    tmp_setup_file = open(tmp_setup_filename, "w")
    
    for line in lines:
        line = line.strip("\n")
        if line.startswith("VERSION"):
            xyz_version = line.strip("\"").split("=")[1]
            x,y, patch_version = xyz_version.split(".")
            new_patch_versrion = int(patch_version)+1
            new_version_line = "VERSION={}.{}.{}\"".format(x,y,new_patch_versrion)
            line = new_version_line
        #print(line)
        tmp_setup_file.write(line+"\n")
        
    tmp_setup_file.close()
    setup_file.close()
        
    shutil.move(tmp_setup_filename,setup_filename)
        
    
def getcwd_name():
    
    cwd = os.getcwd()
    return Path(cwd).name    

    
def make_github_repo():
    
    description = """Creates a github repo. If local repo does not exist 
    then it is also created. If local repo already exists then local repo is 
    updated to set its origin to the newly created github repo.
    
    This tool helps to quickly push a local repo to github. Saves time from 
    having to interact with the github web page to create a new repo. 
    """
    help_text1 = "The github name for the repo. Defaults to directory name."
    help_text2 = "The path of the local repo. Defaults to searching current and parent directories for .git"

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('name', nargs="?", default=getcwd_name(), help=help_text1)
    parser.add_argument('--path', action="store",dest="path", default=os.getcwd(), help=help_text2)
    
    args = parser.parse_args()    
    gr = GitHubRepo(path=args.path, name=args.name)
    
    local_repo, created = gr.make_repo()
    
    if created:
        print("Created local repo {}".format(args.path))
    else:
        print("Repo already exists. Skipping creation")
        
    print("Creating github repo: {} from local path: {}".format(args.name, args.path))
    
    try:
        repo = gr.make_github_repo()
    
        print("Setting origin to {}".format(repo.ssh_url))
        remote = gr.local_repo.create_remote("origin", repo.ssh_url)
    
    
    except github.GithubException as e:
        if e.status == 422: # Repository Exists
            print("Repository exists")
            
            
        
if __name__ == "__main__":
    
    make_github_repo()