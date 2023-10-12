# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).


## [0.0.2] - 2023-10-12

### Added
- ValueErrors when UID, PID, or ENV_TYPE are not present in the environment.

### Changed
- create_engine() now is engine_factory()

### Removed
- SQL Builder functions
- Execution Functions

## [0.0.1] - 2023-09-12

### Added

- Insert functions for raw SQL & Pandas.
- Select functions for raw SQL & Pandas.
- Connection Manager to handle engines.
- Query builders for select & insert operations.
- Good examples and basic guidelines, including proper date formatting.