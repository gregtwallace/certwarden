#/bin/bash

repo=/home/greg/legocerthub-backend
lego_path=/opt/legocerthub

systemctl stop legocerthub

cd $repo
git fetch origin
git pull

export CGO_ENABLED=1
go build -o $repo/lego-amd64-linux ./cmd/api-server
mv $repo/lego-amd64-linux $lego_path

systemctl start legocerthub
