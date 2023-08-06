import random
import re

DIE_PATTERN = re.compile("(?P<count>\\d*)d(?P<value>\\d+)")


def roll(dice_str):
    search = DIE_PATTERN.search(dice_str)
    count = search.group("count")
    count = int(count) if count else 1
    value = int(search.group("value"))
    return sum(random.randrange(value) + 1 for _ in range(count))
