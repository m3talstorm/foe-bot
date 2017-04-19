
"""
"""

# Native
import time
import pprint

# 3rd-Party
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref

#
from request import Request
from models.model import Model
#from models.building_state import BuildingState



class Building(Model):
    """
    """

    REQUEST_CLASS = 'CityProductionService'

    __tablename__ = 'building'

    # Attributes
    # ---------------------------------------------------------

    id = Column(Integer, primary_key=True, default=0)

    connected = Column(Integer, default=0)

    x = Column(Integer, default=0)

    y = Column(Integer, default=0)

    type = Column(String, default='')

    cityentity_id = Column(String, default='')

    level = Column(String, default='')
    # Custom field to denormalize state into
    state = Column(String, default='')
    # Custom field so we can keep track of when stuff should be collected
    collection_time = Column(Float, default=0)

    # Back-refs
    # ---------------------------------------------------------

    city_id = Column(String, ForeignKey('city.id'))

    # Containers
    # ---------------------------------------------------------

    def __init__(self, *args, **kwargs):
        """
        """

        return super(Building, self).__init__(*args, **kwargs)

    def __repr__(self):
        """
        """

        return "Building %s (%s)" % (self.id, self.cityentity_id)

    def populate(self, *args, **kwargs):
        """
        """

        for key in ['player_id', 'clan', 'clan_id', 'topAchievements', '__class__']:
            kwargs.pop(key, None)

        state = kwargs.pop('state')

        if state:

            self.state = state['__class__']

            if self.state == 'ProducingState':
                self.collection_time = time.time() + state['next_state_transition_in']

            elif self.state == 'ProductionFinishedState':
                self.collection_time = time.time()

            elif self.state == 'IdleState':
                self.collection_time = 0
            else:
                pprint.pprint(state)


        return super(Building, self).populate(*args, **kwargs)

    def produce(self):
        """
        """

        if self.type == 'residential':
            return

        if self.collection_time:
            return

        if self.state in ['ProducingState', 'ProductionFinishedState']:
            return

        response = self.request('startProduction', [self.id, 1])

        print "%s started production" % (self)

        #
        self.collection_time = time.time() + (5 * 60)
        self.state = 'ProducingState'

        return response

    def pickup(self):
        """
        """

        if not self.collection_time:
            return

        if self.collection_time > time.time():
            return

        response = self.request('pickupProduction', [[self.id]])

        print "%s picked up production" % (self)

        #
        if self.type == 'residential':
            self.collection_time = time.time() + (60 * 60)
            self.state = 'ProducingState'
        else:
            self.collection_time = 0
            self.state = 'IdleState'

        return response

    def cancel(self):
        """
        """

        if self.type == 'residential':
            return

        response = self.request('cancelProduction', [[self.id]])

        print "%s cancelled production" % (self)

        #
        self.collection_time = 0
        self.state = 'IdleState'

        return response
