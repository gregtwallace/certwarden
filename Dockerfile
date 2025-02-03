# example build:
# docker build . --build-arg=BACKEND_VERSION=v0.8.0 --build-arg=FRONTEND_VERSION=v0.8.0 -t certwarden:v0.8.0

# example run
# docker run -d --name certwarden -e TZ=Europe/Stockholm -v ./data:/app/data -p 4050:4050 -p 4055:4055 -p 4060:4060 -p 4065:4065 -p 4070:4070 ghcr.io/gregtwallace/certwarden:latest

# Versions - keep in sync with build_releases.yml
ARG ALPINE_VERSION=3.21
ARG GO_VERSION=1.23.5
ARG NODE_VERSION=18.20.6
# https://hub.docker.com/_/alpine
# https://hub.docker.com/_/golang
# https://hub.docker.com/_/node

FROM node:${NODE_VERSION}-alpine${ALPINE_VERSION} AS frontend_build

ARG FRONTEND_VERSION

WORKDIR /

RUN apk add git && \
    git clone --depth 1 --branch "${FRONTEND_VERSION}" https://github.com/gregtwallace/certwarden-frontend.git /src && \
    cd /src && \
    npm clean-install && \
    npx vite build


FROM golang:${GO_VERSION}-alpine${ALPINE_VERSION} AS backend_build

ARG BACKEND_VERSION
ARG CGO_ENABLED=1

ENV CGO_CFLAGS="-D_LARGEFILE64_SOURCE"

WORKDIR /

RUN apk add git gcc musl-dev && \
    git clone --depth 1 --branch "${BACKEND_VERSION}" https://github.com/gregtwallace/certwarden-backend.git /src && \
    cd /src && \
    go build -o ./certwarden ./cmd/api-server


FROM alpine:${ALPINE_VERSION}

WORKDIR /app

# acme.sh dependencies
RUN apk add bash
RUN apk add curl
RUN apk add openssl
RUN apk add oath-toolkit-oathtool
RUN mkdir -p /root/.acme.sh

# timezone support
RUN apk add --no-cache tzdata

# copy app
COPY --from=backend_build /src/certwarden .
COPY --from=backend_build /src/config.default.yaml .
COPY --from=backend_build /src/config.example.yaml .
COPY --from=backend_build /src/config.changelog.md .
COPY --from=backend_build /src/scripts/linux ./scripts
COPY --from=frontend_build /src/dist ./frontend_build
COPY ./README.md .
COPY ./CHANGELOG.md .
COPY ./LICENSE.md .

# make default data folder
RUN sh -c "mkdir /app/data"
# defer empty config file generation to Cert Warden on first run (if not manually made by user prior)

# Note: Do not disable http redirect once https is configured or healthcheck will break
HEALTHCHECK CMD curl --silent --output /dev/null --fail http://localhost:4050/certwarden/api/health || exit 1

# http / https server
EXPOSE 4050/tcp 
EXPOSE 4055/tcp

# http challenge server
EXPOSE 4060/tcp

# pprof http / https
EXPOSE 4065/tcp
EXPOSE 4070/tcp

CMD ["/app/certwarden"]
