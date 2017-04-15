
"""
"""

#
import time
import random

#

#
from models.account import Account
from models.tavern import Tavern

import deploy

from db import session


account = Account()

session.add(account)

count = 0

refresh = random.randrange(5 * 60, 30 * 60)

while True:

    if not count or count >= refresh:
        account.fetch()

        print "Players: %s" % (len(account.players))

        print "Buildings: %s" % (len(account.city.buildings))

        print "Taverns: %s" % (len(account.taverns))

        for tavern in account.taverns:
            tavern.sit()
        #
        for player in account.players:
            player.aid()

        Tavern.collect()

        session.commit()

        refresh = count + random.randrange(5 * 60, 30 * 60)

    print "Checking... (%s)" % (count)

    for building in account.city.buildings:
        building.pickup()

    for building in account.city.buildings:
        building.produce()

    session.commit()

    sleep = random.randrange(10, 30)

    time.sleep(sleep)

    count += sleep
