# Check mail
> How to check for Unicron errors through the mail utility.

- [mail manpage](https://linux.die.net/man/1/mail) for Linux

This guide uses `mail` command for Linux and macOS. Alternatively you can use `mutt` or something similar or even a visual mail program, but those only `mail` is covered here.

## Unicron and mails

The `mail` utility will tell in the terminal at intervals, that there is mail to be read, if there are any mails. Mails to _myuser@localhost_ will be triggered by a cronjob item that produces any output, on success or failure.

The local mailbox is useful for debugging tasks that Unicron runs. Based on the setup in [Installation](installation.md), when Unicron runs tasks and any single task fails, Unicron will go from quiet (printing nothing) to printing an alert that a task fail.

This will be sent to the mailbox by _crontab_. The message will say what task failed and it will tell you to look at the task's log. This log output will help you here.

```bash
$ make log-tasks
```

Alternatively, you can view just the log for that task.

```bash
$ view unicron/var/output/my_task.log
```

While testing, you may wish to setup your cronjob to send a mail on _every_ run and then switch it to quiet mode later (to send mail on errors only).


## Install mail

Install the `mail` utility to use the command-line to manage mail sent by crontab.


## View mails

You can view mails by starting `mail` and using the interactive prompt.

```bash
$ mail
```

Example:

```bash
$ mail
"/var/mail/my-user": 60 messages 60 unread
>U  1 my-user@host  Sat Mar 28 16:15  15/666   "Unicron task failed!"
```

Press enter to view mails one by one, or a number (e.g. `1`) and enter to view that mail. Press <kbd>q</kbd> and enter to exit.
