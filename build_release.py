#!/usr/bin/env python3

# Usage
# python3 ./build_release.py `target` [--gitrequired]

# `target` must be in the format: `GOOS_GOARCH`
# see: https://github.com/golang/go/blob/master/src/internal/syslist/syslist.go
# or unofficially: https://gist.github.com/asukakenji/f15ba7e588ac42795f421b48b8aede63
# e.g.,
#  "windows_amd64",
#  "linux_amd64",
#  "linux_arm64",
#  "darwin_amd64",
#  "darwin_arm64",
#  "freebsd_amd64",
#  "freebsd_arm64",

# Assumptions:
# This script and repo source is located in [root]/certwarden
# Backend source is cloned into [root]/certwarden-backend and checked out to the desired tag
# Frontend source is cloned into [root]/certwarden-frontend and checked out to the desired tag

# Build output will be placed in [root]/certwarden/_out


import argparse
import importlib
import os.path
from pathlib import Path
import re
import shutil
import sys
import tarfile

# append parent folder to access other src repo scripts
sys.path.append("..")

build_backend = importlib.import_module("certwarden-backend.build", package="build_backend")
build_frontend = importlib.import_module("certwarden-frontend.build", package="build_frontend")

##
### Helper Functions
##

PATH_SRC = os.path.dirname(os.path.realpath(__file__))

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
### Main Script
##

print("initializing certwarden build script")

# parse args
parser = argparse.ArgumentParser()
parser.add_argument('target')
parser.add_argument('--gitrequired', action='store_true')
args = parser.parse_args()

# get version numbers
# backend
version_string = build_backend.get_backend_version()

# verify frontend matches
fe_ver = build_frontend.get_frontend_version()
if version_string != fe_ver:
  print(f"aborting: backend version {version_string} and frontend version {fe_ver} do not match")
  exit(-1)

# try to get hash for base repo
gitHead = get_commit()
if gitHead == "":
  print("failed to get git hash")
  if args.gitrequired:
    print("aborting: git hash is required by --gitrequired")
    exit(-1)

# validate build target
print(f"build target '{args.target}'")
GOOS, GOARCH = build_backend.parse_os_target(args.target)

# create base out path if it doesn't exist
path_output = os.path.join(PATH_SRC, "_out")
path_output = Path(path_output).resolve()

# create subpath for target
path_target_out = Path(os.path.join(path_output, args.target)).resolve()

if not path_target_out.is_relative_to(path_output):
  print("Security Error: Path traversal attempt detected.")
  exit(-5)

print(f"preparing to build certwarden {version_string} for {args.target}")

if os.path.exists(path_target_out):
  print(f"build output directory '{path_target_out}' already exists, removing it")
  shutil.rmtree(path_target_out)

if not os.path.exists(path_target_out):
  os.makedirs(path_target_out)

# calculate final file and remove any existing completed build
release_file_name = f"certwarden-{version_string}_{args.target}"
for filename in os.listdir(path_output):
  if filename.startswith(release_file_name) and (filename.endswith(".tar.gz") or filename.endswith(".zip")) :
    print(f"build output '{filename}' already exists, removing it")
    os.remove(os.path.join(path_output, filename))


# build backend
print("calling backend build script")
build_backend.build(GOOS, GOARCH, args.gitrequired)

shutil.copytree(build_backend.output_path(), path_target_out, dirs_exist_ok=True)


# build frontend
print("calling frontend build script")
build_frontend.build(args.gitrequired)

shutil.copytree(build_frontend.output_path(), path_target_out, dirs_exist_ok=True)


# copy this repo's addl files
print("copying additional files from root repo")
shutil.copy("README.md", path_target_out)
shutil.copy("CHANGELOG.md", path_target_out)
shutil.copy("LICENSE.md", path_target_out)

# write root HEAD
if gitHead:
  with open(os.path.join(path_target_out, "HEAD-root"), "a") as f:
    f.write(gitHead)


# generate release file from build outputs

# windows & mac use zip, others use tar.gz
file_ext = "zip" if GOOS.lower() == "windows" or GOOS.lower() == "darwin" else "tar.gz"
print(f"generating release file '{release_file_name}.{file_ext}'")

# special case for windows & mac to use zip format
if file_ext == "zip":
  shutil.make_archive(f"{path_output}/{release_file_name}", "zip", path_target_out)

else:
  # filter for setting permissions
  def set_permissions(tarinfo):
    # default no exec and only owner write
    tarinfo.mode = 0o0644
    
    # main app - executable
    if tarinfo.name == "certwarden":
      tarinfo.mode = 0o0755

    # scripts - executable
    elif tarinfo.name.endswith(".sh"):
      tarinfo.mode = 0o0755

    # folders - executable so they're browseable
    elif tarinfo.isdir():
      tarinfo.mode = 0o0755

    return tarinfo

  # make tar
  with tarfile.open(f"{path_output}/{release_file_name}.tar.gz", "w:gz") as tar:
      for file in os.listdir(path_target_out):
        tar.add(os.path.join(path_target_out, file), arcname=file, recursive=True, filter=set_permissions)

print("exiting certwarden build script")
