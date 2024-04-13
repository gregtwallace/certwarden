#/bin/bash

repo=/home/greg/certwarden-backend
certwarden_path=/opt/certwarden

cd $repo
git fetch origin
git pull

export CGO_ENABLED=1

go build -o $repo/certwarden ./cmd/api-server
