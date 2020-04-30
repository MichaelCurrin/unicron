# Unicron homepage
> Easy scheduler to run tasks exactly once per day and retry at intervals if a task fails

[![Actions status](https://github.com/MichaelCurrin/unicron/workflows/Python%20package/badge.svg)](https://github.com/MichaelCurrin/unicron/actions)
[![Made with Docsify](https://img.shields.io/badge/Made%20with-Docsify-blue.svg)](https://docsify.js.org/)
[![GitHub tag](https://img.shields.io/github/tag/MichaelCurrin/unicron.svg)](https://GitHub.com/MichaelCurrin/unicron/tags/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/MichaelCurrin/unicron/blob/master/LICENSE)


## What is Unicron?

Get the right balance in scheduling automated tasks. It runs often enough that tasks run reliably (will not be missed on a day), but not too often that you increase costs (tasks are skipped if they already succeeded today).

The "Unicron" name is made up based on two ideas:

- **Uni** meaning one - as it run's a task just _once_ a day only (if all goes well).
- **Cron** meaning time - as it works best on a schedule

Since the name is close to the mythical _unicorn_, that symbol is used for the logo.

For interest, here are things on Wikipedia also called Unicron:

- [Unicron](https://en.wikipedia.org/wiki/Unicron) the Transformer.
- [Unicron](https://en.wikipedia.org/wiki/MF_Doom_%26_Trunks_Presents_Unicron) the rap album.

### Audience

- Unicron works on Unix-like environments - **Linux** and **macOS**.
- To use Unicron, you should be familiar with running **Bash** commands in the terminal.
- The tool require **Python** to be installed, but you do not have to know anything about Python to use this tool.
- Unicron was built for developers who want to run tasks daily but on **laptops** that are not always awake or connected to the internet.
- It also works great for machines that are **always online**. Output will be logged for successes and failures at the task level so you have that full history, but the crontab mail system will only send messages on failures to avoid noisy messages.


## Requirements

- Linux or macOS
- Python 3
- Crontab
