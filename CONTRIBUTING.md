# Contributing guidelines

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Pull Request Checklist

Before sending your pull requests, make sure you followed this list.

- [ ] Contributing guidelines were read.
- [ ] Changes are consistent with the guidelines.
- [ ] All unit tests passes.

## How to become a contributor and submit your own code
### Contributing code

If you have improvements to aegis, send us your pull requests! For those
just getting started, Github has a [howto](https://help.github.com/articles/using-pull-requests/).

If you want to contribute, start working through the aegis codebase,
navigate to the
[Github "issues" tab](https://github.com/mgurdal/aegis/issues) and start
looking through interesting issues. If you are not sure of where to start, then
start by trying one of the smaller/easier issues here i.e.
[issues with the "good first issue" label](https://github.com/mgurdal/aegis/labels/good%20first%20issue).
If you decide to start on an issue, leave a comment so that other people know that
you're working on it. If you want to help out, but not alone, use the issue
comment thread to coordinate.

### Contribution guidelines and standards

Before sending your pull request for
[review](https://github.com/mgurdal/aegis/pulls),
make sure your changes are consistent with the guidelines and follow the
aegis coding style.

#### General guidelines and philosophy for contribution

*   Include unit tests when you contribute new features, as they help to a)
    prove that your code works correctly, and b) guard against future breaking
    changes to lower the maintenance cost.
*   Bug fixes also generally require unit tests, because the presence of bugs
    usually indicates insufficient test coverage.
*   Keep API compatibility in mind when you change code. aegis has reached version 1 
    and hence cannot make non-backward-compatible API changes without a major release. 
    You can run unit(test.py) and integration(cli.py) tests in [examples](https://github.com/mgurdal/aegis/tree/master/examples) 
    to make sure about the compatibility.
*   When you contribute a new feature to aegis, the maintenance burden is
    (by default) transferred to the project owner. This means that benefit of
    the contribution must be compared against the cost of maintaining the
    feature.

#### Python coding style

Use `black` to format your code. To install `black`:

```bash
pip install black
```

To format with `black`:

```bash
black .
```

#### Running unit tests

We expect you to use a python virtual environment while running your tests. 
You can use your favorite python virtual environment.

Here is an example with `virtualenv`:

**Create a virtual environment**
```bash
cd aegis
virtualenv --python=`which python3` venv
. venv/bin/activate
```

**Install required libraries for development**
```bash
pip install -r equirements/dev.txt
```

**Run aegis test suite**
```bash
make test
```
The command at first will run the flake8 tool (sorry, we don’t accept pull requests with pep8 or pyflakes errors).

After flake8 succeeds the tests will be run.

Please take a look on the produced output.

Any extra texts (print statements and so on) should be removed.

**Test coverage**
```bash
make cov
```

Once the command has finished check your coverage
```bash
python -m http.server -d htmlcov
```

#### Documentation

We encourage documentation improvements. 

We use `mkdocs` to generate our documentation pages.

Please before making a Pull Request about documentation changes run:

```bash
mkdocs build
```

#### Making a Pull Request

After finishing all steps make a GitHub Pull Request with master base branch.

