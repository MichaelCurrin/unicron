# Installation
> How to install Unicron


## System dependencies

### Install Python 3

[install_python_3.md](//gist.githubusercontent.com/MichaelCurrin/57caae30bd7b0991098e9804a9494c23/raw/install_python_3.md ':include')

### Install Crontab

I found this is installed usually on a fresh macOS or Linux setup.

Otherwise follow instructions below to install.

On Debian/Ubuntu:

```bash
$ sudo apt install python3-crontab
```


## Clone

```bash
$ git clone git@github.com:MichaelCurrin/unicron.git
$ cd unicron
```


## Project dependencies

There are _no_ Python packages needed to run the main application.

But if you want to install and use the dev dependencies for local development, see the [Development](development.md) page.

If this is your first time using Unicron, you can skip ahead to the [Usage](usage.md) doc to see how to run Unicron. 


## Setup Unicron as a scheduled task

Continue to the [Setup cron](setup_cron.md) page to setup Unicron as scheduled item which manages your configured tasks.


## Setup as a bin script

Optionally allow _Unicron_ to be executable from anywhere.

1. Choose a bin directory that is in your `PATH`. e.g.
    - `/usr/local/bin` - Standard for Unix steps.
    - `~/bin` - This will need to be created and added to `PATH`.
2. Add a symlink to Unicron. e.g.
    ```bash
    $ cd <BIN_DIR>
    $ ln -s ~/repos/unicron/unicron/unicron.py
    ```
3. Test the script.
    ```bash
    $ cd ~
    $ unicron.py --help
    ...
    ```
