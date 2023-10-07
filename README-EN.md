# wedne: coordinate the construction of the tower

![PyPI](https://img.shields.io/pypi/v/wedne)
![PyPI - License](https://img.shields.io/pypi/l/wedne)

_Этот проект был сделан для русскоязычного сообщества. README на русском [можно найти
здесь][README-RU]._

In Vas3k Club chats, people like to build towers. Towers are one-letter messages from
participants that can be combined to form a word. The main day for building towers is
Wednesday. On Wednesday it is a tradition to build "ITSWEDNESDAYMYDUDES" and send pictures
of frogs. It's not easy: someone always wants to send a message between the letters. A
club member cannot be in the middle. He or she has to choose between creating and
destroying.

wedne has two parts: `wedne.server` and `wedne.client`. The client connects to the public
server and receives instructions for the sending of a letter at a specific time.

## Instructions

### How to build towers?

You don't have to be a programmer. Read this section and find out how to get involved in
construction.

1. Download [the Python installer][py] to your computer,
2. Go through the installation (if asked, check "Add python.exe to PATH"),
3. Open the "Terminal" or "cmd.exe" application,
4. Type `python -m pip install wedne` to install wedne,
5. Finally type `python -m wedne` and log in as in Telegram.

Your client is currently up and running. It will connect to the server and wait for a
command. When the time is right, a message will be sent to your chat from your account.

You can close the instruction.

### I'm advanced, can I run through Docker?

```sh
docker run qwskr/wedne:latest
```

### I'm advanced, can I run a server?

It's easiest to clone and run using Docker Compose:

```sh
docker compose up
```

Without docker, you need to run the API and task handler:

```sh
python -m wedne.server run_api

python -m wedne.server consume_tasks
```

## FAQ

### Why do I have to log into Telegram? Is it safe?

wedne has to send a letter to chat from some account. When you log in, such an account is
connected. The source code is open, you can check for yourself how the Telegram data is
used.

### Can I do it without the Telegram?

You can't.

### Still anxious, how can I run the code from source?

1. Clone the repository (`git clone https://github.com/igoose1/wedne`),
2. Install poetry (`pip install poetry`),
3. Go to the source and install dependencies (`cd wedne; poetry install`),
4. Run wedne (`python -m wedne`).

### What commands can be sent from the server?

Only a command with three variables: what letter to send, when to send it and after whom
to send it. The server cannot send a command to send a word or a phrase. The client will
not accept such a command. The server can't redirect clients to another chat. Chat ID is
stored locally on clients. Command scheme: `wedne/commands.py`

### Can't get it to run, help?

Ask for a help in [the "Бар" chat][chat].

### I don't understand anything, what are the towers and what is the club?

You don't seem to know about the [Vas3k Club][club]. This project is written for it. If
you are not a member, wedne will be of no use to you.

[README-RU]: https://github.com/igoose1/wedne/blob/main/README.md
[py]: https://www.python.org/downloads/
[chat]: https://vas3k.club/room/bar/chat/
[club]: https://vas3k.club/
