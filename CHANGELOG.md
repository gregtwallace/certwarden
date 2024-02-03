# LeGo CertHub Changelog

## [v0.18.4] - 2024-02-02

Minor updates.

### Added
- Add post processing variable names for custom environment variables. Instead
  of being forced to use `LEGO_CERTIFICATE_COMMON_NAME` the string 
  {{CERTIFICATE_COMMON_NAME}} can be used as a value in a custom named
  variable. This allows more versatility in post processing.
- Add ability to run binaries in post process, in addition to scripts.

### Fixed
- Fix issue where time might print strangely in log message about 
  auto-ordering.
- Fix wrong tooltip over the ignore update X button.
- Fix frontend form validation on provider domains. Wildcards are not allowed
  on providers as the domain is already assumed to include all subdomains, 
  including wildcard subdomains. The backend already properly validated this
  but the frontend did not.

### Changed
- Update Vite to 4.5.2.


## [v0.18.2] - 2024-01-11

Minor updates.

### Added
- Add new API route to download key, cert, and certchain all in one file.
- Add ability to view all DNS names on any given order.
- Docker: Add timezone support (use the TZ environment variable).

### Changed
- Change key name display on a given order to show an icon instead of the 
  long name, with a tooltip containing the key name. Clicking the icon 
  still navigates to the key.


## [v0.18.1] - 2024-01-06

Minor fixes to prior release.

### Fixed
- Fix backend post to LeGo client.
- Fix missing field error on frontend.


## [v0.18.0] - 2024-01-05

This release is pretty beefy with a number of significant code changes. Of 
most interest to users is the addition of support for EVEN MORE dns providers 
thanks to the integration of go-acme/lego.

DNS providers supported by the new provider option: 
https://go-acme.github.io/lego/dns/

I'm also working on a client container that can receive certificate updates 
and restart designated docker containers (so they pick up new certs). The 
code for the client is available at 
https://github.com/gregtwallace/legocerthub-client 
but builds aren't yet published and use is not yet recommended unless you 
really want to live on the bleeding edge.

### Added
- Add go-acme le-go provider type. This adds even more dns provider options.
- Add LeGo Client post processing option. Causes the db to upgrade to user 
  version 4. The client is still under development and compiled versions are 
  not yet posted.

### Fixed
- Fix possible provider update having a nil-deref if sending API payload 
  without a config.
- Fix expiration check when trying to manually run post-processing. The wrong 
  expiration was previously being used causing post processing to fail if the 
  order was over ~1 week old.
- Fix logging during challenge checking for valid/invalid. There was a bad
  variable.
- Update some dependencies to address possible vulnerabilities.

### Changed / Improved
- Decoupled domains from provider configs. Providers do not need knowledge of 
  the domains. No changes to the config.yaml file though, this was just some 
  code cleanup.
- Simplify provider manager code a little bit by getting rid of an unneeded
  map.
- Rollback cloudflare api package as a test to observe impact in pprof. This 
  should have no user facing impact.


## [v0.17.3] - 2024-01-02

Minor fixes.

### Added
- Add ability to specify different provider(s) for subdomains. This allows 
  provider A to service example.com but use provider B for sub.example.com.

### Fixed
- Fix nil deref during automatic backup of app prior to config file version 
  upgrade.
- Fix mismatch of domain to provider in case where domains have overlapping 
  names (e.g. testexample.com would have matched to example.com).
- Several possible CVEs addressed via dependency updates and Go version 
  update to 1.21.5.


## [v0.17.2] - 2023-12-30

Minor fixes.

### Fixed
- Fix spawning of zombie `ssl_client` process in docker container.
- Fix label on private key API Key showing as `old` even though it is the 
  only API Key.


## [v0.17.1] - 2023-12-21

Minor fixes to the prior release.

### Fixed
- Ensure backup folder gets created.
- Fix possible hang of shutdown during failed backup waiting to retry.
- Fix post processing logging so it is more clear what's going on.


## [v0.17.0] - 2023-12-20

This release adds backup functionality. It also adds the ability to run 
a script on the server after the succesful completion of certificate 
creation or renewal.

### Added
- Add backup functionality both to store locally on disc and to download 
  to client. Automatic backups are enabled by default but backup settings 
  can be changed in the config file. See the config example, change log, 
  and default for more info.
- Add post-processing script options to certificate. If you want to push 
  new certificates to clients you can use a script on the LeGo server to 
  do so and specify the script path and environment variables in the 
  certificate settings.
- Add post-processing button to certificates' orders. Useful for testing 
  post processing is working without having to repeatedly order new 
  certificates. This can also be used to rollback to previous orders, if 
  needed.

### Changed / Improved
- Relocate db and config file to ./app sub folder of main data folder. 
  Files will be moved automatically from the previous location.
- Cloudlare now permits wrong config. This is so the app still starts 
  even if the internet is down. To compensate, log messages are clear in 
  the logs to highlight the problem.
- Allow non-existent scripts in dns01manual method. This is to allow 
  configuration before the script is in the folder and also to avoid 
  failures to start if a file gets moved. Errors will be logged 
  accordingly.
- Make grids on front end look a little nicer.

### Fixed
- Fix frontend idle logout. The timer was not properly resetting so early 
  timeout would trigger.

### Removed
- Remove notice about Let's Encrypt on the ACME Servers page. Support is 
  more general now, so no need to warn.


## [v0.16.3] - 2023-12-13

> [!CAUTION]
> You need to upgrade to this release **IMMEDIATELY** if you are running 
> version 0.15.1 through 0.16.2. These versions contain a critical 
> security flaw which potentially allowed unauthorized access to private 
> keys.

The sole change in this release is addressing a critical security flaw.

Depending on the sensitivity of your environment, the most secure action 
after updating your version is to revoke all your certificates, rotate all 
of your account private keys, and reissue all of your certificates with 
new keys.

If you're just running a home lab or have access denial measures in 
place to prevent access to your server, this is almost certainly overkill. 
I have been running these versions too and all I am doing is rotating 
my account keys as an extra precaution.

You can also manually review your logs between instllation of 0.15.1 
and now to see if the keys were actually downloaded by an unauthorized 
client.

This vulnerability did not allow access to any other sensitive 
information such as the config file, API keys, etc. Only the download of 
private keys was impacted.

### Added
N/A

### Changed / Improved
N/A

### Fixed
- Fix critical security vulnerability that allowed unauthenticated 
  clients to download sensitive files.

### Removed
N/A


## [v0.16.2] - 2023-12-05

> **Warning**
> This release fixes a security issue where the wrong permissions 
> were set on the database and config files. Please manually verify 
> your ./data/config.yaml and ./data/lego-certhub.db are set to 
> 0600 (RW for owner only).

Release to address the security issue in the warning and ensure files 
have the proper permissions set on creation.

Also a doc fix and install script fix.

### Added
N/A

### Changed / Improved
N/A

### Fixed
- Fix security issue where db and config might not be created with 
  the proper permissions (0600).
- Fix Linux install script. Empty config file causes an error so just 
  let LeGo create the file on first run.
- Update config example, defaults, and change log to include info 
  about the pprof change in the last release (oops, forgot).

### Removed
N/A


## [v0.16.1] - 2023-12-03

A laundry list of fixes and improvements.

Note: The config schema will update from 2 to 3 due to change in the
pprof port config variable.

### Added
- Add exponential backoff and retry for a number of functions (acme 
  directory refresh, dns record checking, acme order processing and
  challenge solving).
- Add more detailed error for when actions run with an empty acme
  directory (i.e. the directory url is currently failing).
- Add automatic config backup before writing automated schema updates.
- Add automatic db backup before writing automated schema updates.
- Add security headers and access logging to pprof server.

### Changed / Improved
- Improve acme post signed debug logging to be more helpful in the 
  event troubleshooting is needed. Logging now occurs of items before
  they are encoded (and thus not easily readable by a human). Log
  unencoded payload and destination, indent server responses before
  logging, and add logging for csr common name and dns name on finalize
  action.
- Make acme error type more straightforward.
- Improve acme post signed logic.
- Improve order fulfillment logic.
- Cap order fulfillment at 2 hours before failing (instead of a set
  number of loops through the logic).
- Do not allow order actions if the certificate form above is change.
  This is intended to prevent accidentally doing an action with stale
  (unsaved) data.

### Fixed
- Fix pprof with HSTS header by having pprof also run in https mode
  when server has a valid cert. As a result, config now has a 
  separate port option for http and https. Also add the new default
  port to Docker files.
- Directory refresh edge case that could result in double refresh.
- Ensure app doesn't shutdown before challenge record deprovisioning
  is complete.
- Use proper errors Is and As instead of assertions and plain
  comparisons.
- Use proper error types for error comparisons (e.g. Cloudflare 
  dns record already exists error and dns check error is not found).
- Fix default permissions on db when creating new.
- Fix frontend cert revoke button color.
- Fix showing a priority on idle workers on the frontend. Priority 
  should be blank since there is no job.
- Fix Place New Order button not being disabled during an action.

### Removed
- Remove redirect to frontend root on login timeout. This was added in
  the last update and is just kind of annoying without much benefit.


## [v0.16.0] - 2023-11-25

The frontend has been completely updated to TypeScript with full type
safety. This involved a ton of code changes, please report any issues.

If you experience something breaking, the previous version has the same
config and database versions, so report the issue and downgrade both
the frontend and the backend binary to the previous version.

### Added
- Add redirect if invalid page is specified when viewing a table of
  things (e.g. keys, certs, etc).
- Add redirect of any frontend path when logged out to the main root
  path.

### Changed
- Complete overhaul to implement TypeScript.
- Overhaul backend responses to be more detailed and consistent.
- Update contexts and hooks on frontend for a little bit more sanity.
- Updated input handler to use recursion and support any depth object.
  Also changed methodology of the handler to make it compatible with
  type safety.
- Show success or error message on password change.
- Update frontend server url validation to confirm only valid
  characters in addition to https.
- Submit button on forms is always enabled.
- Use regex for field name matching to look up value type and error
  message.
- Remove some info from displaying on providers summary page. To get
  all of the details, click into 'Edit'.
- Update type for validation errors and method of recording errors.
- Update frontend dependencies.

### Fixed
- Update Axios version to address a security issue.
- Show success or error message on password change.
- Fix sorting of account list by environment column.
- Add missing CSR 'State' field.

### Removed
N/A


## [v0.15.2] - 2023-11-06

This release is quality of life. It mainly addresses things related to
logging.

### Added
- Info log logout success.

### Changed
- Tweak wording on frontend describing the order queue.
- Reorder CSP params.
- Rename error handling middleware to not use the word error.

### Fixed
- Fix inaccurate info logging of certain information when serving the
  frontend. This was creating log clutter that should only be in debug.
- Fix CSP whitespace on default policy.
- Fix typing of json response Message field.

### Removed
N/A


## [v0.15.1] - 2023-10-31

This release is mostly quality of life improvements. Various security
mechanisms are fine tuned and some minor bugs are fixed.

### Added
- Add Referrer-Policy and set to no-referrer.
- Add more security headers to all server responses.
- Use nonce for styles in Content Security Policy by setting on a meta
  property and using some crafty on the fly code tweaking when the backend
  serves the relevant js file.

### Changed
- Tighten up Content Security Policy.
- Rewrote backend middleware logic to make code easier to follow and to make
  it easier to adjust middlewares moving forward.
- Don't use CORS on 404 error.
- Secure change password and logout routes with access token. (This was
  secure before, the logic is just more consistent now.)
- Simplify backend logout logic.
- Auth minor code cleanup for clarity.
- Rename refresh token to session token and update references to 'session'
  for consistency.
- Update dns_checker log messages.
- Use full base64 character set for nonce generation.
- Simplify (streamline) frontend useAuth hook.

### Fixed
- Fix broken checkbox when editing an ACME Server.
- Fix Vary header usage logic for download.
- Update auth log message format to match new format.
- Add proper fallback options to Content Security Policy.
- Fix retry logic on frontend during access token refresh (fewer unneeded
  retries will occur).

### Removed
- Remove nonce from scripts in Content Security Policy and only allow
  'self' in script Content Security Policy.


## [v0.15.0] - 2023-10-23

> **Warning**
> You must ensure your config.yaml is at least config_version: 1 prior to
> installing or LeGo will not start.

Note: If you are new or don't have a config.yaml, one will be created for
you on the first run of LeGo.

Moving forward LeGo will enforce config_version but will migrate seemlessly
unless there are notes to the contrary. Notes will include specific needed
actions. To assist with changes across versions, all releases now include a
config.changelog.md which notes all changes, not just breaking changes.

If you are already on the previous version (0.14.1) you can just manually
insert `config_version: 1` without any other changes. You should still
review the config default and example to ensure you have the options you
want.

This version also includes a bunch of other features, most of which revolve
around adding more security to LeGo.

### Added
- Create config.yaml if one does not exist.
- Add strict enforcement of config.yaml schema version.
- Add auto update schema from 1 to 2. Older version 0 or unspecified
  version will need manual intervention (at a minimum config_version
  will need to be added).
- Add HTTP Strict Transport Security (HSTS) header by default. Config has
  an option to disable the header (`disable_hsts`).
- Add relatively strict `Content-Security-Policy` header, including nonces
  on scripts. Vite does not yet support nonces for style but I will add
  it later when it does.
- Add headers to prevent MIME type sniffing and iframes.
- Add `frontend_show_debug_info` config option to set frontend to show
  debug info and do some console.logging.
- Add ability to clear the update notification from the left side
  navigation bar.
- Add logout tooltip.
- Add theme toggle tooltip.
- Add data-preload on style, script, and link tags.
- Add timeout context on Cloudflare API calls.
- Include config.changelog.md in releases. This file details changes to
  config.yaml over time.

### Changed
- Move theme toggle to just an icon in bottom right corner in footer.
- Rewrite frontend file handler on the Go backend. Needed to provide
  more consistent headers and nonce support.
- Update to Go 1.21.3, Node 18.18.2, and Vite 4.5.0.
- Update all other dependencies in frontend and backend.
- Update acme.sh script to 3.0.7 (adds a couple more dns providers).
- Update Cloudflare provider to utilize newest Cloudflare Go api.
- Some minor code cleanup.
- Rename `cors_permitted_origins config option` to 
  `cors_permitted_crossorigins`.
- Minor navbar restyling.
- Change status/new version information and update frontend to properly
  show the changed information.
- Redact certain senstive information when the frontend is set to log
  debug info to the console.

### Fixed
- Fix accidentally allowing all cross-origins by default. If no origins
  are specified, CORS is disabled.
- Explicitly set dockerbuild tool versions so binary releases and docker
  releases are built in the same way.

### Removed
- Removed dockerfile generation of empty config file. This is now handled
  by the backend when it runs for the first time.
- Remove frontend Settings link to backend URL. Link just goes to a 404
  so there isn't really a point.
- Remove Roboto font include and move it to external files.


## [v0.14.1] - 2023-10-17

The are two significant updates in this version. The first is the removal
of dev mode and related feature disablement over http. This provides more
configuration flexibility (e.g. behind a reverse proxy) but does forego
some security. Users are trusted to choose what is right for them.

The other major update is the addition of the ability to review orders
that are in progress or queued up to be worked. The new section "Order
Queue" shows both orders actively being worked by a worker and also
orders awaiting an available worker. The list of orders show under edit
certificate also reflects if a particular order is already in the queue
and the "Retry" button is disabled if the order already queued up. This
feature should eliminate some of the "guessing" about what LeGo is doing
in the background without having to look through the logs.

### Added
- Add ability to view orders currently being worked on and queued to be
  worked on when a worker is available.

### Changed
- Update worker log messages to include worker number.
- Return 404 for bad routes instead of 401.
- Frontend dev mode replaced with show/log debug info. This is set by the
  backend if log level is debug.
- Change some minor styling on frontend.
- On frontend edit certificate, update order status to reflect information
  if the order is in the order worker queue.

### Fixed
- Fix border colors on input array of objects of text fields.

### Removed
- Remove dev mode.
- Remove disabling of certain functions when server is running over http
  (instead of https).
- Remove password complexity requirements.


## [v0.14.0] - Skipped

## [v0.13.1] - 2023-10-12

This release adds the ability to add, edit, and delete providers via the
frontend GUI. It is now possible to setup LeGo without manually editing
the config file. You should still check the config example to see if you
need or want to set any of those options.

### Added
- Add ability to add, edit, and delete providers via the GUI and without
  having to restart LeGo.
- Add example config to release packages and docker image. This should
  have been added last version.

### Changed
- If dns_checker can't properly configure dns servers, fallback to sleep
  for 2 minutes. This is to avoid app start failure in this instance and
  instead to use a reasonable alternative. An error is still logged.
- Change deprecated substr func to substring func.
- Set 'Revoke' button on certificate orders to be red.
- Don't redact acme-dns provider info. It isn't sensitive enough to
  justify the additional complexity.
- Always log some basic info when orders are placed and completed.
  Previously this was only showing at debug log level.

### Fixed
- Fix sometimes non-unique key on GUI display of provider config.
- Fix handling of redacted info when it is POSTed.

### Removed
N/A


## [v0.13.0] - 2023-10-10

> **Warning**
> Please read as there are breaking changes requiring manual intervention.

1: LeGo config MUST be updated using the new provider format which includes
specifying domains. See the example config file. A wildcard provider can also
be configured (single domain of *) and LeGo will use this provider if there
is no provider configured for a given domain. If you only use one provider,
you should add the wildcard domain and you're done.

2: Domain arg has been removed from dns manual scripts. Domain cannot be reliably
determined and as such it has been removed. This caused the position of the args
for these scripts to move and your scripts will need an update if you use this
method.

3: Removed redirects from old paths. When LeGo added the base path /legocerthub
old routes at base / were given redirects to prevent breakage. These redirects
are now removed and any clients using the old paths will need their scripts
updated.

This release does away with the need to select a challenge provider for each
certificate. It also has several tweaks and minor fixes.

The groundwork is also in place to add/edit/delete providers via the GUI. This
will be added in a future version.

### Added
- Add environment output on sample dns scripts.
- Add backend functionality to modify providers while server is running via
  routes. Frontend modification not yet added.
- Add ability to view providers in the frontend.

### Changed
- Update to logging of some debug info.
- Separate default config from example config to make it more apparent what the
  default settings are.
- Reduce API key length from 48 to 32. This is based on an entropy calculation
  and still provides adequate security.
- Move ACME Servers to side bar in frontend navigation.
- Update config version from 0 to 1 (see notes above).
- Code clean up in several spots.
- Clarified various log messages.
- Clean up and streamline logic for form handling on frontend, including
  common input handler.

### Fixed
- Do a better job of redacting certain sensitive information in debug logs.
- Fix api keys form unchanged calculation.
- Add openssl to dockerbuild (needed for acme.sh).
- Fix usage of access_token by frontend.
- Fix manifest paths.

### Removed
- Remove need to select a challenge method. Instead, domains are configured
  and LeGo automatically selects the correct provider based on the domains
  in the certificate.


## [v0.12.6] - 2023-08-20

Releasing solely to fix importing of private keys via the frontend UI.
There are other minor changes but they are so minor they probably aren't
relevant to users.

### Added
N/A

### Changed
- Generic-ify SafeMap (minor code clean improvements).
- Minor update to handling of empty acme time in Order object NotBefore
  and NotAfter fields.
- Verify session is still valid before refreshing a session. This was
  already being done, but made it more explicit.

### Fixed
- Fix private key import via frontend UI.

### Removed
N/A


## [v0.12.5] - 2023-08-11

This release adds shutdown and restart functions. Otherwise, it mainly
fixes some minor bugs and optimizes some code.

Config Note: 'private_key_name' is no longer a config field. The key
is now derived from 'certificate_name'.

### Added
- Add shutdown and restart routes with buttons in frontend to trigger
  those routes.

### Changed
- Update some route names.
- Update LeGo https certificate reload logic to no longer require a go
  routine. LeGo cert will update as soon as it renews.
- Optimize view log handler for better memory footprint.
- Update output package to remove unneeded vars.

### Fixed
- Fix broken log download handler and optimize related code.
- Modify logger so it is gracefully closed on exit, though it is not
  perfect due to lumberjack bug:
  https://github.com/natefinch/lumberjack/issues/56
- Fix log view handler failing to close file.

### Removed
- Remove LeGo config option for private key. Private key is now derived
  from the certificate name.


## [v0.12.4] - 2023-08-08

This release resolves a significant issue with the challenge solver
failing in certain cases involving wild card certificates or multiple
ACME providers.

### Added
- Add an error if user tries to enable acme.sh on a Windows server.
- Add better notes in default config regarding acme.sh options.
- Add shutdown handler for client to trigger LeGo shutdown.
- Make WorkTracker data type for reuse.

### Changed
- Move pprof to its own http server and port.
- Significant overhaul of custom http client to make it more sane.
- Rework how challenge resource provisioning is tracked. Instead of in
  each method, centralize in Challenges package.
- Some minor code tidy up.

### Fixed
- Fix when multiple workers are trying to solve Challenges that use
  the same resource name. This could cause Orders to fail under certain
  conditions. Instead, queue the resources and solve the Challenges
  one at a time.
- Make Cloudflare use the app's http Client with the proper settings.

### Removed
N/A


## [v0.12.3] - 2023-08-06

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


## [v0.12.2] - Skipped

## [v0.12.1] - Skipped

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
