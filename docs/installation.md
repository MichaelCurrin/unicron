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


## Setup Unicron tasks

_Unicron_ will run tasks for you if you set it up.

Follow instructions below to add add executables (or symlinks to executables) in the _targets_ directory. You might want to actually the example script as below - you can use it to confirm Unicorn works as expected and see what output it gives.

1. Start from the repo root.
2. Create a script and make it executable. e.g.
    ```bash
    $ echo -e '#!/bin/bash\necho "Hello world!"\n' > unicron/var/targets/hello.sh
    $ chmod +x unicron/var/targets/hello.sh
    ```
3. Run the script directly to check that it works fine. e.g
    ```bash
    $ unicron/var/targets/hello.sh
    Hello world!
    ```

Repeat setup for all tasks that you want automated through _Unicron_. Once you have one executable script setup, you can easily copy the file for each new task.


## Setup a single cron job

<!-- TODO move command above to SH script -->

<!-- TODO: Make executable without cd then update here. Also consider if make should be used here. -->

<!-- TODO: Repeat scheduling this in the usage/config section in more detail with `crontab -e`. -->


You only need to add a **single** _Unicron_ item to _crontab_, regardless of how many task you have configured in _Unicron_.

Follow instructions below to configure _crontab_ to run the main _Unicron_ script at an interval throughout the day.

### Frequency

Pick a frequency - such as every 30 minutes (`*/30`) or every hour (`0`). This could be more frequent, but there is not much benefit, as Unicron is aimed at scripts that only run once per day and when the time doesn't matter. So as long as you are online _sometime_ for 30 minutes to an hour during a day and then turn your laptop off, you'll get your tasks to run.

Example:

```
*/30    *       *       *       *
```

### Script name

Use this as the cron command:

- `~/repos/unicron/unicron.py`

You could use just `unicron.py` instead, but then you need to make sure that the bin directory is in the `PATH` value in crontab config.


### Verbosity

Omit the `--verbose` flag so that Unicron will **only** send an email if there is an error. Note that app and task runs _always_ go to the log files, in case mails are quiet from successes but you still want to check history and output.

If there are any errors, they will appear in the [Mail](mail.md) utility.


### Put it all together

```sh
$ crontab -e
```

Sample crontab config:

```
SHELL=/bin/bash
PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
MAILTO=$USER

*/30    *       *       *       *       ~/repos/unicron/unicron.py
```


#### Note for macOS

After updating macOS to Catalina, I found that `crontab` would **not** send mail, for _Unicron_ or anything else. Even when the task has actually run and when `mail` command works alone.

But I found the solution below does work. Assuming sending using `MAILTO` does not work, or is disabled globally or inline as `MAILTO=''`.


```
MAILTO=''
*/30    *       *       *       *       RESULT="$(cd ~/repos/unicron/unicron && ./unicron.py 2>&1)"; \
                                          if [[ $? -ne 0 ]]; then echo "$RESULT" | mail -s 'Unicron task failed!' $USER
```

There might be a more efficient way, but this captures stdout and stderr as a variable. If there is any content in the variable, send a `mail`. We send the content to the `mail` command and set the subject and target user.
