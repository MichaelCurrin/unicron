# Mail
> How to check for Unicron errors through mail utility.

Install the `mail` utility to use the command-line to manage mail sent by crontab.

If there are errors, the `mail` utility will you in the terminal, without having to run anything.

You can view mails by starting `mail` and using the interactive prompty.

```sh
$ mail
```

Example:

```sh
$ mail
"/var/mail/my-user": 60 messages 60 unread
>U  1 my-user@host  Sat Mar 28 16:15  15/666   "Unicron task failed!"
```

Press enter to view mails one by one, or a number (e.g. `1`) and enter to view that mail. Press <kbd>q</kbd> and enter to exit.
