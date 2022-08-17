# Changelog

These are the changes made to the Ky3M project from the beginning:

## [Release 0.2.1](https://github.com/Procybit/Ky3m/releases/tag/v0.2.1) (XXXX-XX-XX)

**PLEASE RE-ADOPT MODS WITH "${file.jarVersion}" VERSION IF YOU HAVE SUCHLIKE!**

### Fixed

- Fixed BURST (did not delete bundles before)
- Fixed DETACH output
- Fixed Minecraft mod info extractor in "${file.jarVersion}" case.
- Fixed BIND when entering invalid saved ID

## [Release 0.2.0](https://github.com/Procybit/Ky3m/releases/tag/v0.2.0) (2022-08-16) - General Functionality Phase

Transition to the General Functionality Phase.

All planned methods have been implemented.

The main goal of subsequent releases (up to release [0.3.0](https://github.com/Procybit/Ky3m/releases/tag/v0.3.0)) will be to improve all existing methods.

## [Release 0.1.2](https://github.com/Procybit/Ky3m/releases/tag/v0.1.2) (2022-08-15)

### Fixed

- Updated RELEASE'ed .jar filename generator (https://github.com/Procybit/Ky3M/issues/3 fix)

### Added

- Redesigned generic exceptions handling

## [Release 0.1.1](https://github.com/Procybit/Ky3M/releases/tag/v0.1.1) (2022-08-09)

### Fixed

- Enhanced extractor's mcmod.info finder (https://github.com/Procybit/Ky3M/issues/1 fix)
- Fixed error when ADOPTS couldn't find saved .jar files

### Changed

- Enabled generic exceptions handling (previously disabled) that occur when the user interacts incorrectly with the CLI.
- RELEASE method now generates more unique filenames (using gmttime)

## [Release 0.1.0](https://github.com/Procybit/Ky3M/releases/tag/v0.1.0) (2022-08-08) - Basic Functionality Phase

- First official project release
