# Development


## Setup
> Setup Unicron locally

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
> Run checks locally

### Format and lint

Format Python files and run linting checks.

```bash
$ make fmt
```

### Tests

Run unit tests.

```bash
$ make unit
```


## CI
> Run Github Actions on the project

See the [main.yml](https://github.com/MichaelCurrin/unicron/blob/master/.github/workflows/main.yml) workflow file in the repo.

This sets up checks to run on Github Actions.

Nothing is persisted - the project is not packaged and distributed anywhere.


## Docs site

Built on [DocsifyJS](docsify.js.org/).

### Locally

Requires Node.js installed.

Optionally install [Docsify CLI](https://www.npmjs.com/package/docsify-cli).

```bash
$ npm install -g docsify-cli
```

If you don't install it, it will be downloaded with `npx` in the next command but not installed.

Run local docs server from the project root:

```bash
$ make docs
```

### Remote

Start serving as a Github Pages or Netlify site, serving from the docs directory.

No build command is needed.
