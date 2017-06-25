
"""
"""

# Native
import random
import time
import uuid
import curses
from curses import wrapper

# # 3rd-Party
import pydash
import moment

# # Proprietary
from models.building import Building
from models.player import Player
from models.resources import Resources

from db import session


from monitor import Monitor



class BuildingMonitor(Monitor):
    """
    """

    def render(self):
        """
        """

        # Get all the ative attacks
        buildings = session.query(Building).order_by(Building.collection_time).all()
        friends = session.query(Player).filter(Player.is_friend == 1).all()
        neighbours = session.query(Player).filter(Player.is_neighbor == 1).all()
        guild = session.query(Player).filter(Player.is_guild_member == 1).all()

        resources = session.query(Resources).all()

        now = moment.unix(time.time(), utc=True).format('HH:mm:ss')

        self.screen.addstr(self.line, 0, "Time: %s | Running: %ss | Update in: %ss" % (now, int(self.running), 100))
        self.screen.addstr(self.line, 0, self.SEPERATOR)
        self.screen.addstr(self.line, 0, "Coins: %s | Supplies: %s" % (resources.money, resources.supplies))
        self.screen.addstr(self.line, 0, "Friends: %s | Neighbours: %s | Guild: %s" % (len(friends), len(neighbours), len(guild)))
        self.screen.addstr(self.line, 0, "Buildings: %s" % (len(buildings)))
        self.screen.addstr(self.line, 0, self.SEPERATOR)

        #
        MAPPER = {
            'residential': curses.color_pair(1),
            'production': curses.color_pair(2),
            'goods': curses.color_pair(3),
        }
        #
        self.screen.addstr(self.line, 0, "ID  | Building                       | Type         | State                   | Collection Time | Remaining |")
        self.screen.addstr(self.line, 0, self.SEPERATOR)
        #
        for building in buildings[:35]:

            colour = MAPPER.get(building.type, '')

            remaining = "%0.0f" % round(building.collection_time - time.time())

            collection = moment.unix(building.collection_time, utc=True).format('HH:mm:ss')

            self.screen.addstr(self.line, 0, "%s | %s | %s | %s | %s | %s" % (self.fixed(building.id, 3),
                                                                            self.fixed(building.cityentity_id, 30),
                                                                            self.fixed(building.type, 12),
                                                                            self.fixed(building.state, 23),
                                                                            self.fixed(collection, 15),
                                                                            self.fixed(remaining, 3)),
                                                                            colour)


        return
