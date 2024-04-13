# Parent dir is root
$scriptDir = Get-Location
$rootDir = Split-Path -Path $scriptDir -Parent
$outDir = Join-Path -Path $scriptDir -ChildPath "/out"

## Backend
Set-Location $rootDir/certwarden-backend

# Include config example
Copy-Item -Path $rootDir/certwarden-backend/config.default.yaml -Destination $outDir

# Mandatory env flag for sqlite
$env:CGO_ENABLED = 1

# Windows x64
$env:GOARCH = "amd64"
$env:GOOS = "windows"
go build -o $outDir/certwarden.exe ./cmd/api-server

## Frontend
Set-Location $rootDir/certwarden-frontend
npx vite build

# remove old build
Remove-Item -Path $outDir/frontend_build -recurse
New-Item -ItemType Directory -Force -Path $outDir/frontend_build

# move to out
Move-Item -Path $rootDir/certwarden-frontend/dist/* -Destination $outDir/frontend_build

# Return to original path
Set-Location $scriptDir
