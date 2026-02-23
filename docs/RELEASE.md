# Release Process

## Versioning Strategy

Python Playground follows [Semantic Versioning](https://semver.org/) (SemVer):

- **MAJOR** version: Incompatible API changes
- **MINOR** version: New functionality in a backward-compatible manner
- **PATCH** version: Backward-compatible bug fixes

Format: `vMAJOR.MINOR.PATCH` (e.g., `v1.2.3`)

## Tagging Instructions

### Creating a Release Tag

1. **Update Version**:
   - Update version in `pyproject.toml`
   - Update `CHANGELOG.md` with release date

2. **Create Tag**:
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

3. **Automated Release**:
   - GitHub Actions will automatically create a release when a tag matching `v*` is pushed
   - The workflow reads release notes from `releases/RELEASE_NOTES_{tag}.md` or falls back to `CHANGELOG.md`

## Release Notes Process

### Option 1: Release Notes File (Recommended)

Create a file in `releases/` directory:
- **Filename**: `RELEASE_NOTES_v1.0.0.md`
- **Format**: Markdown
- **Content**: Detailed release notes for this version

### Option 2: CHANGELOG.md

The release workflow will extract notes from `CHANGELOG.md` if no release notes file exists.

Format in CHANGELOG.md:
```markdown
## [1.0.0] - YYYY-MM-DD

### Added
- Feature 1
- Feature 2

### Changed
- Improvement 1

### Fixed
- Bug fix 1
```

## Automated Release Workflow

When you push a tag matching `v*`:

1. **Workflow Triggered**: `.github/workflows/release.yml` runs
2. **Version Extraction**: Extracts version from tag (e.g., `v1.0.0`)
3. **Release Notes**: Looks for `releases/RELEASE_NOTES_{tag}.md`, falls back to `CHANGELOG.md`
4. **GitHub Release**: Creates a GitHub release with:
   - Tag name
   - Release title
   - Release notes body
   - Not marked as draft or prerelease

## Pre-Release Checklist

- [ ] All tests passing
- [ ] CHANGELOG.md updated
- [ ] Version updated in `pyproject.toml`
- [ ] Release notes prepared (optional but recommended)
- [ ] Documentation reviewed
- [ ] No breaking changes (or documented)
- [ ] Dependencies up to date

## Post-Release

- [ ] Verify release created on GitHub
- [ ] Check release notes rendered correctly
- [ ] Update any external documentation
- [ ] Announce release (if applicable)

## Emergency Releases

For critical security fixes:

1. Create patch version
2. Tag immediately
3. Document in SECURITY.md
4. Follow standard release process

## Example Release Workflow

```bash
# 1. Update version in pyproject.toml
# 2. Update CHANGELOG.md
git add pyproject.toml CHANGELOG.md
git commit -m "Release: v1.0.0"
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main
git push origin v1.0.0
```

The GitHub Actions workflow will handle the rest automatically.

