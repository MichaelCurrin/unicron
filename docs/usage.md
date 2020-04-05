# Usage
> How to manage Unicron tasks and logs on the command-line


If you have setup crontab as per [Installation](installation.md) guide, then Unicron will run several time daily. Check output using [Mail](#mail) section below.

You can run a task through Unicron. Do this manually or by adding a command to crontab - see [Run main script](#run-main-script).

You can use the commands here to [View logs](#view-logs) to see the history of tasks and to see detailed errors from your task runs.


## Mail

If there are errors, the `mail` utility will you in the terminal, without having to run anything.

You can view mails using `mail` command as below.

```sh
mail
"/var/mail/my-user": 60 messages 60 unread
>U  1 my-user@host  Sat Mar 28 16:15  15/666   "Unicron task failed!"
```

## Unicron commands

Run these commands from the repo root.


### See Makefile help

```bash
$ make help
```

### Run main script

Run by hand.

This step uses the verbose mode. This is so that INFO and DEBUG messages that would normally be hidden from printing are still shown on the console.

The example output below is for the script which was setup using [Installation](installation.md) instructions.

- First run.
    ```bash
    $ make run
    unicron/unicron.py -v
    2020-01-13 22:49:12,770 INFO:unicron.py unicron - Task count: 1
    2020-01-13 22:49:12,770 DEBUG:unicron.py hello.sh - Executing, since no run record found.
    2020-01-13 22:49:12,781 INFO:unicron.py hello.sh - Success.
    2020-01-13 22:49:12,781 INFO:unicron.py unicron - Suceeded: 1; Failed: 0; Skipped: 0
    ```
- Second run.
    ```bash
    $ make run
    unicron/unicron.py -v
    2020-01-13 22:49:30,438 INFO:unicron.py unicron - Task count: 1
    2020-01-13 22:49:30,438 INFO:unicron.py hello.sh - Skipping, since already ran today.
    2020-01-13 22:49:30,438 INFO:unicron.py unicron - Suceeded: 0; Failed: 0; Skipped: 1
    ```

Once _Unicron_ has attempted all tasks, if any task failed then _Unicron_ will exit with an error status. This can be useful for control flow when using cron and `mail`. If running through `make`, the error will appear as follows:

```
...
make: *** [run] Error 1
```

### View logs

Run this command to tail the app and task logs. Sample output is for the run commands above.

```
$ make log
==> output/hello.sh.log <==

2020-01-13 22:49:12,770 INFO:unicron.py - Executing...
2020-01-13 22:49:12,782 INFO:unicron.py - Output:
    Hello world!


==> app.log <==
2020-01-13 22:49:12,770 INFO:unicron.py unicron - Task count: 1
2020-01-13 22:49:12,770 DEBUG:unicron.py hello.sh - Executing, since no run record found.
2020-01-13 22:49:12,781 INFO:unicron.py hello.sh - Success.
2020-01-13 22:49:12,781 INFO:unicron.py unicron - Suceeded: 1; Failed: 0; Skipped: 0
2020-01-13 22:49:30,438 INFO:unicron.py unicron - Task count: 1
2020-01-13 22:49:30,438 INFO:unicron.py hello.sh - Skipping, since already ran today.
2020-01-13 22:49:30,438 INFO:unicron.py unicron - Suceeded: 0; Failed: 0; Skipped: 1
```
