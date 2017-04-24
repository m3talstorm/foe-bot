
"""
"""

# Native
import time
import pprint
from collections import OrderedDict

# 3rd-Party
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship, backref

import pydash

#
from request import Request
from models.model import Model
from models.city import City
from models.player import Player
from models.tavern import Tavern


class Account(Model):
    """
    """

    REQUEST_CLASS = "StartupService"

    __tablename__ = 'account'

    # Attributes
    # ---------------------------------------------------------

    player_id = Column(Integer, primary_key=True, default=0)

    id = Column(String, default=0)

    user_name = Column(String, default='', unique=True)

    # Back-refs
    # ---------------------------------------------------------

    # Containers
    # ---------------------------------------------------------

    city = relationship(City, backref=backref('account', uselist=False), uselist=False)

    players = relationship(Player, backref=backref('account', uselist=False))

    taverns = relationship(Tavern, backref=backref('account', uselist=False))

    def __init__(self, *args, **kwargs):
        """
        """

        return super(Account, self).__init__(*args, **kwargs)

    def __repr__(self):
        """
        """

        return "Account %s (%s)" % (self.player_id, self.user_name)

    def fetch(self):
        """
        Does a HTTP request to get the start up blob for the city, then populates the models
        """

        print "%s fetching..." % (self)

        timer = time.time()

        data = self.request('getData', [])

        account = Request.service(data, 'StartupService')
        account['taverns'] = Request.method(data, 'getOtherTavernStates')

        self.update(**account)

        print "%s fetched in %.2fs" % (self, time.time() - timer)

        return self

    def populate(self, *args, **kwargs):
        """1
        """

        user = kwargs.pop('user_data')
        social = kwargs.pop('socialbar_list')
        taverns = kwargs.pop('taverns')
        city = kwargs.pop('city_map')

        for key in ['player_id', 'user_name']:
            setattr(self, key, user[key])

        for key in kwargs.keys():
            kwargs.pop(key)

        # City

        if not self.city:
            self.city = City(account=self)

        self.city.update(**city)

        # Players

        for raw_player in social:

            player = self.session.query(Player).filter_by(player_id=raw_player['player_id']).first()
            if not player:
                player = Player(account=self)

            player.update(**raw_player)

        # Taverns

        for raw_tavern in taverns:

            tavern = self.session.query(Tavern).filter_by(ownerId=raw_tavern['ownerId']).first()
            if not tavern:
                tavern = Tavern(account=self)

            tavern.update(**raw_tavern)

        return super(Account, self).populate(*args, **kwargs)
