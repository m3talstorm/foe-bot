
"""
"""

# Native
import time

# 3rd-Party

#
from request import Request
from models.model import Model


class TreasureChest(object):
    """
    """

    REQUEST_CLASS = "TreasureHuntService"

    id = 0

    #flags = None

    #state = TreasureChestCollectable

    #journey_restart_time = 0

    #travel_time = 0

    def __init__(self, **kwargs):
        """
        """

        for key, value in kwargs.iteritems():

            if key == '__class__':
                key = 'klass'

            if key == 'state':
                if value['__class__'] == 'ProducingState':
                    value['pickup_time'] = time.time() + value['next_state_transition_in']

                if value['__class__'] == 'ProductionFinishedState':
                    pass

            setattr(self, key, value)

        return

    def __repr__(self):
        """
        """

        return "Building %s (%s)" % (self.id, self.cityentity_id)

    def collect(self):
        """
        """

        if self.state['__class__'] = 'TreasureChestClosed':
            return

        response = self.request('collectTreasure', None)

        print "%s collected" % (self)

        return response


# self.state['__class__'] = TreasureChestClosed, TreasureChestTraveling, TreasureChestCollectable

# getOverview
