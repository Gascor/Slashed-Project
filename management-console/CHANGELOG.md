# Changelog

All notable changes to this project will be documented in this file.

## [0.0.123a] - 2025-01-10

### Added +
- Added a new "Game Servers" tab to the `AdminPanel` to display a list of game servers.
- Implemented server status indicators (green, red, yellow) in the "Game Servers" tab.
- Added controls to restart and shutdown game servers in the "Game Servers" tab.
- Integrated API call to fetch the list of game servers and their statuses.
- Added periodic updates for server statuses in the "Game Servers" tab.

### Changed #
- Organized the layout of the "Game Servers" tab using `QHBoxLayout` to separate the server list and controls.
- Improved error handling and logging for API calls in the "Game Servers" tab.

### Fixed ~
- Fixed issues with the application icon not appearing correctly in the compiled version.
- Fixed various UI layout issues in the `AdminPanel`.

### Removed -
- N/A

## [0.0.114a] - 2025-01-04

### Added +
- Separated `LoginDialog` and `AdminPanel` classes into their respective files.
- Added functionality to set the application icon from `resources/app.ico`.
- Added environment variable loading from `.env` file for database credentials.

### Changed #
- Updated `AdminPanel` to correctly use `QFileDialog.Options` for importing SQL scripts.
- Improved error handling and logging for database connections and SQL script execution.

### Fixed ~
- Fixed issues with `QFileDialog` options in `AdminPanel`.
- Fixed missing `os` import in `login_dialog.py`.
- Fixed `TypeError` in `LoginDialog` constructor.

### Removed -
- N/A

## [0.0.102a] - 2025-01-03

### Added +
- Initial implementation of the Management Console.
- Login functionality with username and password.
- Database connection using `pymysql`.
- System monitoring with CPU, RAM, and network usage.
- SQL script import and execution.
- Database reset functionality.

### Changed #
- Switched from `mysql-connector-python` to `pymysql` for database interactions.

### Fixed ~
- Fixed issues with resource paths for images.
- Fixed segmentation fault issues during compilation with Nuitka.

### Removed -
- N/A

## [0.0.101] - 2024-12-29

### Added +
- Initial setup and project structure.
- Basic UI components and layout.

### Changed #
- N/A

### Fixed ~
- N/A

### Removed -
- N/A

## [0.0.100] - 2024-12-23

### Added +
- Project initialization.
- Basic dependencies and environment setup.

### Changed #
- N/A

### Fixed ~
- N/A

### Removed -
- N/A