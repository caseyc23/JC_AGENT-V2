# Changelog

All notable changes to JC-Agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enterprise-grade documentation with professional standards
- Comprehensive API documentation with OpenAPI/Swagger support
- Docker containerization support
- System service templates (systemd, Windows Service)
- Performance benchmarking guidelines
- Security best practices documentation
- Code quality tooling setup (flake8, mypy, black, isort)
- Contribution guidelines
- Development environment setup documentation

### Changed
- Transformed documentation from consumer-friendly to enterprise-grade
- Removed emojis and casual language throughout codebase
- Updated README with technical specifications
- Enhanced API endpoint documentation

### Fixed
- Documentation consistency across all files
- Professional naming conventions applied

### Added
- 2026-01-11: Secure secrets handling, test coverage improvements, and CI workflow
	- Add `jc/secrets.py` helper to load local `.env` and prefer `OPENAI_API_KEY` over `OPENROUTER_API_KEY`.
	- Wire core modules (`jc.research`, `jc.self_awareness`, `jc.llm_provider`) to use the helper.
	- Add `.env.example` and README guidance for secure secrets handling.
	- Add focused unit tests for JC internals and settings GUI helpers to raise coverage.
	- Add GitHub Actions CI workflow to run `pytest -q` and preserve coverage artifacts.

## [1.0.0] - 2025-12-31

### Added
- Initial release of JC-Agent framework
- FastAPI REST API server with async support
- Multi-provider LLM integration (OpenRouter, Ollama, OpenAI, HuggingFace)
- Core orchestration engine
- Learning and memory management system
- Natural language voice interface
- Web research and data aggregation capabilities
- Capability introspection and honesty module
- Cross-platform desktop application
- System tray integration for Windows
- Comprehensive configuration management
- Example environment configuration
- Windows installer scripts
- Automated startup configuration
- Professional chat interface with modern UI
- Complete deployment guides

### Security
- Encrypted credential management
- Secure API key handling
- Local-first architecture
- Environment-based configuration

## [0.9.0] - 2025-12-30

### Added
- Initial project structure
- Core agent modules
- Basic API endpoints
- Development environment setup

### Changed
- Refined agent capabilities
- Improved system integration

---

## Version Numbering

Given a version number MAJOR.MINOR.PATCH, increment the:

1. MAJOR version when making incompatible API changes
2. MINOR version when adding functionality in a backwards compatible manner
3. PATCH version when making backwards compatible bug fixes

Additional labels for pre-release and build metadata are available as extensions to the MAJOR.MINOR.PATCH format.

## Release Process

1. Update version numbers in relevant files
2. Update this CHANGELOG.md
3. Create a release branch
4. Run full test suite
5. Create git tag
6. Push to repository
7. Create GitHub release with release notes

## Categories

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities
