#!/usr/bin/env python3

# Used to copy files from the root repo that go into a release

import argparse
import os.path
from pathlib import Path
import re
import shutil

##
### Helper Functions
##

# build script is in the source root
PATH_SRC = os.path.dirname(os.path.realpath(__file__))

# return build path (useful for main build release script)
def output_path():
  return os.path.join(PATH_SRC, "_out")

# Function to get current commit hash without needing git executable or lib
# Modified version of: https://stackoverflow.com/a/68215738/7572076
def get_commit():
  git_folder = Path(os.path.join(PATH_SRC, '.git'))
  head_content = Path(git_folder, 'HEAD').read_text().split('\n')[0]
  commit_regex = re.compile(r"^[a-fA-F0-9]{40}$")

  # HEAD references another file in ref
  if head_content.startswith("ref: "):
    head_name = head_content.split(' ')[-1]
    head_ref = Path(git_folder,head_name)
    ref_file_content = head_ref.read_text().replace('\n','')

    if re.match(commit_regex, ref_file_content):
      return ref_file_content

  # HEAD has a commit in it (such as for a tag)
  if re.match(commit_regex, head_content):
    return head_content

  return ""


##
#### Build Script
##
def build(git_required):
  # try to get hash
  git_head = get_commit()
  if git_head == "" and git_required:
    print("aborting: failed to get git hash (required by --gitrequired)")
    exit(-1)

  print("copying additional files from certwarden-root")

  if os.path.exists(output_path()):
    print("certwarden-root build output directory already exists, removing it")
    shutil.rmtree(output_path())
  os.makedirs(output_path())

  shutil.copy("README.md", output_path())
  shutil.copy("CHANGELOG.md", output_path())
  shutil.copy("LICENSE.md", output_path())

  # write root HEAD
  if git_head:
    with open(os.path.join(output_path(), "HEAD-root"), "a") as f:
      f.write(git_head)


##
### Main Script
##
def main():
  print("initializing certwarden-root build script")

  # parse args
  parser = argparse.ArgumentParser()
  parser.add_argument('--gitrequired', action='store_true')
  args = parser.parse_args()

  # run build
  build(args.gitrequired)

  print("exiting certwarden-root build script")


# run main if this script is called directly
if __name__ == "__main__":
  main()
