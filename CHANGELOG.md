# Changelog

## [0.4.3] - 2020-03-04

### Changes

- `Dataset.is_valid` is not longer an abstract method. Its concrete implementation checks for the existance of a `self.path / ".valid"` which is set after `download` is called succesfully.

## [0.4.2] - 2020-02-22

### Adds

- Added `toy.spirals` dataset.
