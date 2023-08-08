import datetime

import pytest

from wedne.commands import CommandSchema


def test_fail_command_validation_on_word():
    with pytest.raises(ValueError):
        _ = CommandSchema(letter="long word", after=None, when=datetime.datetime.min)
