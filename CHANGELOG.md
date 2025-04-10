# Changelog

All notable changes to the SmallProxy project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2023-04-10

### Added
- Initial release of SmallProxy
- Dual port architecture (8888 for proxy, 5000 for web interface)
- Filter management UI with whitelist/blacklist modes
- Real-time log monitoring with color-coded log entries
- Default blacklist and whitelist configurations
- Modern responsive UI built with Tailwind CSS
- Docker containerization for easy deployment

### Changed
- Modified log colorization to show "Proxying refused on filtered domain" messages in orange (log-line-block class) instead of red

### Fixed
- Proper handling of log file rotation in UI 