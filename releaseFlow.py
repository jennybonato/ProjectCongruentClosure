#!/usr/bin/env python
import argparse
import json
import logging
import re
from sys import exit

from bitchangelog.bitchangelog import update_changelog
from git import Git, Repo

RELEASE_TYPES = ['major', 'minor', 'patch']
MASTER = "master"
TESTING = "testing"
RELEASE = "release"

repo = Repo('.')
git = Git()
new_version = ''

'''
    Compute the new version based on the current version and the release type
'''
def compute_new_version(type: str) -> str:

    # Retrieve current version
    current_version = ''
    with open("package.json", "r") as fin:
        current_version = json.load(fin)["version"]

    major, minor, patch = list(map(int, current_version.split(".")))
    if type == "patch":
        patch += 1
    elif type == "minor":
        patch = 0
        minor += 1
    else:
        patch = 0
        minor = 0
        major += 1

    version = ".".join(map(lambda x: str(x).zfill(2), [major, minor, patch]))
    logging.info(f"New version will be {version}")
    return version

'''
    Check if the current branch is the correct branch and if there are no changes
'''
def check_current_branch_status(branch: str) -> bool:
    current_branch = git.branch("--show-current")
    if current_branch.startswith(branch):
        logging.error(f"You must be on {branch} branch, but you are on {current_branch}")
        exit(1)
    if (repo.is_dirty(untracked_files=True)):
        logging.error("Your repo is dirty, please commit or stash your changes")
        exit(1)

def update_version_and_changelog() -> None:
    with open("android/gradle.properties", "r+") as gradle_properties_file:
        file_content = gradle_properties_file.read()
        gradle_properties_file.seek(0)
        gradle_properties_file.write(
            re.sub(r'versionName=.*', f'versionName={new_version}', file_content))
        gradle_properties_file.truncate()

    with open("ios/BIT/Info.plist", "r+") as info_plist_file:
        file_content = info_plist_file.read()
        info_plist_file.seek(0)
        key = "<key>CFBundleShortVersionString</key>"
        info_plist_file.write(re.sub(r'{}\n\t<string>.*</string>'.format(key),
                              f'{key}\n\t<string>{new_version}</string>', file_content))
        info_plist_file.truncate()

    with open("package.json", "r+") as package_json_file:
        data = json.load(package_json_file)
        data["version"] = new_version
        package_json_file.seek(0)
        json.dump(data, package_json_file, indent=2)

    with open("app.json", "r+") as app_json_file:
        data = json.load(app_json_file)
        data["expo"]["version"] = new_version
        app_json_file.seek(0)
        json.dump(data, app_json_file, indent=2)

    update_changelog(new_version)

'''
    Create a new release branch with the given version, commit new changes,
    tag the commit and push the branch and the tag
'''
def commit_and_push_release_branch() -> None:

    if not repo.is_dirty(untracked_files=True):
        logging.warning("Your repo is clean, nothing to commit")
        exit(1)

    git.checkout("-b", f"{RELEASE}/{new_version}")
    git.add(".")
    git.commit("-m", "Update version")
    git.push("origin", f"{RELEASE}/{new_version}")
    git.tag(new_version)
    git.push("origin", new_version) # Push remote tag

def merge_release_branch_into_master() -> None:
    logging.info(f"Do you want to merge {RELEASE}/{new_version} branch into {MASTER}? [y/n]")
    merge = input()

    if merge.lower() in ("y", "yes"):
        git.checkout(MASTER)
        git.merge(f"{RELEASE}/{new_version}", "--no-ff")
        git.push("origin", MASTER)
        git.push("origin", "--delete", f"{RELEASE}/{new_version}")
    else:
        logging.warning("Merge aborted, rollbacking...")
        git.push("origin", "--delete", new_version) # Delete remote tag
        git.tag("-d", new_version)
        git.checkout(TESTING)
        git.push("origin", "--delete", f"{RELEASE}/{new_version}")
        git.branch("-D", f"{RELEASE}/{new_version}")
        exit(1)

def merge_master_into_develop() -> None:
    git.checkout(TESTING)
    git.merge(MASTER, "--no-ff")
    git.push("origin", TESTING)


def prepare_release() -> int:
    logging.info("Starting release flow")

    check_current_branch_status(TESTING)
    update_version_and_changelog()
    commit_and_push_release_branch()

    logging.info("Release prepared")
    exit(0)

def approve_release() -> int:
    logging.info("Approving release")

    check_current_branch_status(RELEASE)
    merge_release_branch_into_master()
    merge_master_into_develop()

    logging.info("Release flow completed")
    exit(0)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Bitapp release flow")
    parser.add_argument("-t", "--type", default="patch",
                        help=f"Release type: {', '.join(RELEASE_TYPES)}", required=False, type=str, dest="type")
    parser.add_argument("-d", "--debug", default=False, help="Debug mode",
                        action="store_true", required=False, dest="debug")
    parser.add_argument("-a", "--approve", default=False, help="Approve release",
                        action="store_true", required=False, dest="approve")
    args = parser.parse_args()

    level = logging.INFO
    if args.debug:
        level = logging.DEBUG
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)6s | %(message)s')

    if str.lower(args.type) not in RELEASE_TYPES:
        logging.error(f"Release type is not valid, choose one of {', '.join(RELEASE_TYPES)}")
        exit(1)

    new_version = compute_new_version(args.type)

    if args.approve:
        approve_release()
    else:
        prepare_release()
