# wedne: координируем строительство башни

![PyPI](https://img.shields.io/pypi/v/wedne)
![PyPI - License](https://img.shields.io/pypi/l/wedne)

_This project was built for a Russian-speaking community. There's no English version of
the README._

В чатах "Вастрик Клуба" любят строить башни. Башни — это однобуквенные сообщения от
участников, из которых может составиться слово. Самый важный башенный день — среда. В
среду принято строить "ITSWEDNESDAYMYDUDES" и отправлять лягушек. Это непросто: постоянно
кто-то хочет отправить сообщение между буквами. Клубчанин не может быть посередине,
приходится выбирать между созиданием и разрушением.

wedne состоит из двух частей: `wedne.server` и `wedne.client`. Клиенты регистрируются в
общем сервере и получают команды: отправить такую-то букву в такое-то время.

## Инструкции

### Как строить башни?

Не обязательно быть программистом. Прочтите эту секцию и узнайте, как поучаствовать в
строительстве.

1. Скачайте на компьютер [установщик Python][py],
2. Пройдите установку (если спросят, отметьте "Add python.exe to PATH"),
3. Откройте приложение "Терминал" или "Командную строку",
4. Введите туда `python -m pip install wedne` — теперь вы установили wedne,
5. Наконец введите `python -m wedne.client` и залогиньтесь как в телеграме.

Теперь у вас работает клиент. Он подключится к серверу и начнет ждать команду. Когда
придет время, в чат от вашего имени отправится буква.

Можете закрывать инструкцию.

### Я продвинутый, могу ли я запустить через Docker?

```sh
docker run qwskr/wedne:latest
```

### Я продвинутый, могу ли я запустить сервер?

Проще всего склонировать и запустить с помощью Docker Compose:

```sh
docker compose up
```

Без докера надо запустить API и обработчик задач:

```sh
python -m wedne.server run_api

python -m wedne.server consume_tasks
```

## FAQ

### Почему я должен входить в телеграм? Это безопасно?

wedne должен отправить букву в чат от какого-то аккаунта. При входе как раз подключается
такой аккаунт. Исходный код открыт, можно проверить самому, как используются данные
телеграма.

### Без телеграма можно?

Нельзя.

### Какие команды могут прийти с сервера?

Только команда из трех переменных: какую букву отправлять, когда отправлять и после кого
отправлять. Сервер не может скомандовать отправить слово или предложение — клиент такое не
примет. Сервер не может направить клиентов на другой чат — ID чата хранится на клиентах
локально. Схема команды: `wedne/commands.py`

### Не могу запустить, помогите?

Спросите помощи в [чате "Бар"][chat].

### Ничего не понимаю, что за башни и что за клуб?

Кажется, вы не знаете про ["Вастрик Клуб"][club]. Этот проект написан для него. Если вы не
участник, вам wedne будет бесполезен.

[py]: https://www.python.org/downloads/
[chat]: https://vas3k.club/room/bar/chat/
[club]: https://vas3k.club/
