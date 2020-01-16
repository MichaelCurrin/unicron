# Uni-Cron :clock1:
> A scheduler to run tasks exactly once per day but retry until a success. :repeat_one::hourglass_flowing_sand::unicorn:

[![Actions status](https://github.com/MichaelCurrin/uni-cron/workflows/Python%20package/badge.svg)](https://github.com/MichaelCurrin/uni-cron/actions)
[![GitHub tag](https://img.shields.io/github/tag/MichaelCurrin/uni-cron.svg)](https://GitHub.com/MichaelCurrin/puni-cron/tags/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/MichaelCurrin/uni-cron/blob/master/LICENSE)

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
- [Installation](#installation)
    - [Clone](#clone)
    - [Configuration](#configuration)
- [Usage](#usage)
    - [See Makefile help](#see-makefile-help)
    - [Run main script](#run-main-script)
    - [View logs](#view-logs)
- [Development](#development)
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
4. Scheduling - add a command to the _crontab_ file.
    ```bash
    $ crontab -e
    ```
    ```
    SHELL=/bin/bash
    PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
    MAILTO=my-user

    # Run every 30 minutes and only send mail on failure.
    */30 *    *    *    *    cd ~/repos/uni-cron/unicron && ./unicron.py
    ```

<!-- TODO: Make executable without cd then update here. Also consider if make should be used here. -->

<!-- TODO: Repeat scheduling this in the usage/config section in more detail with `crontab -e`. -->


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

Why code something new? Well, I did find a possible solution that was recommended online using a combination of `anacron` and `at` together (covered further below). But, the drawback is that those tools only work on _Linux_ and I need to solve the case on _macOS_. So I made _Uni-Cron_.

I read some tutorials and conversations online around scheduling tasks on Unix-like systems with `cron`, `crontab`, `anacron` and `at`. These tools are summarized below.

- `cron` - Run tasks at a varying frequencies, from every minute to once a year. If the machine is off during a schedule time, the job will not run.
- `anacron` - Run tasks up to once per day using `cron` configuration, except this `anacron` expects that the machine may not be on all the time so is able catch up on any missed tasks. The downside though is that if a daily task fails, `anacron` will not retry it.
- `at` - Schedule a task in the future in a queue of tasks, when system resources allow.
- `anacron` with `at` - It has been suggested online to use `anacron` to kick off the jobs when the machine comes online. Then every time there is a failure, use `at` to get the job to schedule another run off itself later in the day. Repeat this until a success.

## Installation

### Clone

```bash
$ git clone git@github.com:MichaelCurrin/uni-cron.git
$ cd uni-cron
```

### Configuration

Add executables or symlinks to executables in the target directory.

Configure crontab to run the main script at an interval through the day such every 30 min (or every 1 hour). This can be more frequent, but there is not much benefit as this is aimed at scripts that only run once per day and the time doesn't matter.

<!-- TODO: How to setup crontab and to disable mails for it. -->

Example of setting up and testing a script.

```bash
$ cd <PATH_TO_REPO>
```

Create a test file and make it executable.

```bash
$ echo -e '#!/bin/bash\necho "Hello world!"\n' > unicron/var/targets/hello.sh
$ chmod +x unicron/var/targets/hello.sh
```

Run it directly to check works fine.

```bash
$ unicron/var/targets/hello.sh
Hello world!
```

## Usage

```bash
$ cd <PATH_TO_REPO>
```

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
    2020-01-13 22:49:12,770 DEBUG:unicron.py hello.sh - Executing, since no run record found.
    2020-01-13 22:49:12,781 INFO:unicron.py hello.sh - Success.
    ```
- Second run.
    ```bash
    $ make run
    unicron/unicron.py -v
    2020-01-13 22:49:30,438 INFO:unicron.py hello.sh - Skipping, since already ran today.
    ```

### View logs

Run this command to tail the app and task logs. Sample output is for the run commands above.

```bash
$ make log
==> output/hello.sh.log <==

2020-01-13 22:49:12,770 INFO:unicron.py - Executing...
2020-01-13 22:49:12,782 INFO:unicron.py - Output:
    Hello world!


==> app.log <==
2020-01-13 22:49:12,770 DEBUG:unicron.py hello.sh - Executing, since no run record found.
2020-01-13 22:49:12,781 INFO:unicron.py hello.sh - Success.
2020-01-13 22:49:30,438 INFO:unicron.py hello.sh - Skipping, since already ran today.
```


## Development

See available commands.

```bash
$ make help
```

Run formatting and linting.

```bash
$ make check
```

See the config file for those settings - [pyproject.toml](pyproject.toml).

Run tests script.

```bash
$ make test-output
```


## License

Released under [MIT License](LICENSE).

Feel free to use this application and to use or modify the code. Please give credit with a link back to this repo.
