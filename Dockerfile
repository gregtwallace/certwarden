# example build:
# docker build . --build-arg=ROOT_REF=v0.31.1 -t certwarden:v0.31.1

# example master branch build and export
#   docker builder prune -a 
#   docker build . --build-arg=ROOT_REF=master -t certwarden:v0.31.2-a1
#   docker save -o ./out/cw0.31.2-a1.tar certwarden:v0.31.2-a1

# import into docker
#   docker load -i ./cw0.31.2-a1.tar

# example run
# docker run -d --name certwarden -e TZ=Europe/Stockholm -v ./data:/app/data -p 4050:4050 -p 4055:4055 -p 4060:4060 -p 4065:4065 -p 4070:4070 ghcr.io/gregtwallace/certwarden:latest

# Versions
# The resulting container's alpine version
ARG ALPINE_VERSION=3.24.2
# https://hub.docker.com/_/alpine

# used in build containers -- major version defaults that will be overridden by github actions
ARG GO_VERSION=1
ARG NODE_VERSION=24
# https://hub.docker.com/_/golang
# https://hub.docker.com/_/node

# default to building most recent tags
ARG ROOT_REF=master
ARG BACKEND_REF="${ROOT_REF}"
ARG FRONTEND_REF="${ROOT_REF}"

# default blank will use the build environment's values
ARG GOOS=""
ARG GOARCH=""

##



# Build frontend
FROM node:${NODE_VERSION}-alpine AS frontend_build

ARG FRONTEND_REF

WORKDIR /

# install python and git (build.py needs python)
RUN apk add --no-cache python3 git && \
    ln -sf python3 /usr/bin/python

# clone repo
RUN git clone --depth 1 --branch "${FRONTEND_REF}" https://github.com/gregtwallace/certwarden-frontend.git /src/certwarden-frontend

# build
RUN \
    cd /src/certwarden-frontend && \
    npm ci && \
    python build.py --gitrequired



# Build backend
FROM golang:${GO_VERSION}-alpine AS backend_build

ARG BACKEND_REF

ARG GOOS
ARG GOARCH

WORKDIR /

# install python and git (build.py needs python)
RUN apk add --no-cache python3 git && \
    ln -sf python3 /usr/bin/python

# clone repo
RUN git clone --depth 1 --branch "${BACKEND_REF}" https://github.com/gregtwallace/certwarden-backend.git /src/certwarden-backend

# build (get current OS_ARCH for build)
RUN \
    export GOOS="${GOOS:-$(go env GOOS)}" && \
    export GOARCH="${GOARCH:-$(go env GOARCH)}" && \
    cd /src/certwarden-backend && \
    python build.py "${GOOS}_${GOARCH}" --gitrequired



# "Build" root repo
FROM alpine:${ALPINE_VERSION} AS root_build

ARG ROOT_REF

WORKDIR /

# install python and git (build.py needs python)
RUN apk add --no-cache python3 git && \
    ln -sf python3 /usr/bin/python

# clone repo
RUN git clone --depth 1 --branch "${ROOT_REF}" https://github.com/gregtwallace/certwarden.git /src/certwarden

# build
RUN \
    cd /src/certwarden && \
    python build.py --gitrequired



# Make final container
FROM alpine:${ALPINE_VERSION}

WORKDIR /app

# add LE's new CAs (until they're mainstreamed)
COPY --from=root_build /src/certwarden/ca/root-ye.pem /usr/local/share/ca-certificates/root-ye.crt
COPY --from=root_build /src/certwarden/ca/root-yr.pem /usr/local/share/ca-certificates/root-yr.crt

RUN cat /usr/local/share/ca-certificates/root-ye.crt >> /etc/ssl/certs/ca-certificates.crt && \
    cat /usr/local/share/ca-certificates/root-yr.crt >> /etc/ssl/certs/ca-certificates.crt

# acme.sh dependencies (bash, curl, openssl, oathtool) + timezone support (tzdata)
RUN apk add --no-cache \
    bash \
    curl \
    openssl \
    oath-toolkit-oathtool \
    tzdata && \
    mkdir -p /root/.acme.sh

# copy app
COPY --from=backend_build  /src/certwarden-backend/_out .
COPY --from=frontend_build /src/certwarden-frontend/_out .
COPY --from=root_build     /src/certwarden/_out .

# permissions for scripts (*.sh files only)
RUN find ./scripts -type f -name "*.sh" -print0 | xargs -0 chmod 755

# make default data folder
RUN mkdir -p /app/data
# defer empty config file generation to Cert Warden on first run (if not manually made by user prior)

# Note: Do not disable http redirect once https is configured or healthcheck will break
# shorter interval / start period so CI (and `docker run` users) see "healthy" sooner
HEALTHCHECK --interval=10s --start-period=10s \
    CMD curl --silent --output /dev/null --fail http://localhost:4050/certwarden/api/health || exit 1

# http / https server
EXPOSE 4050/tcp 
EXPOSE 4055/tcp

# http challenge server
EXPOSE 4060/tcp

# pprof http / https
EXPOSE 4065/tcp
EXPOSE 4070/tcp

CMD ["/app/certwarden"]
