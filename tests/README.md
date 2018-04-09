# Inkscape Extension Tests

This folder contains tests for the Inkscape extensions and libraries in this
repo.

> **NOTE:** As of 2018-04-08, `tests.test_coverage.ScriptCoverageTest` fails
> because of untested modules. All other tests should pass.

To run all tests:

```shell
# In the top-level directory of the extensions repo:
$ python2 setup.py test
$ python3 setup.py test
```

To run the tests in a specific file (in this case,
`tests/test_inkex_effect.py`):

```shell
# In the top-level directory of the extensions repo:
$ python2 setup.py test --test-suite=tests.test_inkex_effect
$ python3 setup.py test --test-suite=tests.test_inkex_effect
```
