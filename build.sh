#/bin/bash

repo=/home/greg/certwarden-backend
certwarden_path=/opt/certwarden

cd $repo
git fetch origin
git pull

go build -o $repo/certwarden ./cmd/api-server
