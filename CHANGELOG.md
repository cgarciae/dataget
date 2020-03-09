# Changelog

## [0.4.6] - 2020-03-09
### Adds
- Adds the `vision.imagenet` dataset.

## [0.4.5] - 2020-03-05
### Adds
- Adds the `vision.fashion_mnist` dataset.
### Changes
- Changes download progress smoothing parameters.


## [0.4.4] - 2020-03-05
### Adds
- Adds the `vision.cifar10` and `vision.cifar100` datasets.
### Changes
- Improves docs for `toy.spirals` and `vision.mnist` datasets.
- Improves download progressbar info.


## [0.4.3] - 2020-03-04
### Changes
- `Dataset.is_valid` is not longer an abstract method. Its concrete implementation checks for the existance of a `self.path / ".valid"` which is set after `download` is called succesfully.


## [0.4.2] - 2020-02-22
### Adds
- Added `toy.spirals` dataset.
