#! /usr/bin/python
# -*- coding: utf-8 -*-

import json
import random


def get_gift(people):
  return tuple(people)[random.randint(0, len(people)-1)]

def scrumble(couples):
  peoples = set()
  for c in couples:
    peoples.update(c)

  gifts = {}
  for i, c in enumerate(couples):
    couple = set(c)
    for p in c:
      have_gift = set(gifts.values())
      others = peoples - couple - have_gift
      g = get_gift(others)
      gifts[p] = g
  return gifts


if __name__ == "__main__":
  with open('conf.json', 'r') as fh:
    data = json.load(fh)

  cont = True
  while cont:
    try:
      gifts = scrumble(data["couple"])
      cont = False
      for p, g in gifts.iteritems():
        print p, " fait un cadeau à:", g
    except ValueError, e:
      cont = True
