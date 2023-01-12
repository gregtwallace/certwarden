#/bin/bash

repo=/home/greg/legocerthub-backend
lego_path=/opt/legocerthub

cd $repo
git fetch origin
git pull

export CGO_ENABLED=1

go build -o $repo/lego-linux-amd64-linux ./cmd/api-server
