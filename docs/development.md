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

## Docs site

Built on [Docsify-JS](docsify.js.org/).

### Locally

Install [Docsify CLI](https://www.npmjs.com/package/docsify-cli):

```sh
npm install -g docsify-cli
```

Run local docs server from root:

```sh
make docs
```

### Remote

Start serving as a Github Pages or Netlify site, serving from the docs directory.

No build command is needed.
