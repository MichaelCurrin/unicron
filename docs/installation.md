# Installation
> How to install Unicron


## System dependencies

- Install [Python 3](https://python.org/)
- Install _crontab_
    - This is available for macOS and Linux and so might be installed already.


## Clone

```bash
$ git clone git@github.com:MichaelCurrin/unicron.git
$ cd unicron
```


## Project dependencies

There are _no_ project dependencies needed to run the main application.

I you want to install and use the dev dependencies for local development, see the [Development](development.md) page.


Run Unicron directly to test that it runs.

- Using _Python_
    ```sh
    $ cd ~/repos/unicron/unicron
    $ ./unicron.py --help
    ```
- Using `make`.
    ```sh
    $ cd ~/repos/unicron/
    make usage
    ```

## Run as a bin script

Optionally allow _Unicron_ to be executable from anywhere.

1. Choose a bin directory that is in your `PATH`. e.g.
    - `/usr/local/bin` - Standard for Unix steps.
    - `~/bin` - This will need to be created and added to `PATH`.
2. Add a symlink to Unicron. e.g.
    ```sh
    $ cd <BIN_DIR>
    $ ln -s ~/repos/unicron/unicron/unicron.py
    ```
3. Test the script.
    ```sh
    $ cd ~
    $ unicron.py --help
    ...
    ```

Continue to the [Setup cron](setup_cron.md) page.
