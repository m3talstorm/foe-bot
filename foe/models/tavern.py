
"""
"""

# Native
import json

# 3rd-Party
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

#
from request import Request
from models.model import Model

class Tavern(Model):
    """
    """

    REQUEST_CLASS = 'FriendsTavernService'

    __tablename__ = 'tavern'

    # Attributes
    # ---------------------------------------------------------

    ownerId = Column(Integer, primary_key=True, default=0)

    sittingPlayerCount = Column(Integer, default=0)

    unlockedChairCount = Column(Integer, default=0)

    nextVisitTime = Column(Integer, default=0)

    state = Column(String, default='available')

    # Back-refs
    # ---------------------------------------------------------

    account_id = Column(Integer, ForeignKey('account.player_id'))

    # Containers
    # ---------------------------------------------------------

    def __init__(self, **kwargs):
        """
        """

        return super(Tavern, self).__init__(**kwargs)

    def __repr__(self):
        """
        """

        return "Tavern %s (%s)" % (self.ownerId, self.state)

    def populate(self, *args, **kwargs):
        """
        """

        return super(Tavern, self).populate(*args, **kwargs)

    @property
    def sittable(self):
        """
        """

        if self.state in ['noChair', 'isSitting', 'alreadyVisited']:
            return False

        if self.sittingPlayerCount >= self.unlockedChairCount:
            return False

        return True

    def sit(self):
        """
        """

        if not self.sittable:
            return

        response = self.request('getOtherTavern', self.ownerId)

        print "%s sat" % (self)

        return response

    @classmethod
    def collect(cls):
        """
        """

        response = cls.request('getOwnTavern', [])

        print "Collected tavern"

        return response
