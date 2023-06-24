from dirsync import sync
import os
import subprocess

# Define the source and target directories
source = 'C:\\'
target = 'F:\\'

# Define a function to sync two directories using dirsync
def sync_dirs(source, target, action):
    # Try to sync the directories using the given action
    try:
        sync(source, target, action)
        print(f"Successfully synced {source} and {target} using {action}")
    # Handle any exceptions raised by dirsync
    except Exception as e:
        print(f"Failed to sync {source} and {target} using {action}")
        print(f"Error: {e}")

# Define a function to run git commands using subprocess
def run_git_command(command):
    # Try to run the git command as a list of arguments
    try:
        result = subprocess.run(command, capture_output=True, check=True)
        print(f"Successfully ran {' '.join(command)}")
        print(result.stdout.decode())
    # Handle any exceptions raised by subprocess
    except Exception as e:
        print(f"Failed to run {' '.join(command)}")
        print(f"Error: {e}")
# Sync source to target using update action
sync_dirs(source, target, 'update')
# Sync target to source using sync action
# sync_dirs(target, source, 'sync')
# Change the current working directory to the target directory
os.chdir(target)
# Run git commands to add, commit and log changes
run_git_command(['git', 'add', '-A'])
run_git_command(['git', 'commit', '-m', 'Sync files'])
run_git_command(['git', 'log', '-1'])