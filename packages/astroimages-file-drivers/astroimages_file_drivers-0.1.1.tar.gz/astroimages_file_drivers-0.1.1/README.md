AstroImages Generic File Handling routines (astroimages-file-drivers)
=================================
![Version](https://img.shields.io/badge/version-0.1.1-blue.svg?cacheSeconds=2592000)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)
![Build Test](https://github.com/AstroImages/astroimages-file-drivers/workflows/Build%20Test%20(astroimages-file-drivers)/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=AstroImages_astroimages-file-drivers&metric=alert_status)](https://sonarcloud.io/dashboard?id=AstroImages_astroimages-file-drivers)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/AstroImages/astroimages-file-drivers.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/AstroImages/astroimages-file-drivers/context:python)

Generic file handling routines and wrappers


Usage
-----

Clone the repo:

```console
$ git clone https://github.com/AstroImages/astroimages-file-drivers/
$ cd astroimages-file-drivers
```

Create virtualenv:

```console
$ virtualenv -p python3 env
$ source env/bin/activate
(env) $ pip3 install -r requirements.txt
```

## Testing

To run unit tests:

```console
(env) $ python -m unittest discover test/unit -v
```

## Packaging

To package
    
```console
(env) $ python setup.py sdist
```

To upload

```console
(env) $ pip3 install twine
(env) $ twine upload dist/*
```

## References

- https://stackoverflow.com/questions/41984750/download-file-from-amazon-s3-using-rest-api

License
-------

MIT, see LICENSE file


