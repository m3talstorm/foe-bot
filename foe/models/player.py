
"""
"""

# Native
import time
import json
import pprint

# 3rd-Party
from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship, backref

#
from request import Request
from models.model import Model


class Player(Model):
    """
    """

    REQUEST_CLASS = "OtherPlayerService"

    __tablename__ = 'player'

    # Attributes
    # ---------------------------------------------------------

    id = Column(String, default=0)

    player_id = Column(Integer, primary_key=True, default=0)

    score = Column(Integer, default=0)

    is_online = Column(Boolean, default=False)

    is_friend = Column(Boolean, default=False)

    is_neighbor = Column(Boolean, default=False)

    is_guild_member = Column(Boolean, default=False)

    is_self = Column(Boolean, default=False)

    is_invited = Column(Boolean, default=False)

    profile_text = Column(String, default='')

    city_name = Column(String, default='')

    has_great_building = Column(Boolean, default=False)

    is_active = Column(Boolean, default=False)

    name = Column(String, default='')

    avatar = Column(String, default='')

    # Custom field so we can keep track of when stuff should be collected
    collection_time = Column(Float, default=0)

    # Back-refs
    # ---------------------------------------------------------

    account_id = Column(Integer, ForeignKey('account.player_id'))

    # Containers
    # ---------------------------------------------------------

    #clan =

    def __init__(self, *args, **kwargs):
        """
        """

        return super(Player, self).__init__(*args, **kwargs)

    def __repr__(self):
        """
        """

        return "Player %s (%s)" % (self.player_id, self.name)

    def populate(self, *args, **kwargs):
        """
        """

        for key in ['clan', 'clan_id', 'topAchievements', 'title', 'won_battles', 'rank', 'incoming', 'registered', 'rewarded', 'accepted']:
            kwargs.pop(key, None)

        self.collection_time = time.time() + kwargs.pop('next_interaction_in', 0)

        return super(Player, self).populate(*args, **kwargs)

    @property
    def aidable(self):
        """
        """

        if not self.collection_time:
            return False

        if self.collection_time > time.time():
            return False

        if self.is_self:
            return False

        if self.is_neighbor:
            return True

        if self.is_friend:
            return True

        if self.is_guild_member:
            return True

        return False

    def aid(self):
        """
        """

        if not self.aidable:
            return

        data = self.request('polivateRandomBuilding', self.player_id)

        self.collection_time = 0

        print "%s aided" % (self)

        return data

    def visit(self):
        """
        Visits the players city and prints out buildings we are interested in... good for sabotaging
        """

        data = self.request('visitPlayer', [self.player_id])

        for i, value in enumerate(data):
            if value['requestClass'] == 'OtherPlayerService':
                city = value['responseData']
                break

        buildings = city['city_map']['entities']

        for building in buildings:

            if building['type'] in ['goods', 'production', 'random_production']:
                pprint.pprint(building)

        return data
