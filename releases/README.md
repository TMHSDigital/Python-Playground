# Releases Directory

## Purpose

This directory contains release notes for specific versions of Python Playground. Release notes provide detailed information about what changed in each release.

## Structure

Release notes files follow this naming convention:

```
RELEASE_NOTES_v{VERSION}.md
```

Examples:
- `RELEASE_NOTES_v1.0.0.md`
- `RELEASE_NOTES_v1.2.3.md`
- `RELEASE_NOTES_v2.0.0.md`

## Release Notes Format

Each release notes file should include:

1. **Version Header**: Clear version number and release date
2. **Summary**: Brief overview of the release
3. **Added**: New features and additions
4. **Changed**: Changes to existing functionality
5. **Fixed**: Bug fixes
6. **Removed**: Deprecated or removed features
7. **Migration Guide**: If there are breaking changes

Example structure:

```markdown
# Release Notes v1.0.0

**Release Date**: YYYY-MM-DD

## Summary

Initial stable release of Python Playground with core examples and documentation.

## Added

- Core Python examples
- Data structures implementations
- Basic testing framework

## Changed

- Improved documentation structure

## Fixed

- Resolved documentation typos

## Migration Guide

No migration needed for initial release.
```

## Release Workflow Process

1. **Before Release**:
   - Create release notes file: `RELEASE_NOTES_v{VERSION}.md`
   - Document all changes comprehensively
   - Include migration guides for breaking changes

2. **During Release**:
   - Tag the release: `git tag -a v{VERSION} -m "Release v{VERSION}"`
   - Push tag: `git push origin v{VERSION}`
   - GitHub Actions automatically creates the release using these notes

3. **After Release**:
   - Verify release notes appear correctly on GitHub
   - Link to release notes in CHANGELOG.md if desired

## Fallback to CHANGELOG.md

If a release notes file doesn't exist for a version, the automated release workflow will extract notes from `CHANGELOG.md` instead. However, dedicated release notes files are recommended for major releases as they provide more space for detailed explanations.

## Best Practices

- **Be Descriptive**: Provide enough detail for users to understand changes
- **Include Examples**: Show code examples for new features
- **Document Breaking Changes**: Clearly mark and explain any breaking changes
- **Link Issues**: Reference related issues and pull requests
- **Thank Contributors**: Acknowledge contributors in the release notes

## Questions?

If you have questions about the release process, see `docs/RELEASE.md` for detailed instructions.

