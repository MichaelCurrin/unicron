# Uni-Cron :clock1:
> A scheduler to tasks exactly once per day but will retry until a success.  :repeat_one::hourglass_flowing_sand::unicorn:

[![Made with Bash](https://img.shields.io/badge/Made%20with-Bash-blue.svg)](https://www.gnu.org/software/bash/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/MichaelCurrin/py-project-template/blob/master/LICENSE)

<img src="logo.png" alt="logo" style="width:200px;"/>

- [What is Uni-Cron?](#what-is-uni-cron)
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

## What is Uni-Cron?

Get the right balance in scheduling automated tasks. Run often enough that tasks run reliably even on a laptop, but not too often that you increase costs.

- _Uni_ => one
- _Cron_ => time

Also, it sounds like _unicorn._

## Features

- Schedule daily tasks to each run exactly once per day.
- No problem if the machine is off or asleep in the morning - the task will still run later in the day.
- If a task fails (such as bad internet connection), the task will be retried later in the day until it succeeds.
- Ideal for machines like laptops which not always awake and connected to the internet.

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

```sh
$ git clone git@github.com:MichaelCurrin/uni-cron.git
$ cd uni-cron
```

### Configuration

Add executables or symlinks to executables in the target directory.

Configure crontab to run the main script at an interval through the day such every 30 min (or every 1 hour). This can be more frequent, but there is not much benefit as this is aimed at scripts that only run once per day and the time doesn't matter.

<!-- TODO: How to setup crontab to disable mails -->
