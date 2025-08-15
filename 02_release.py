import subprocess
import sys
import os
import shutil
import json

reltype = ""
hostingsite = ""
rootdir = ""


def run_command(command):
    print(f"Running command: {command}")
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print(f"Command '{command}' failed with error:\n{result.stderr}")
        sys.exit(1)
    return result.stdout.strip()


def update_changelog(version):
    print("updating effort")
    effort_hr = 0
    try:
        with open('.timetracker', 'r') as f:
            timetracker_data = json.load(f)
            effort_sec = timetracker_data.get('total', 0)
            effort_hr = effort_sec // 3600
        os.unlink('.timetracker')
    except FileNotFoundError:
        print(".timetracker file not found, skipping effort update.")
    except Exception as e:
        print(f"Error reading .timetracker: {e}")

    print("generate the changelog from git log")
    base_branch = run_command('git merge-base origin/main HEAD')
    logs = run_command(f'git log {base_branch}..HEAD --pretty=%B')
    log_messages = logs.split('\n\n')
    filtered_log_messages = []
    for log_message in log_messages:
        first_line = log_message.split('\n')[0]
        if first_line.startswith("feature:") or first_line.startswith("fix:"):
            filtered_log_messages.append(log_message)
    log_messages = filtered_log_messages
    log_messages.reverse()

    print("write changelog")
    with open('changelog.json', 'r') as file:
        changelog = json.load(file)
        if f"{version}" in changelog.keys():
            effort = changelog[f"{version}"]['effort']
            effort = effort.replace('h', '')
            effort = float(effort) + effort_hr
            changelog[f"{version}"]['effort'] = f"{effort}h"
            for msg in log_messages:
                if msg.startswith("feature:"):
                    clean_msg = msg.replace("feature:", "").strip()
                    if clean_msg not in changelog[f"{version}"]['features']:
                        changelog[f"{version}"]['features'].append(clean_msg)
                elif msg.startswith("fix:"):
                    clean_msg = msg.replace("fix:", "").strip()
                    if clean_msg not in changelog[f"{version}"]['fixes']:
                        changelog[f"{version}"]['fixes'].append(clean_msg)
        else:
            changelog[f"{version}"] = {
                'effort': "",
                'features': [],
                'fixes': []
            }
            changelog[f"{version}"]['effort'] = f"{effort_hr}h"
            for msg in log_messages:
                if msg.startswith("feature:"):
                    clean_msg = msg.replace("feature:", "").strip()
                    changelog[f"{version}"]['features'].append(clean_msg)
                elif msg.startswith("fix:"):
                    clean_msg = msg.replace("fix:", "").strip()
                    changelog[f"{version}"]['fixes'].append(clean_msg)
    # Sort the changelog dictionary by keys in descending order
    changelog = dict(
        sorted(changelog.items(), key=lambda x: x[0], reverse=True))
    with open('changelog.json', 'w') as file:
        json.dump(changelog, file, indent=4)

    print("Testcases refreshing")
    with open('vkhgaruda/test/nitya_seva.md', 'r+') as testspec:
        content = testspec.read()
        testspec.seek(0)
        testspec.write(content.replace("-[x]", "-[]"))
        testspec.truncate()
        # Load the updated changelog
        with open('changelog.json', 'r') as f:
            changelog = json.load(f)

        # Get the first (latest) version's features
        first_version = next(iter(changelog))
        features = changelog[first_version].get('features', [])

        # Read the test spec again to update after "# new features"
        testspec.seek(0)
        content = testspec.read()
        split_marker = "# new features"
        if split_marker in content:
            before, _ = content.split(split_marker, 1)
            new_content = before + split_marker + "\n"
            for feature in features:
                new_content += f"-[] {feature}\n"
            testspec.seek(0)
            testspec.write(new_content)
            testspec.truncate()

def set_parameters():
    global rootdir
    global reltype

    rootdir = run_command('git rev-parse --show-toplevel')

    if len(sys.argv) == 2:
        reltype = sys.argv[1]
    else:
        relid = input("Enter the release type: 1. Release 2. Test ")
        if relid == '1':
            reltype = 'release'
        elif relid == '2':
            reltype = 'test'
        else:
            print("Invalid release type")
            sys.exit(1)
    print(f"Release type: {reltype}")


def set_hosting_site(app):
    global hostingsite
    if (app == 'vkhgaruda' and reltype == 'release'):
        hostingsite = 'vkhillgaruda'
    elif (app == 'vkhgaruda' and reltype == 'test'):
        hostingsite = 'testgaruda'
    elif (app == 'vkhsangeetseva' and reltype == 'release'):
        hostingsite = 'govindasangetseva'
    elif (app == 'vkhsangeetseva' and reltype == 'test'):
        hostingsite = 'testsangeetseva'
    else:
        print("Hosting site could not be determined")
        sys.exit(1)
    print(f"Hosting site: {hostingsite}")


def replace_string_in_file(file, search_string, replacement_string):
    curdir = os.getcwd()
    os.chdir(rootdir)
    with open(file, 'r') as file:
        lines = file.readlines()
    with open(file, 'w') as file:
        for line in lines:
            if search_string in line:
                file.write(replacement_string)
            else:
                file.write(line)
    os.chdir(curdir)


def set_value_in_file(filepath, search_string, value):
    curdir = os.getcwd()
    os.chdir(rootdir)
    with open(filepath, 'r') as file:
        lines = file.readlines()
    with open(filepath, 'w') as file:
        for line in lines:
            if search_string in line:
                if '=' in line:
                    key, _ = line.split('=', 1)
                    file.write(f'{key}={value}\n')
                elif ':' in line:
                    key, _ = line.split(':', 1)
                    file.write(f'{key}: {value}\n')
            else:
                file.write(line)
    os.chdir(curdir)


def get_value_from_file(filepath, search_string):
    ret = ""
    curdir = os.getcwd()
    os.chdir(rootdir)
    with open(filepath, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if line.startswith("#"):
            continue
        if search_string in line:
            if '=' in line:
                _, value = line.split('=', 1)
                ret = value.strip()
                break
            elif ':' in line:
                key, value = line.split(':', 1)
                ret = value.strip()
                break
    return ret
    os.chdir(curdir)


def release():
    os.chdir(rootdir)

    print("get the branch name")
    branch_name = run_command('git rev-parse --abbrev-ref HEAD')
    branch_name = branch_name.lstrip()
    version = branch_name
    update_changelog(version)

    if branch_name != 'main':
        print("commit all changes and push to git")
        if run_command('git status --porcelain'):
            run_command('git add -A')
            if branch_name == "main":
                run_command('git commit -m "post release changes"')
            else:
                run_command(f'git commit -m "release {branch_name}"')
            run_command('git push origin')
            if branch_name != "main" and reltype == 'release':
                run_command('git checkout main')
                run_command('git pull')
                run_command(f'git merge {branch_name}')
                run_command('git push origin')
        else:
            print("No changes to commit")

def main():
    input("Please stop the timetracker if running...")
    set_parameters()
    release()
    print("all operations completed")


if __name__ == '__main__':
    main()
