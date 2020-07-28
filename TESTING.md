# Why Test Extensions

Previously, Inkscape extensions were not tested for quality or correctness. But since 1.0 the extensions repository is far more strict about requiring tests and requiring tests to pass before changes can be merged in.

You may find yourself being frustrated by the tests, especially if at first it doesn't make sense why they are failing. But these tests are important and I ask that everyone be as kind as they can to make sure the quality of the repository is maintained.

# Running Tests

You must install the program `pytest` in order to run these tests. You may run all tests by ommitting any other paramiters or select tests by adding the test filename that you want to run.

    pytest
    pytest tests/test_my_extension.py

You can also run tests until the first time the fail, and ask pytest to run the previously failed tests first. This can be useful in cutting down how long pytest takes to run before hitting a failure.

    pytest -x --ff

# Test Files

Each extension should have it's own test file in the tests directory. This test may be a series of function tests or they may be "comparison" tests. The comparison tests will fail whenever the output of an extension changes, so often they will need to be updated to reflect your changes.

Usually the test file will be named `tests/test_{name_of_extension}.py` using the same name as the extension file itself. For tests covering inkex and other modules you may find test files have the format `tests/test_{package}_{module}.py` or similar.

Each test can be run independently as shown in the previous section.

# Test Data

As well as test python files, each test will normally depend on additional data. From source svg files, to output comparision tests and other such things.

This data is always held in `tests/data`, when writing tests, please make sure your data goes into the right directory. If you are updating the comparison test, ususally you just need to rename the `export` file generated and remove the `.export` suffix to enable it.

See tests/data/README.md for further information.

# Writing or Updating tests

To learn how to write tests, or what the test code means. You need to read the documentation available inside the tester module. From a python3 terminal type:

    from inkex import tester
    help(tester)

# Coverage

Coverage reports tell us how much of an extension is being exercised when tests are run.

The latest coverage report for master branch can be found at
https://inkscape.gitlab.io/extensions/coverage/.

To run a complete coverage report, you can specify the `--cov=.` option like so:

    pytest --cov=. --cov-report term

For a single extension coverage report, you can limit it further with:

    pytest --cov=my_extension.py --cov-report term

## Testing Options

Tests can be run with these options that are provided as environment variables:

    FAIL_ON_DEPRECATION=1 - Will instantly fail any use of deprecated APIs
    EXPORT_COMPARE=1 - Generate output files from comparisions. This is useful for manually checking the output as well as updating the comparison data.
    NO_MOCK_COMMANDS=1 - Instead of using the mock data, actually call commands. This will also generate the msg files similar to export compare.
    INKSCAPE_COMMAND=/other/inkscape - Use a different Inkscape (for example development version) while running commands. Works outside of tests too.
    XML_DIFF=1 - Attempt to output an XML diff file, this can be useful for debugging to see differences in context.
    DEBUG_KEY=1 - Export mock file keys for debugging. This is a highly specialised option for debuging key generation.

For example:

    EXPORT_COMPARE=1 pytest

or

    export EXPORT_COMPARE=1
    pytest

# Testing custom extensions

The same testing framework can be used in your own extension repositories by requiring the inkex module and using the inkex.tester module set which should be available with inkscape or can be installed via pypi.

This is a great way of ensuring you have access to the same tools inkscape uses to test as well as making it easier for your external extension to make its way to the core reopsitory without resistance.
