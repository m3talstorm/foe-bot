
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

class Resources(Model):
    """
    """

    REQUEST_CLASS = "ResourceService"

    __tablename__ = 'resources'

    # Attributes
    # ---------------------------------------------------------

    money = Column(Integer, default=0)

    supplies = Column(Integer, default=0)

    granite = Column(Integer, default=0)

    carnival_roses = Column(Integer, default=0)

    stars = Column(Integer, default=0)

    cloth = Column(Integer, default=0)

    honey = Column(Integer, default=0)

    lead = Column(Integer, default=0)

    population = Column(Integer, default=0)

    gems = Column(Integer, default=0)

    sandstone = Column(Integer, default=0)

    wine = Column(Integer, default=0)

    guild_expedition_attempt = Column(Integer, default=0)

    medals = Column(Integer, default=0)

    alabaster = Column(Integer, default=0)

    dye = Column(Integer, default=0)

    cypress = Column(Integer, default=0)

    ebony = Column(Integer, default=0)

    limestone = Column(Integer, default=0)

    negotiation_game_turn = Column(Integer, default=0)

    expansions = Column(Integer, default=0)

    summer_tickets = Column(Integer, default=0)

    spring_lanterns = Column(Integer, default=0)

    tavern_silver = Column(Integer, default=0)

    premium = Column(Integer, default=0)

    raw_cypress = Column(Integer, default=0)

    raw_dye = Column(Integer, default=0)

    raw_cloth = Column(Integer, default=0)

    raw_ebony = Column(Integer, default=0)

    raw_granite = Column(Integer, default=0)

    # Back-refs
    # ---------------------------------------------------------

    account_id = Column(Integer, ForeignKey('account.player_id'), primary_key=True)

    def __init__(self, *args, **kwargs):
        """
        """

        return super(Resources, self).__init__(*args, **kwargs)


    def __repr__(self):
        """
        """

        return "Resources"


    def populate(self, *args, **kwargs):
        """
        """

        return super(Resources, self).populate(*args, **kwargs)

