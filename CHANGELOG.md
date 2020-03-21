# Changelog

## [0.4.9] - 2020-03-21
### Adds
- Adds the `image.udacity_simulator` dataset.

## [0.4.8] - 2020-03-17
### Adds
- Adds the `audio.free_spoken_digit` dataset.

## [0.4.7] - 2020-03-10
### Adds
- Adds the `structured.movielens_*` dataset family.
- Add the `text.imdb_reviews` dataset. 
### Changes
- `get` method is now strict with all arguments.

## [0.4.6] - 2020-03-09
### Adds
- Adds the `image.imagenet` dataset.

## [0.4.5] - 2020-03-05
### Adds
- Adds the `image.fashion_mnist` dataset.
### Changes
- Changes download progress smoothing parameters.


## [0.4.4] - 2020-03-05
### Adds
- Adds the `image.cifar10` and `image.cifar100` datasets.
### Changes
- Improves docs for `toy.spirals` and `image.mnist` datasets.
- Improves download progressbar info.


## [0.4.3] - 2020-03-04
### Changes
- `Dataset.is_valid` is not longer an abstract method. Its concrete implementation checks for the existance of a `self.path / ".valid"` which is set after `download` is called succesfully.


## [0.4.2] - 2020-02-22
### Adds
- Added `toy.spirals` dataset.
