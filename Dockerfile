# example build:
# docker build . --build-arg=BACKEND_VERSION=v0.8.0 --build-arg=FRONTEND_VERSION=v0.8.0 -t legocerthub:v0.8.0

# example run
# docker run -d --name legocerthub -v ./data:/app/data -p 4050:4050 -p 4055:4055 -p 4060:4060 -p 4065:4065 ghcr.io/gregtwallace/legocerthub:latest

FROM node:18-alpine as frontend_build

ARG FRONTEND_VERSION

WORKDIR /

RUN apk add git && \
    git clone --depth 1 --branch "${FRONTEND_VERSION}" https://github.com/gregtwallace/legocerthub-frontend.git /src && \
    cd /src && \
    npm clean-install && \
    npx vite build


FROM golang:alpine AS backend_build

ARG BACKEND_VERSION
ARG CGO_ENABLED=1

WORKDIR /

RUN apk add git gcc musl-dev && \
    git clone --depth 1 --branch "${BACKEND_VERSION}" https://github.com/gregtwallace/legocerthub-backend.git /src && \
    cd /src && \
    go build -o ./lego-linux-amd64 ./cmd/api-server


FROM alpine:latest

WORKDIR /app

# acme.sh dependencies
RUN apk add bash
RUN apk add curl
RUN apk add openssl
RUN mkdir -p /root/.acme.sh

# copy app
COPY --from=backend_build /src/lego-linux-amd64 .
COPY --from=backend_build /src/config.default.yaml .
COPY --from=backend_build /src/scripts/linux ./scripts
COPY --from=frontend_build /src/dist ./frontend_build
COPY ./README.md .
COPY ./CHANGELOG.md .
COPY ./LICENSE.md .

# make default config
RUN sh -c "mkdir /app/data"
RUN sh -c "printf '%s\n'                \
            'config_version: 1'         \
        > /app/data/config.yaml"

# Note: Do not disable http redirect once https is configured or healthcheck will break
HEALTHCHECK CMD wget --no-verbose --tries=1 --spider --no-check-certificate http://localhost:4050/legocerthub/api/health || exit 1

EXPOSE 4050/tcp
EXPOSE 4055/tcp
EXPOSE 4060/tcp
EXPOSE 4065/tcp

CMD /app/lego-linux-amd64
