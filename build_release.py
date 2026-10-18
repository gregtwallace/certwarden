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
import shutil
import sys
import tarfile

# append parent folder to access other src repo scripts
sys.path.append("..")

build_root = importlib.import_module("certwarden.build", package="build_root")
build_backend = importlib.import_module("certwarden-backend.build", package="build_backend")
build_frontend = importlib.import_module("certwarden-frontend.build", package="build_frontend")


##
### Helper Functions
##

# build script is in the source root
PATH_SRC = os.path.dirname(os.path.realpath(__file__))

# return release path
def output_path():
  return os.path.join(PATH_SRC, "_release")


##
### Main Script
##

def main():
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

  # validate build target
  print(f"build target '{args.target}'")
  GOOS, GOARCH = build_backend.parse_os_target(args.target)

  # create base out path if it doesn't exist
  path_output = Path(output_path()).resolve()

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


  # addl root files
  print("calling addl root build script")
  build_root.build(args.gitrequired)

  shutil.copytree(build_root.output_path(), path_target_out, dirs_exist_ok=True)


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


# run main if this script is called directly
if __name__ == "__main__":
  main()
