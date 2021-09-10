# Configure crontab
> Set up a single cron job

<!-- TODO move command above to SH script -->

<!-- TODO: Make executable without cd then update here. Also consider if make should be used here. -->

<!-- TODO: Repeat scheduling this in the usage/config section in more detail with `crontab -e`. -->


You only need to add a **single** _Unicron_ item to _crontab_, regardless of how many task you have configured in _Unicron_.

Follow instructions below to configure _crontab_ to run the main _Unicron_ script at an interval throughout the day.


## Frequency

Pick a frequency - such as every 30 minutes (`*/30`) or every hour (`0`). This could be more frequent, but there is not much benefit, as Unicron is aimed at scripts that only run once per day and when the time doesn't matter. So as long as you are online _sometime_ for 30 minutes to an hour during a day and then turn your laptop off, you'll get your tasks to run.

Example:

```
*/30    *       *       *       *
```


## Script name

Use this as the cron command:

- `~/repos/unicron/unicron.py`

You could use just `unicron.py` instead, but then you need to make sure that the bin directory is in the `PATH` value in crontab config.


## Verbosity

Omit the `--verbose` flag so that Unicron will **only** send an email if there is an error. Note that app and task runs _always_ go to the log files, in case mails are quiet from successes but you still want to check history and output.

If there are any errors, they will appear in the [Mail](mail.md) utility.


## Put it all together

```bash
$ crontab -e
```

Sample crontab config:

```
SHELL=/bin/bash
PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
MAILTO=$USER

*/30    *       *       *       *       ~/repos/unicron/unicron/unicron.py
```


## Alternative cron target

Rather than relying on crontab to send the mail, you can be more explicit and use the `mail` command on any errors.

An optional shell script is provided to handle that for you. So then replace the cron target above with [~/repos/unicron/bin/cron_target.sh](https://github.com/MichaelCurrin/unicron/blob/master/bin/cron_target.sh), shown here:

[Cron target](https://raw.githubusercontent.com/MichaelCurrin/unicron/master/bin/cron_target.sh ':include :type=code')

Just make sure to set `MAILTO=''` _before_ that target is run, to disable the standard crontab mailing.

Note this script will run quietly on success, so if you run it in the terminal it may return without out which is fine.


### macOS note

In fact if you are running macOS, this is approach might be **necessary**, as the former approach does not work. After upgrading to _Catalina_, I found that `crontab` would **not** send mail in general for any task (even `echo 'Test'`). Even when the task has actually run and when `mail` command does work when run alone.

There might be a more efficient way, but this captures stdout and stderr as a variable. If there is any content in the variable, send a `mail`. We send the content to the `mail` command and set the subject and target user.
