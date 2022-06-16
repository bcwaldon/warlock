# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2022-06-16
### Added
- Meta: Locked dependencies via `poetry.lock` file in version control. #44
- Meta: Add [pre-commit](https://pre-commit.com) config to enforce code styling and file formatting. #43
- Meta: Add [tox](https://tox.readthedocs.io/en/latest/index.html) config for test automation across Python versions. #47
- Tests for DeprecationWarnings issued for `Model.changes`. #46
- Cache the validator instance to speedup schema validation process. #55
- Support for jsonschema 4.x. #65
- Support for Python 3.9, 3.10. #65

### Fixed
- Fixed DeprecationWarnings for using `assertEquals` in tests. #45

### Changed
- Meta: Replace setuptools with poetry for packaging and dependency management. #35
- Changed behavior of `model_factory` back to pre-1.3 call signature. #39

### Removed
- Support for Python 3.4 (EOL). #44
- Support for Python 3.5, 3.6 (EOL). #65
- Support for Python 2.7 (EOL by 2019-01-01). #48

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

[Unreleased]: https://github.com/bcwaldon/warlock/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/bcwaldon/warlock/compare/v1.3.3...v2.0.0
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
