import datetime

# This is official tdesktop snap's API key. It's obfuscated because I'm not
# sure Telegram would be happy to see it here
API_ID = 123456 + 487879
API_HASH = "f".join(["c9ca14", "d1c48680", "73d4", "12d414b425d"])[::-1]

WATCHING_DELAY = datetime.timedelta(seconds=2)
WRITE_FIRST_DELAY = datetime.timedelta(seconds=3.77)

DESTROYING_TEXT = "ПУК"
