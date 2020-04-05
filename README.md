# Uni-Cron :clock1:
> Easy scheduler to run tasks exactly once per day and retry at intervals if a task fails :repeat_one::hourglass_flowing_sand::unicorn:

[![Actions status](https://github.com/MichaelCurrin/uni-cron/workflows/Python%20package/badge.svg)](https://github.com/MichaelCurrin/uni-cron/actions)
[![GitHub tag](https://img.shields.io/github/tag/MichaelCurrin/uni-cron.svg)](https://GitHub.com/MichaelCurrin/uni-cron/tags/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](#license)

<p align="center">
    <img width="250" src="logo.png">
</p>

- [What is Uni-Cron?](#what-is-uni-cron)
    - [Audience](#audience)
- [Features](#features)
    - [Benefits](#benefits)
    - [Basic structure](#basic-structure)
    - [Sample](#sample)
    - [What is the point of running once but retrying?](#what-is-the-point-of-running-once-but-retrying)
    - [What kind of tasks can you run?](#what-kind-of-tasks-can-you-run)
    - [Technical details](#technical-details)
- [Alternative approaches](#alternative-approaches)
    - [Sleeping](#sleeping)
    - [Existing tools](#existing-tools)
- [Requirements](#requirements)
- [Installation](#installation)
- [System dependencies](#system-dependencies)
    - [Clone](#clone)
    - [Setup tasks](#setup-tasks)
    - [Setup one cron job](#setup-one-cron-job)
        - [Note for macOS](#note-for-macos)
- [Usage](#usage)
    - [See Makefile help](#see-makefile-help)
    - [Run main script](#run-main-script)
    - [View logs](#view-logs)
- [Development](#development)
    - [Setup](#setup)
    - [Checks](#checks)
- [License](#license)


## What is Uni-Cron?

Get the right balance in scheduling automated tasks. It runs often enough that tasks run reliably (will not be missed on a day), but not too often that you increase costs (tasks are skipped if they already succeeded today).

Uni-Cron is:

- _Uni_ (one) - run a task just once a day, if all goes well.
- _Cron_ (time) - schedule task runs, especially for retries.

And since the name is close to _unicorn_, that symbol is used in the docs.

See also:
- [Unicron](https://en.wikipedia.org/wiki/Unicron) the Transformer.
- [Unicron](https://en.wikipedia.org/wiki/MF_Doom_%26_Trunks_Presents_Unicron) the rap album.

### Audience

- Uni-Cron works on Unix-like environments - **Linux** and **macOS**.
- To use Uni-Cron, you should be familiar with running **Bash** commands in the terminal.
- The tool require **Python** to be installed, but you do not have to know anything about Python to use this tool.
- Uni-cron was built for developers who want to run tasks daily but on **laptops** that are not always awake or connected to the internet.
- It also works great for machines that are **always online**. Output will be logged for successes and failures at the task level so you have that full history, but the crontab mail system will only send messages on failures to avoid noisy messages.

## Features

### Benefits

- **Efficient scheduling - avoid running tasks too often**
    * Schedule tasks to daily, exactly once.
    * Tasks run as early as possibly in the day, attempting frequency you set (e.g. every 30 minutes).
    * When Uni-Cron runs again, it will skip any tasks which were successes.
- **Reliable scheduling to avoid missing tasks on a day**
    * It's no problem if the machine is off or asleep in the morning - the task will still run later in the day.
    * If a task fails (such as bad internet connection), the task will be retried later in the day until it succeeds.
- **Easy task configuration**
    * Add a _single_ crontab entry and point it at Uni-Cron.
    * Add tasks you want to run to a single directory. Either as executable scripts or as symlinks. _Future feature: configure with YAML config file._
    * Whenever Uni-Cron runs, the tasks queued up will run consecutively. No worrying about load on the memory or network traffic or that tasks might run simultaneously. Without Uni-Cron, you'd have to check that all the crontab times are different and that long-running tasks do not overlap with each other.
- **Logging which is informative but so noisy that is hides errors**
    * A detailed log for each task, using the task's output (successes and failures).
    * A summary log at the main app level. By default, Uni-Cron runs with no output if successful, which means you can run it with crontab without generating mails unless there are failures.

### Basic structure

- The main application script is a Python script - [unicron.py](/unicron/unicron.py).
- This works together with a directory of variable files - *unicron/var/*
    * User-defined tasks - *var/targets/*
    * App-managed run events - *var/last_run/*
    * Task log output - *var/log/*
    * Application log - *var/app.log*

### Sample

Given a configured script `hello.sh` in the targets directory.

<!-- TODO: Update with new output -->

1. First run today - the script executes.
    ```bash
    $ ./unicron.py --verbose
    2020-01-05 19:23:05 INFO:unicron hello.sh - Success.
    ```
2. Second run today - the script is skipped.
    ```bash
    $ ./unicron.py --verbose
    2020-01-05 19:23:56 INFO:unicron hello.sh - Skipping, since already ran today.
    ```
3. First run tomorrow - the script executes.
    ```bash
    $ ./unicron.py --verbose
    2020-01-06 12:22:00 INFO:unicron hello.sh - Success.
    ```
4. Scheduling - add a single command to your _crontab_ configuration. For example, run every 30 minutes and only send mail if at least one job fails.


### What is the point of running once but retrying?

- Tasks will be run more than once a day where needed.
    - This avoids the issue where a task is scheduled with `cron.daily` or `crontab` for a time when the machine might be off or asleep.
    - This also avoid the problem where a task actually runs and fails for some reason, but it gets ignored until the next day leaving a gap in your daily data dumps. (Failures could happen for for lack of internet connection or the request cannot complete.)
- Tasks are not run too often as there are costs associated.
    - Once you already have the data from a source on a day, you can stop trying to fetch that data.
    - This reduces noisy mails from many tasks which passed or failed into just failure mails, but with a full log still available.
    - Avoid wasting unnecessary processing and local storage.
    - Avoid limits from hitting a social media API too often.
    - You can schedule a tasks every 5 minutes if you want but still only run each task successfully only once.

### What kind of tasks can you run?

The configured tasks should be executables or symlinks to executables so the programming language does not matter. For example the task could be a compiled binary from Go, or a Bash or Python script.

My usecase for for this tool is for scraping webpages, for fetching Twitter API data and for Twitter interactions (post a message or retweet searched tweets). This can be applied to other tasks such as database dumps.

### Technical details

- This project is targeted at developers.
- Main log and task-specific logs of successes and errors, for easy viewing of history and problems
- Built on Bash.
- Run all tasks using a single _crontab_ entry.
- Mails will only be sent when a task failures (Avoid noisy crontab mails caused by tasks succeeding or failing)
- Runs on Linux and macOS.

## Alternative approaches

### Sleeping

Note that making a process sleep is inefficient for memory and also does not help if your machine restarts during the day and loses the process. Therefore use an **existing** background process (`crond`) that runs every minute to kick off any configured jobs.

### Existing tools

Why code something new? Well, I _did_ find a possible solution that was recommended online using a combination of `anacron` and `at` together and I covered this [here](https://github.com/MichaelCurrin/learn-to-code/blob/master/Shell/Scheduling/README.md). But, the drawback is that those tools only work on _Linux_ and I need to solve the case on _macOS_. So I made _Uni-Cron_.


## Requirements

- Python 3
- Crontab


## Installation

## System dependencies

- Install [Python 3](https://python.org/)
- Install _crontab_
    - This is available for macOS and Linux and so might be installed already.


### Clone

```bash
$ git clone git@github.com:MichaelCurrin/uni-cron.git
$ cd uni-cron
```

There are no project dependencies to run the main application.

Optionally see the [Development](#development) section if you want to install and use the dev dependencies.

### Setup tasks

_Unicron_ will run tasks for you if you set it up - you can add executables or symlinks to executables in the targets directory.

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

Repeat setup for all tasks that you want automated through _Unicron_.


### Setup one cron job

Follow instructions below to configure crontab to run the main _Unicron_ script at an interval throughout the day.

```bash
$ crontab -e
```

You only need to add a **single** _Unicron_ item to _crontab_, regardless of how many task you have configured in _Unicron_.


Here we add a task to run daily.
```
SHELL=/bin/bash
PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
MAILTO=$USER

*/30 *    *    *    *    cd ~/repos/uni-cron/unicron && ./unicron.py
```

Pick a frequency for the the first item - such as every 30 minutes (`*/30`) or every hour (`0`). This could be more frequent, but there is not much benefit, as Unicron is aimed at scripts that only run once per day and when the time doesn't matter. So as long as you are online _sometime_ for 30 minutes to an hour during a day and then turn your laptop off, you'll get your tasks to run.

Omit the `--verbose` flag so it will **only** send an email if there is an error. Note that app and task runs _always_ go to the log files, in case mails are quiet from successes but you still want to check history and output.

#### Note for macOS

After updating macOS to Catalina, I found that `crontab` would **not** send mail, for _Unicron_ or anything else. Even when the task has actually run and when `mail` command works alone.

But I found that does work as an alternative to the setup above. Though it is longer:

```
*/30    *       *       *       *       RESULT="$(cd ~/repos/uni-cron/unicron && ./unicron.py 2>&1)"; [[ $? -ne 0 ]] || echo "$RESULT" | mail -s 'Unicron task!' $USER
```

<!-- TODO move command above to SH script -->

<!-- TODO: Make executable without cd then update here. Also consider if make should be used here. -->

<!-- TODO: Repeat scheduling this in the usage/config section in more detail with `crontab -e`. -->



## Usage

Run these commands from the repo root.

### See Makefile help

```bash
$ make help
```

### Run main script

Run by hand.

This step uses the verbose mode. This is so that INFO and DEBUG messages that would normally be hidden from printing are still shown on the console.

The example output below is for the script which was setup using [Installation](#installation) instructions.

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


## Development


### Setup

Create a virtual environment at the project root and activate it.

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

Install dev dependencies.

```bash
$ make dev-install
```

### Checks

Format Python files and run linting checks.

```bash
$ make check
```

Run tests script.

```bash
$ make test-output
```


## License

Released under [MIT License](/LICENSE).

Feel free to use this application and to use or modify the code. Please give credit with a link back to this repo.

Logo made using [logomakr](https://logomakr.com/) tool and their stock images.
