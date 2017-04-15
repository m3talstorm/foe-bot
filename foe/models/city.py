
"""
"""

# Native
import time
import pprint
import json
from collections import OrderedDict

# 3rd-Party
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship, backref

import pydash

#
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
