# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
## Added
- Meta: Locked dependencies via `poetry.lock` file in version control

### Changed
- Meta: Replace setuptools with poetry for packaging and dependency management

### Removed
- Support for Python 3.4 (EOL)

## [1.3.3] - 2019-05-20
### Fixed
- setup.py failing for Python 2.7. #41

### Added
- Test run of setup.py in develop mode for installing requirements, sanity check. Relates to #41

## [1.3.2] - 2019-05-20
### Fixed
- README failed parsing in non utf-8 environments. Enforce encoding. #37

## [1.3.1] - 2019-05-19
### Added
- Travis CI test support for Python 3.6, and 3.7
- More project metadata to properly list on PyPi

### Removed
- Travis CI test runs for Python 2.6, and 3.3

### Changed
- Requirement for jsonschema library extended to version `<4`
- Conform to Black codestyle
- Move unittests to `tests/` directory

### Fixed
- README formatting (codeblocks showing correctly)

## [1.3.0] - 2016-06-25

## [1.2.0] - 2015-10-12

## [1.1.0] - 2013-11-19

## [1.0.1] - 2013-06-28

## [1.0.0] - 2013-04-26

## [0.8.2] - 2013-03-25

## [0.8.1] - 2013-01-31

## [0.8.0] - 2013-01-21

## [0.7.0] - 2012-11-26

[Unreleased]: https://github.com/bcwaldon/warlock/compare/v1.3.3...HEAD
[1.3.3]: https://github.com/bcwaldon/warlock/compare/v1.3.2...v1.3.3
[1.3.2]: https://github.com/bcwaldon/warlock/compare/v1.3.1...v1.3.2
[1.3.1]: https://github.com/bcwaldon/warlock/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/bcwaldon/warlock/compare/1.2.0...1.3.0
[1.2.0]: https://github.com/bcwaldon/warlock/compare/1.1.0...1.2.0
[1.1.0]: https://github.com/bcwaldon/warlock/compare/1.0.1...1.1.0
[1.0.1]: https://github.com/bcwaldon/warlock/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/bcwaldon/warlock/compare/0.8.2...1.0.0
[0.8.2]: https://github.com/bcwaldon/warlock/compare/0.8.1...0.8.2
[0.8.1]: https://github.com/bcwaldon/warlock/compare/0.8.0...0.8.1
[0.8.0]: https://github.com/bcwaldon/warlock/compare/0.7.0...0.8.0
[0.7.0]: https://github.com/bcwaldon/warlock/releases/tag/0.7.0
