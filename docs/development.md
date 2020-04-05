# Development

## Setup

Create a virtual environment at the project root and activate it.

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

Install dev dependencies.

```bash
$ make dev-install
```

## Checks

Format Python files and run linting checks.

```bash
$ make check
```

Run tests script.

```bash
$ make test-output
```
