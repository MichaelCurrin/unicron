# Unicron :clock1:
> Easy scheduler to run tasks exactly once per day and retry at intervals if a task fails :repeat_one::hourglass_flowing_sand::unicorn:

[![Actions status](https://github.com/MichaelCurrin/uni-cron/workflows/Python%20package/badge.svg)](https://github.com/MichaelCurrin/uni-cron/actions)
[![GitHub tag](https://img.shields.io/github/tag/MichaelCurrin/uni-cron.svg)](https://GitHub.com/MichaelCurrin/uni-cron/tags/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/MichaelCurrin/uni-cron/blob/master/LICENSE)

<p align="center">
    <img width="250" src="_media/logo.png">
</p>


## What is Unicron?

Get the right balance in scheduling automated tasks. It runs often enough that tasks run reliably (will not be missed on a day), but not too often that you increase costs (tasks are skipped if they already succeeded today).

The Unicron name comes from two parts:

- _Uni_ (one) - it run a task just _once_ a day, if all goes well.
- _Cron_ (time) - it is used for scheduled task runs, especially for retries.

And since the name is close to the mythical _unicorn_, that symbol is used in the docs.

Searching for Unicron will show the following on Wikipedia:

- [Unicron](https://en.wikipedia.org/wiki/Unicron) the Transformer.
- [Unicron](https://en.wikipedia.org/wiki/MF_Doom_%26_Trunks_Presents_Unicron) the rap album.

### Audience

- Uni-Cron works on Unix-like environments - **Linux** and **macOS**.
- To use Uni-Cron, you should be familiar with running **Bash** commands in the terminal.
- The tool require **Python** to be installed, but you do not have to know anything about Python to use this tool.
- Uni-cron was built for developers who want to run tasks daily but on **laptops** that are not always awake or connected to the internet.
- It also works great for machines that are **always online**. Output will be logged for successes and failures at the task level so you have that full history, but the crontab mail system will only send messages on failures to avoid noisy messages.


## Requirements

- Python 3
- Crontab


## Docs

- [Features](features.md)
- [Installation](/docs/installation.md)
- [Usage](/docs/usage.md)
- [Development](/docs/development.md)


## License

Released under [MIT License](https://github.com/MichaelCurrin/uni-cron/blob/master/LICENSE).

Feel free to use this application, to use or modify the code and to contribute with a Pull Request. Please give credit with a link back to this repo, where you use some of all of the code.

Logo made using [logomakr](https://logomakr.com/) tool and their stock images.
