
"""
"""

# Native
import time
import pprint
import json
import random
from collections import OrderedDict

# 3rd-Party
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship, backref

import pydash

# Proprietary
from request import Request
from models.model import Model
from models.building import Building
from models.tavern import Tavern
from models.player import Player


class City(Model):
    """
    """

    REQUEST_CLASS = "StartupService"

    __tablename__ = 'city'

    # Attributes
    # ---------------------------------------------------------

    id = Column(String, primary_key=True, default='0')

    title = Column(String, default='')

    # Back-refs
    # ---------------------------------------------------------

    account_id = Column(Integer, ForeignKey('account.player_id'))

    # Containers
    # ---------------------------------------------------------

    buildings = relationship(Building, backref=backref('city', uselist=False))

    def __init__(self, *args, **kwargs):
        """
        """

        return super(City, self).__init__(*args, **kwargs)

    def __repr__(self):
        """
        """

        return "City"

    def populate(self, *args, **kwargs):
        """
        """

        for key in ['city_entities', 'blocked_areas', 'tilesets', '__class__', 'unlocked_areas']:
            kwargs.pop(key, None)

        buildings = kwargs.pop('entities')

        # Buildings

        for raw_building in buildings:

            if raw_building['type'] in ['production', 'residential', 'goods']:

                building = self.session.query(Building).get(raw_building['id'])
                if not building:
                    building = Building(city=self)

                building.update(**raw_building)


        return super(City, self).populate(*args, **kwargs)

    def pickup(self):
        """
        Picks up (gather resources) all the builds in the city
        """

        # Get the IDs of all the buildings that can be picked up
        ids = [building.id for building in self.buildings if building.pickupable()]
        # No point in going any futher if there is nothing to pickup
        if not ids:
            print "No buildings need picking up"
            return self

        # Pick a random sample (~70%) of the of these buildings
        count = int(len(ids) * 0.7)
        # Sample the builds at random
        sample = random.sample(ids, count)
        # Pickup all of them at once
        response = self.request('pickupProduction', [sample], klass='CityProductionService')

        print "Picked up %s/%s buildings at once" % (len(sample), len(ids))
        # Get the buildings that weren't all picked up at once
        difference = set(ids).difference(set(sample))
        # Now pick up the rest one-by-one
        for building in self.buildings:

            if building.id in difference:
                # Add a built of time so it looks like a human ;)
                sleep = random.uniform(0.5, 1)
                time.sleep(sleep)

                building.pickup()
            elif building.id in sample:
                # This building was picked up as part of the multi/batch pickup so just update the state
                building.pickedup()

        return self

    def produce(self):
        """
        Starts production of all building in the city
        """

        for building in self.buildings:
            # Add a built of time so it looks like a human ;)
            sleep = random.uniform(0.5, 2)
            time.sleep(sleep)

            building.produce()

        return self
