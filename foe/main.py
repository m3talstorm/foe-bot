
"""
"""

#
import time
import random

#

#
from models.account import Account
from models.tavern import Tavern
from models.buildingService import BuildingService

import deploy

from db import session

from config import config


account = Account()

session.add(account)

count = 0

refresh = random.randrange(config['settings']['update']['min'], config['settings']['update']['max'])

while True:

    if not count or count >= refresh:
        account.fetch()
        session.commit()

        #break

        print "Players: %s" % (len(account.players))

        print "Buildings: %s" % (len(account.city.buildings))

        print "Taverns: %s" % (len(account.taverns))

        print "Money: %s" % "{:,}".format(account.resources.money)

        print "Supplies: %s" % "{:,}".format(account.resources.supplies)

        for tavern in account.taverns:
            tavern.sit()
        #
        for player in account.players:
            player.aid()

        Tavern.collect()

        session.commit()

        refresh = count + random.randrange(config['settings']['update']['min'], config['settings']['update']['max'])

    print "Checking... (%s)" % (count)
    # NOTE: The full update should adjust for any coins/supplies/resources gained from these pickups
    account.city.pickup()

    account.city.produce()

    session.commit()

    sleep = random.randrange(10, 30)

    time.sleep(sleep)

    count += sleep
