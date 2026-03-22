# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.4] - 2024-01-XX

### Added
- **CHANGELOG.md**: Added comprehensive changelog to track all version changes
- **Improved Documentation**: Enhanced README.md with corrected examples and clearer explanations

### Fixed
- **Clone Method Bug**: Fixed `clone()` method in both `classdef` and `structdef` to return a new instance instead of a dictionary
- **Static Method Validation**: Fixed bug where static method validation used incorrect attribute name (`__methods__` instead of `__interface__.methods`)
- **Documentation Errors**: 
  - Fixed grammatical error in version notice ("wrong metadata" → "incorrect metadata")
  - Removed misleading statement about `InterfaceError` not being exported
  - Fixed subject-verb agreement ("parent constructor are" → "parent constructor is")
  - Corrected misleading comment about `to_string` being a "built-in method" (now says "overrides default behavior")
  - Fixed method signatures in examples to match actual implementation (removed `self` from static methods)
  - Changed parameter names from `other` to `object` in interface definitions for consistency

### Changed
- **Version Updates**: Updated version number from 1.0.3 to 1.0.4 in both `pyproject.toml` and `mbpc/__init__.py`
- **Code Quality**: Improved code consistency and fixed validation logic

### Technical Details
- The `clone()` method now properly creates a new instance of the class/struct with a deep copy of all attributes
- Static method validation now correctly checks against `interface.__interface__.methods` instead of the non-existent `interface.__methods__`
- All documentation examples now reflect the actual behavior of the library

## [1.0.3] - 2024-01-XX

### Removed
- This version was permanently removed from PyPI due to documentation errors

## [1.0.2] - 2024-01-XX

### Removed
- This version was permanently removed from PyPI due to documentation errors

## [1.0.1] - 2024-01-XX

### Removed
- This version was permanently removed from PyPI due to documentation errors

## [1.0.0] - 2024-01-XX

### Removed
- This version was permanently removed from PyPI due to documentation errors

---

**Note**: Versions 1.0.0 through 1.0.3 were removed from PyPI due to trivial bugs including invalid example code in documentation and incorrect metadata. Version 1.0.4 is the first stable, properly documented release.