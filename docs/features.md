# Features

## Benefits

- **Efficient scheduling - avoid running tasks too often**
    * Schedule tasks to daily, exactly once.
    * Tasks run as early as possibly in the day, attempting frequency you set (e.g. every 30 minutes).
    * When Unicron runs again, it will skip any tasks which were successes.
- **Reliable scheduling to avoid missing tasks on a day**
    * It's no problem if the machine is off or asleep in the morning - the task will still run later in the day.
    * If a task fails (such as bad internet connection), the task will be retried later in the day until it succeeds.
- **Easy task configuration**
    * Add a _single_ crontab entry and point it at Unicron.
    * Add tasks you want to run to a single directory. Either as executable scripts or as symlinks. _Future feature: configure with YAML config file._
    * Whenever Unicron runs, the tasks queued up will run consecutively. No worrying about load on the memory or network traffic or that tasks might run simultaneously. Without Unicron, you'd have to check that all the crontab times are different and that long-running tasks do not overlap with each other.
- **Logging which is informative but so noisy that is hides errors**
    * A detailed log for each task, using the task's output (successes and failures).
    * A summary log at the main app level. By default, Unicron runs with no output if successful, which means you can run it with crontab without generating mails unless there are failures.

## Basic structure

- The main application script is a Python script - [unicron.py](https://github.com/MichaelCurrin/unicron/blob/master/unicron/unicron.py).
- This works together with a `var` directory. hat contains subdirectories which contain unversioned files:
    * User-defined tasks - *var/targets/*
    * App-managed run events - *var/last_run/*
    * Task log output - *var/log/*
    * Application log - *var/app.log*
- There is also `_test_var` directory for testing the application without affecting the main `var` directory.

## Sample

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


## What is the point of running once but retrying?

- Tasks will be run more than once a day where needed.
    - This avoids the issue where a task is scheduled with `cron.daily` or `crontab` for a time when the machine might be off or asleep.
    - This also avoid the problem where a task actually runs and fails for some reason, but it gets ignored until the next day leaving a gap in your daily data dumps. (Failures could happen for for lack of internet connection or the request cannot complete.)
- Tasks are not run too often as there are costs associated.
    - Once you already have the data from a source on a day, you can stop trying to fetch that data.
    - This reduces noisy mails from many tasks which passed or failed into just failure mails, but with a full log still available.
    - Avoid wasting unnecessary processing and local storage.
    - Avoid limits from hitting a social media API too often.
    - You can schedule a tasks every 5 minutes if you want but still only run each task successfully only once.

## What kind of tasks can you run?

The configured tasks should be executables or symlinks to executables so the programming language does not matter. For example the task could be a compiled binary from Go, or a Bash or Python script.

My usecase for for this tool is for scraping webpages, for fetching Twitter API data and for Twitter interactions (post a message or retweet searched tweets). This can be applied to other tasks such as database dumps.

## Technical details

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

Why code something new? Well, I _did_ find a possible solution that was recommended online using a combination of `anacron` and `at` together and I covered this [here](https://github.com/MichaelCurrin/learn-to-code/blob/master/Shell/Scheduling/README.md). But, the drawback is that those tools only work on _Linux_ and I need to solve the case on _macOS_. So I made _Unicron_.
