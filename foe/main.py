
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

        print "Money: %s" % (account.resources.money)

        print "Supplies: %s" % (account.resources.supplies)

        for tavern in account.taverns:
            tavern.sit()
        #
        for player in account.players:
            player.aid()

        Tavern.collect()

        session.commit()

        refresh = count + random.randrange(config['settings']['update']['min'], config['settings']['update']['max'])

    print "Checking... (%s)" % (count)

    buildingService = BuildingService()
    response = buildingService.multipickup(account.city.buildings)

    account.updateFromResponse(response)

    for building in account.city.buildings:
        sleep = random.uniform(0.5, 2)
        time.sleep(sleep)
        building.produce()

    session.commit()

    sleep = random.randrange(10, 30)

    time.sleep(sleep)

    count += sleep
