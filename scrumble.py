#! /bin/env python3

import codecs
import datetime
import json
import logging
import random
import sys
import collections

# logging.basicConfig(level=logging.DEBUG)


def get_gift(people):
    return tuple(people)[random.randint(0, len(people) - 1)]


def scrumble(couples):
    peoples = set()
    for c in couples:
        peoples.update(c)

    # Dict with people
    # X -> Y
    # X do a gift to Y
    gifts = collections.OrderedDict()
    for i, c in enumerate(couples):
        couple = set(c)
        for p in c:
            have_gift = set(gifts.values())
            others = peoples - couple - have_gift
            g = get_gift(others)
            gifts[p] = g
    return gifts


def search_gifts(configuration):
    while True:
        try:
            gifts = scrumble(configuration["couple"])
            for p, g in gifts.items():
                print(f"{p:20} -> {g:>20}")
            return
        except ValueError as e:
            pass


def load_config(conf_file):
    with codecs.open(conf_file, "r", "utf8") as fh:
        configuration = json.load(fh)
    return configuration


def help_message():
    print(f"Usage of {sys.argv[0]}:")
    print("{sys.argv[0]} <config_file_to_read>")
    sys.exit(1)


def get_date_to_compute(configuration):
    # init random to what is given by user
    default_date = datetime.date.today().isoformat()

    return datetime.date.fromisoformat(configuration.get("date", default_date))


def init_random(date_to_compute):
    # this idea does not work
    tdelta = date_to_compute - REF_DATE
    logging.debug("Init seed with: %s", tdelta.total_seconds())
    random.seed(tdelta.total_seconds())


if __name__ == "__main__":
    if len(sys.argv) != 2:
        help_message()
    else:
        configuration = load_config(sys.argv[1])
        search_gifts(configuration)
