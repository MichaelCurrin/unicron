# Usage
> How to use Unicron to run tasks, manage tasks and view logs

The commands in this guide are all run with `make` and should be run from the root directory.

The main things you to do with _Unicron_ are:

- Run tasks
    - You can [run tasks](#run-tasks) through Unicron directly, either manually (does not require crontab setup) or by adding a Unicron run command to crontab (see [Installation](installation.md) guide).
- View logs
    - You can use commands here to [View logs](#view-logs) to see the history of tasks and to see detailed errors from your task runs.


## Available make commands

<details>
<summary>
    
Click to expand.

```bash
$ make help
```

</summary>

[Makefile](https://raw.githubusercontent.com/MichaelCurrin/unicron/master/Makefile ':include :type=code')

</details>


## View configured tasks

### Main

```bash
$ make ls-tasks
```

### Test

```bash
$ make ls-test-tasks
```
```
-rwxr-xr-x  1 user  151928526  84  7 Feb 13:18 fail.sh
-rwxr-xr-x  1 user  151928526  21  7 Feb 13:18 never_run_before.sh
-rw-r--r--  1 user  151928526  13  7 Feb 13:18 not_executable.sh
-rwxr-xr-x  1 user  151928526  21  7 Feb 13:18 old.sh
-rwxr-xr-x  1 user  151928526  21  7 Feb 13:18 today.sh
```


## Run tasks

This step uses the verbose mode. This is so that _INFO_ and _DEBUG_ messages that would normally be hidden from printing are still shown on the console.

### Main

The example output below is for the demo script which was setup using [Installation](installation.md) instructions.

- First run.
    ```bash
    $ make run
    ```
    ```
    unicron/unicron.py -v
    2020-04-05 10:00:00,414 INFO:unicron.py unicron - Task count: 1
    2020-04-05 10:00:00,429 DEBUG:unicron.py hello.sh - Executing, since last run date is old.
    2020-04-05 10:00:02,224 INFO:unicron.py hello.sh - Success.
    2020-04-05 10:00:02,300 INFO:unicron.py unicron - Suceeded: 1; Failed: 0; Skipped: 0
    ```
- Second run.
    ```bash
    $ make run
    ```
    ```
    unicron/unicron.py -v
    2020-04-05 10:10:00,414 INFO:unicron.py unicron - Task count: 1
    2020-04-05 10:10:00,429 INFO:unicron.py hello.sh - Skipping, since already ran today.
    2020-04-05 10:10:00,500 INFO:unicron.py unicron - Suceeded: 0; Failed: 0; Skipped: 1
    ```

Once _Unicron_ has attempted all tasks, if any task failed then _Unicron_ will exit with an error status. This can be useful for control flow when using cron and `mail`. If running through `make`, the error will appear as follows:

```
...
make: *** [run] Error 1
```


### Test

Without any custom tasks setup, you start test _Unicron_ immediately by running the versioned test tasks.

```bash
$ make run-test
```


## View task last run dates

### Main

```bash
$ make ls-runs
```

### Test

```bash
$ make ls-test-runs
```
```
cd unicron/_test_var/last_run/ && tail *
==> never_run_before.sh.txt <==
2020-04-05
==> old.sh.txt <==
2020-04-05
==> today.sh.txt <==
2020-04-05
```


## View logs

You can run commands through `make` to view logs and also _tail_ them in realtime - watch them continuously for new lines. Press <kbd>CTRL</kbd>+<kbd>C</kbd> to stop watching the logs.

Check [Makefile help](#see-makefile-help) then view the make targets which use "log" in the name and choose one.


### Main

Here we tail the task logs and app log as the same time. If you do this in one terminal tab and run tasks in the other, you can see the activity in the logs as it happens.

<details>
<summary>

Click to expand.

```bash
$ make log
```

</summary>

```
==> output/hello.sh.log <==

2020-01-13 22:49:12,770 INFO:unicron.py - Executing...
2020-01-13 22:49:12,782 INFO:unicron.py - Output:
    Hello world!

==> app.log <==
    2020-04-05 10:00:00,414 INFO:unicron.py unicron - Task count: 1
    2020-04-05 10:00:00,429 DEBUG:unicron.py hello.sh - Executing, since last run date is old.
    2020-04-05 10:00:02,224 INFO:unicron.py hello.sh - Success.
    2020-04-05 10:00:02,300 INFO:unicron.py unicron - Suceeded: 1; Failed: 0; Skipped: 0
    2020-04-05 10:10:00,414 INFO:unicron.py unicron - Task count: 1
    2020-04-05 10:10:00,429 INFO:unicron.py hello.sh - Skipping, since already ran today.
    2020-04-05 10:10:00,500 INFO:unicron.py unicron - Suceeded: 0; Failed: 0; Skipped: 1
```

</details>

### Test

<details>
<summary>

Click to expand.

```bash
$ make log-test
```

</summary>

```
cd unicron && tail -n20 -F _test_var/output/*.log _test_var/app.log

==> _test_var/output/fail.sh.log <==
2020-04-05 15:29:48,233 INFO:unicron.py - Executing...
2020-04-05 15:29:48,253 ERROR:unicron.py - Output:
    Printing to stdout.
    Oh no! Printing to stderr

==> _test_var/output/never_run_before.sh.log <==
2020-04-05 15:29:48,255 INFO:unicron.py - Executing...
2020-04-05 15:29:48,280 INFO:unicron.py - Output:
    Baz

==> _test_var/output/not_executable.sh.log <==
2020-04-05 15:29:48,281 INFO:unicron.py - Executing...
2020-04-05 15:29:48,293 ERROR:unicron.py - Output:
    /bin/sh: /Users/mcurrin/repos/unicron/unicron/_test_var/targets/not_executable.sh: Permission denied

==> _test_var/output/old.sh.log <==
2020-04-05 15:29:48,299 INFO:unicron.py - Executing...
2020-04-05 15:29:48,321 INFO:unicron.py - Output:
    Bar

==> _test_var/app.log <==
2020-04-05 15:29:48,232 INFO:unicron.py unicron - Task count: 5
2020-04-05 15:29:48,233 DEBUG:unicron.py fail.sh - Executing, since no run record found.
2020-04-05 15:29:48,253 ERROR:unicron.py fail.sh - Exited with error status! Check this task's log.
2020-04-05 15:29:48,253 DEBUG:unicron.py never_run_before.sh - Executing, since no run record found.
2020-04-05 15:29:48,279 INFO:unicron.py never_run_before.sh - Success.
2020-04-05 15:29:48,280 DEBUG:unicron.py not_executable.sh - Executing, since no run record found.
2020-04-05 15:29:48,290 ERROR:unicron.py not_executable.sh - Exited with error status! Check this task's log.
2020-04-05 15:29:48,298 DEBUG:unicron.py old.sh - Executing, since last run date is old.
2020-04-05 15:29:48,321 INFO:unicron.py old.sh - Success.
2020-04-05 15:29:48,322 INFO:unicron.py today.sh - Skipping, since already ran today.
2020-04-05 15:29:48,323 INFO:unicron.py unicron - Succeeded: 2; Failed: 2; Skipped: 1
```

</details>


## Python CLI

Instead of going through `make`, you can run the Python script directly:

```bash
$ cd ~/repos/unicron/unicron
$ ./unicron.py --help
```
