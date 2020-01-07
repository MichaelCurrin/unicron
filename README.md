# Uni-Cron :clock1:
> A scheduler to tasks exactly once per day but will retry until a success. :repeat_one::hourglass_flowing_sand::unicorn:

[![Made with Bash](https://img.shields.io/badge/Made%20with-Bash-blue.svg)](https://www.gnu.org/software/bash/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/MichaelCurrin/py-project-template/blob/master/LICENSE)

_:warning: **NOTICE**: This project is very new and still in pre-release stage. It does work as a prototype to the extent shown in the [Usage](#usage) section, along with the logging output. The first major tag and release (v1.0.0) will indicate it is moved to Python3 with unit tests plus better docs around quiet mails on crontab. In the meantime, you are welcome to use this as is (I am using it already). But know that the project main script will change - the idea is that ./unicorn.py will work the same but better._

![logo](logo.png)

- [What is Uni-Cron?](#what-is-uni-cron)
- [Sample](#sample)
- [Features](#features)
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
- [Development](#development)
- [License](#license)


## What is Uni-Cron?

Get the right balance in scheduling automated tasks. Run often enough that tasks run reliably even on a laptop, but not too often that you increase costs.

- _Uni_ => one
- _Cron_ => time

Also, it sounds like _unicorn._


## Features

- **Efficient scheduling**
    * Schedule daily tasks to each run exactly once per day. When set on a recurring cron job, any jobs already run today will be skipped.
- **Reliable scheduling**
    * It's no problem if the machine is off or asleep in the morning - the task will still run later in the day.
    * If a task fails (such as bad internet connection), the task will be retried later in the day until it succeeds.
    * Ideal for machines like laptops which not always awake and connected to the internet.
- **Easy configuration**
    * Add script or a symlink in the targets directory.
    * _Future feature: configure with YAML config file._
- **Logging**
    * Reduce noise - successes are logged but don't create crontab mails.
    * Successes and failures.
    * A brief log for main app level and a detailed log for each task using the task's output (successes and failures).


### Sample

Given a configured script `hello.sh` in the targets directory.

1. First run today - the script executes.
    ```bash
    $ ./unicron.sh
    2020-01-05 19:23:05 INFO:unicron.sh hello.sh - Success.
    ```
2. Second run today - the script is skipped.
    ```bash
    $ ./unicron.sh
    2020-01-05 19:23:56 INFO:unicron.sh hello.sh - Skipping, since already ran today.
    ```
3. First run tomorrow - the script executes.
    ```bash
    $ ./unicron.sh
    2020-01-06 12:22:00 INFO:unicron.sh hello.sh - Success.
    ```
4. Scheduling - add the command to the _crontab_ file.
    ```
    # Run every 30 minutes.
    */30 *    *    *    *    cd ~/repos/uni-cron/unicron && ./unicron.sh
    
    # Or, run hourly.
    0    *    *    *    *    cd ~/repos/uni-cron/unicron && ./unicron.sh
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

## Existing tools

I did find a possible solution that was recommended online using a combination of `anacron` and `at` together. But the drawback is that those tools only work on _Linux_ and I need to solve the case on _macOS_. So I made this tool.

There are a lot of tutorials and conversations online around scheduling tasks on Unix-like systems with `cron`, `crontab`, `anacron` and `at`. These are summarized below.

- `cron` - Run tasks at a varying frequencies, from every minute to once a year. If the machine is off during a schedule time, the job will not run.
- `anacron` - Run tasks up to once per day using `cron` configuration, except this tool expects that the machine may not be on all the time so is able catch up on any missed tasks.
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
$ echo echo -e '#!/bin/bash\necho "Hello world!"\n' > unicron/var/targets/hello.sh
$ chmod +x hello.sh
```

Run it manually.

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

```bash
$ make run
cd unicron && ./unicron.sh
2020-01-05 19:23:05 INFO:unicron.sh hello.sh - Success.
```

```bash
$ make run
cd unicron && ./unicron.sh
2020-01-05 19:23:56 INFO:unicron.sh hello.sh - Skipping, since already ran today.
```

<!--
## Development

```bash
$ make test
```
-->

## License

Released under [MIT License](LICENSE).

Feel free to use this application and to use or modify the code. Please give credit with a link back to this repo.
