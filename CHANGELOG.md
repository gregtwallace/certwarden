# LeGo CertHub Changelog

## [v0.12.1] - 2023-08-06

This version is mostly minor fixes.  Pprof support is also added.

### Added
- Add pprof support. Default config option has it disabled though.
- On account object output, include EAB and TOS fields for the relevant
  ACME server.

### Changed
- Conditionally show EAB fields only when they're needed.
- Only show KID on frontend if debug and it is known.
- Use http.ServeContent to serve zip files.
- Deprecate 'domain' arg in dns01 manual method.
- Set directory refresh to occur at 1am + random minute rather than 24
  hours from the last one.

### Fixed
- Fix Cloudflare challenge method failing for domains where the zone has
  more than two parts (e.g. some-name.in.ua).
  See: https://github.com/gregtwallace/legocerthub/issues/22
- Minor code cleanup (move an error, remove an export, and fix a typo).

### Removed
- Cloudflare zone map does not require safety, so mutex was removed.


## [v0.12.0] - 2023-07-27

This version brings support for conditional headers. It also cleans up
some of the backend logic and fixes a couple of issues.

### Added
- Add etag header to pem files when they're sent.
- Add last-modified time stamp to pem files when they're sent.
- Add support for request headers if-match and if-none-match.
- Add support for request headers if-modified-since and
  if-unmodified-since.
- Add support for request header if-range.

### Changed
- Use http.ServeContent to send pem files to clients instead of previous
  Write method.
- Switch to a separate CORS package for ease of use and to ensure proper
  specs are followed without having to maintain it myself.
- Overhauled logic in storage and download packages so pem output is a
  little more sane.
- Updated output package logging to make it a little cleaner and clarify
  some log messages.

### Fixed
- Fixed issue where legacy request api keys would be saved to log.
- Fixed check that always said db needs an upgrade in new version even
  when it didn't.
- Added missing x-api-key and apikey headers to CORS list.

### Removed
N/A


## [v0.11.1] - 2023-07-26

The only fix in this update is acme.sh being added to the Docker
container. If you're not using Docker, there is no difference between
0.11.0 and 0.11.1.

### Added
N/A

### Changed
N/A

### Fixed
- Fixed acme.sh not installing into the Docker container.

### Removed
N/A


## [v0.11.0] - 2023-07-25

This release streamlines new certificate creation by allowing simultaneous
key generation. In the new certificate 'private key' drop down, there is a
new option to generate a key. This eliminates the need to make a new key
separately first. The key name, description, and other fields are copied
from what is specified on the certificate.

### Added
- Add ability to generate a key simultaneously with a new certificate.

### Changed
- Set default new key to Generate and ECDSA P-256.

### Fixed
N/A

### Removed
N/A


## [v0.10.5] - 2023-07-22

This update fixes the acme.sh challenge method when running in Docker
container. It also bundles the acme.sh scripts with LeGo so no extra
modifications are needed to use this method.

### Added
- Bundle acme.sh scripts (v3.0.6) with LeGo.

### Changed
N/A

### Fixed
- Fix acme.sh challenge method when running in Docker.
- Fix linux scripts (primarily install and upgrade scripts).

### Removed
N/A


## [v0.10.4] - 2023-07-18

This release mainly upgrades code dependencies.

### Added
- Some default config comments regarding Docker.

### Changed
- Upgrade to Go 1.20.6.
- Upgrade to Node 18.17.
- Upgrade to Vite 4.4.4.
- Upgrade to eslint 8.45.0.
- Upgrade to semver 6.3.1.
- Upgrade @emotion/react                ^11.10.6  →   ^11.11.1
- Upgrade @emotion/styled               ^11.10.6  →   ^11.11.0
- Upgrade @fontsource/roboto            ^4.5.8    →   ^5.0.5
- Upgrade @mui/icons-material           ^5.11.16  →   ^5.14.0
- Upgrade @mui/material                 ^5.12.2   →   ^5.14.0
- Upgrade @types/react                  ^18.0.28  →   ^18.2.15
- Upgrade @types/react-dom              ^18.0.11  →   ^18.2.7
- Upgrade @vitejs/plugin-react-swc      ^3.0.0    →   ^3.3.2
- Upgrade axios                         ^1.3.6    →   ^1.4.0
- Upgrade eslint-plugin-react-refresh   ^0.3.4    →   ^0.4.3

### Fixed
- Fixed refresh cookie when running in http mode.
- Fixed typo in NODE_VERSION build var.

### Removed
N/A


## [v0.10.3] - 2023-07-05

This release adds the ability to manually edit API keys. This functionality
is intended for advanced users only.

There are also a number of minor bug fixes.

### Added
- Added ability to directly edit API keys. This is generally discouraged
  though.

### Changed
- Improved Cloudflare error logging.
- Reorganize file structure of some frontend components.

### Fixed
- Fixed bad app redirect from root path `/`.
- Fixed bad redirect from http to https in certain configurations.
- Fixed sql query for PUT on certs.
- Fixed sql query for PUT on keys.
- Fixed edit cert re-render due to incorrect comparison of subject alt
  arrays.

### Removed
N/A


## [v0.10.2] - 2023-06-30

Minor updates including modifying the base path for services so LeGo can sit
behind a reverse proxy.

Ideally you would update all client scripts to include the new base path when
accessing the api (e.g. `/legocerthub/api`), however, redirect routes were
added so this isn't necessary (yet).

### Added
- Add base path of `/legocerthub` for both /app and /api. This allows LeGo to
  sit behind a reverse proxy. Redirect routes were added to provide backward
  compatibility with scripts calling the old paths (assuming LeGo isn't behind
  a reverse proxy).
- Add comments regarding how to configure cloudflare dns challenges.

### Changed
- Cloudflare dns challenge no longer requires specifying zone names when using
  an API token. LeGo automatically queries for available zones.
- Cloudflare dns challenge confirms that the proper permission exists (edit dns)
  before adding a zone (domain) to the configured list. If the permission is
  missing, a warning is logged.

### Fixed
- Modify `netcap` command in linux install and update scripts. Some OSes
  will error if the command uses a wildcard.
- Fix typo relating to cloudflare dns challenges in config.default.yaml.

### Removed
- Removed unused var when backend creates environment for frontend.


## [v0.10.1] - Skipped

## [v0.10.0] - 2023-06-19

Primarily this update adds support for custom ACME Servers instead of just
hardcoding Let's Encrypt. This functionality can be found in the web UI
Settings. I've done some testing with Google Cloud but that's about it. LE
is still the most tested provider but feel free to open issues if you run
across problems with others.

Warning: Your database schema will be modified upon install, so make sure you do
a backup just in case.

Warning 2: If you've changed the default ACME server in the last version you
will need to manually edit the database after upgrade to fix the directory
URLs. The upgrade assumes prior use of LE servers and sets those values.

### Added
- Add acme_servers package to manage acme services. This allows users to define
  which ACME Servers they want to use instead of just Let's Encrypt.
- Add comments in default config to elaborate on what dev_mode does.
- Add db user_version as part of db creation.
- Add db user_version upgrade logic from v0 to v1 (these changes are to
  implement the new acme_servers package).
- Add information on server status and new versions regarding db version.
- Add warning in frontend if new version will update db user_version.
- Add widget in Settings to link to ACME Servers viewing and editing. This is
  instead of adding a sidebar link.

### Changed
- Update Vite to version 4.3.9.
- Refactor challenges so storage does not depend on it. This also changes the
  logic for who enabled/disabled is reported.
- Don't export Storage service members.
- Modify frontend to reflect changes to backend status and new version reporting.
- Lint Button component.

### Fixed
- Fix a broken error check in certificates.
- Fix frontend password length check to match backend (which was changed last
  version).

### Removed
N/A


## [v0.9.4] - 2023-06-02

This fixes the docker health check and http redirect.

### Added
- Add a debug log line for the start up of the dns_checker service.
- Add `/api/health` endpoint. This endpoint does not require authentication and
  returns a 204 if the server is running.

### Changed
- Reduce min password length from 10 to 8 characters. This is less secure, please
  don't actually do it! If you're doing dev work and want a bad password strictly
  for testing, turn devMode on and min length is completely removed.

### Fixed
- Fix docker healthcheck failing. Corrected healthcheck in Dockerfile and also
  set it to the `/api/health` endpoint.
- Fix unlikely case where isRefreshing may not properly change back to false on
  the frontend if the token refresh errored.
- Fix http redirect in cases where bind address is not the correct browser address.
  For example, previously binding to `0.0.0.0` would cause an incorrect redirect to
  https://0.0.0.0 rather than the actual server. The new method uses the same
  hostname as was in the original request so it doesn't matter what the bind
  address is set to or what alias the client is using to connect.

### Removed
N/A


## [v0.9.3] - 2023-05-20

Fixes dns_checker null pointer bug where dns methods don't work if Cloudflare
method was not enabled (even if not using Cloudflare).

### Added
- Add External Account Binding support, though support of alternate CAs is
  still considered experimental.
- Add generic error code catcher on ACME calls.

### Changed
- Require email on accounts.

### Fixed
- Fix issue where dns_checker didn't start if dns-01 was being used but
  Cloudflare was disabled.
- Fix non-standard account field `createdAt`.
- Fix response processing of account key rollover action.
- Fix issue where frontend would erroneously display a `0` in form footers.

### Removed
N/A


## [v0.9.2] - 2023-05-19

Thanks to those that have made contributions!

### Added
- Build arm64 support both as binary and as docker image.
- Add docker-compose.yml sample to repo.
- Add sample docker build & commands.
- Docker first run includes `config_version` now.
- EXPERIMENTAL: Allow changing of ACME directories in config.

### Changed
- Changed docker binary to match other binaries.
- Made acme.sh temp script name more specific.

### Fixed
N/A

### Removed
- All logging saves to log files now. `log` package has been completely 
  removed.
- Removed frontend references to Let's Encrypt.


## [v0.9.1] - 2023-05-17

Two additional challenge methods have been added. Most excitingly, if you
clone the acme.sh repo you can use ANY dns provider supported by that set
of scripts without having to edit any scripts yourself.

Support for acme-dns was also added.

You should add `config_version: 0` to your config file as this is a new
check. Nothing will break without it but you will get an error in the log.

### Added
- Config version check to help flag when breaking changes are anticipated
  during a version upgrade.
- Support for acme-dns server (https://github.com/joohoi/acme-dns)
- Support for acme.sh (https://github.com/acmesh-official/acme.sh)
- Support for environment variables in dns-01 manual shell scripts.

### Changed
- Change update check display to show time last checked.

### Fixed
- Logging of stderr for dns-01 manual shell scripts.

### Removed
N/A


## [v0.9.0] - 2023-05-13

This release brings a number of changes including an automatic check for new
versions as well as docker support. Please review the config.default.yaml to
ensure you're using all of the desired settings.

### Added
- Added update check that queries a remote json file daily to determine if a
  new version is available. Auto update is not part of this and may be added at
  a later date.
- Docker support.
- Log app version on start to make logs clear as to which version was running
  during an event.

### Changed
- Allow really poor passwords in dev mode (removed min character length).

### Fixed
- Minor type fix in challenges.
- Minor simplification of auth construction.
- Flexbox on navbar.
- Password change error not properly displaying.
- Missing useEffect dependency in main.

### Removed
- Removed 'hostname' config option. Backend now configures the self hosted
  frontend with an absolute path so a hostname isn't needed.


## [v0.8.0] - 2023-05-04

> **Warning**
> Please read as there are breaking changes requiring manual intervention.

lego-certhub.db, config.yaml, and the log folder need to be manually moved to
a /data subfolder if coming from a prior release.

You may also need to update your config file:
- 'bind_address' added to specify what address the server should bind to. The
  default is blank which binds to all available addresses.
- 'cors_permitted_origins' should be set if you need cross-origin support.

### Added
Backend
- Added 'bind_address' configuration option which defaults to all addresses.
- Added 'cors_permitted_origins' to define permitted origins for cross-origin
  requests.

Frontend
- Added highlighting on active navbar route.

### Changed
Backend
- Moved db, config, and log storage to /data subfolder (primarily to make
  docker mounting easier).
- Updated cross-origin configuration to better match intent.
- API URL for hosted frontend is based on config 'hostname'. This should be
  a dns resolvable fqdn.
- Updated some log messages regarding server start and bind address.
- 'hostname' functionality was clarified.
- Simplified subject validation functions on certificates.
- Did some linting on certificates put function.

Frontend
- Updated ApiError wording.
- Updated navbar components to make a little nicer.

### Fixed
Backend
- Fixed cookie to properly permit cross-origin refresh. If cross-origin is not
  configured, cookie SameSite is set to strict for added security.
- Fixed inability for ACME Accounts secured by RSA key to validate DNS
  challenges. (https://github.com/gregtwallace/legocerthub-backend/issues/1)

Frontend
- Fixed a path that was not properly updated when moving to Vite.
- Fixed auth_expiration management by moving from a cookie to session storage.
- Fixed app rendering where the wrong render would briefly appear before App
  had loaded session storage data.

### Removed
Backend
- Localhost is no longer always allowed by cross-origin header.
- Removed some details regarding backend configuration when querying status.
- Removed login expiration cookie.

Frontend
- Removed details related to backend status call change.


## [v0.7.0] - 2023-04-29

Major updates were made to the frontend in this release, including removing
Create React App and replacing it with Vite.

### Added
Backend
- Added tests for validation package.

Frontend
- Defined props with prop-types.
- Added sublabel on text array component.
- Added placeholder message on empty InputSelect fields.

### Changed
Backend
- Log Cloudflare domains at Info level.
- Updated email validation regex and method. Domain piece uses domain validator
  and email username is separately validated.
- DNS Manual Script name updated.

Frontend
- Port from Create React App to Vite (CRA is deprecated).
- Moved constants to a separate file.
- Updated paths for navigation when using cancel and submit buttons. Next
  destination is now explicit rather than relative.
- Login form clears if backend rejects the login.

### Fixed
Frontend
- Did a ton of linting.
- Fixed issue where Axios errors could cause a loop on logout and also cleaned
  up Axios error handling in general.
- Fixed issue where Rollover Account Key would still show loading message even
  after loaded.

### Removed
Frontend
- Removed dummy forms.
- Removed duplicative FormError component and replaced with common ApiError
  component.


## [v0.6.11] - 2023-03-12

### Added
- Added debug log message when dns checker is configured to skip the check.

### Changed
- Update dependency versions: x/text, x/net, x/time, x/crypto, & go-retryablehttp
- Abort dns checker sleep when configured to skip and shutdown signal is received.

### Fixed
- Patched several CVEs by upgrading dependencies, including CVE-2022-32149,
  CVE-2022-41721, CVE-2022-27664, and CVE-2022-41723.
- Add missing error check in Cloudflare challenge provider.

### Removed
N/A


## [v0.6.10] - 2023-03-08

### Added
N/A

### Changed
- Update Go version and move Node and Go versions to global variables in build script.
- Rename DNS example scripts to avoid accidental overwrite.
- Minor code clarification in CORS.

### Fixed
N/A

### Removed
N/A


## [v0.6.9] - 2023-01-29

### Added
- Config option to disable dns checker module. Instead, specify a time to sleep and
  then assume dns propagated successfully.
- Manual DNS script challenge validation module. Calls external scripts to create
  and remove DNS records. This allows support for any DNS provider. Add example scripts
  to show variables available to scripts.
- Add some more config comments on dns checker config.

### Changed
- Better logging for config parsing.
- Better authentication logging for audit trail.
- Better download logging for audit trail.
- Exit on improperly formatted config.yaml

### Fixed
- Fix install and upgrade linux scripts to work when called from any path.
- Fix logic auto order logic that could sometimes result in the job being called
  twice on the same day.
- Include subject in the CSR DNSNames field (not just Alt Names). LE accepted the
  previous method but Pebble returns an error without this.
- Frontend: Fix missing Staging Flag in All Certificates.
- Frontend: Fix wrong information in confirm delete certificate Dialog.

### Removed
N/A
