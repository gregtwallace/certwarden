# LeGo CertHub Changelog

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
