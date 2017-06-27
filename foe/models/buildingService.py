
"""
"""

# Native
import time
import random
import pprint
from collections import OrderedDict

from request import Request

from account import Account

class BuildingService(object):
    """
    """

    REQUEST_CLASS = 'CityProductionService'

    def __init__(self, *args, **kwargs):
        """
        """

        return super(BuildingService, self).__init__(*args, **kwargs)

    def __repr__(self):
        """
        """

        return "Building service"

    def multipickup(self, buildings):
        """
        """

        updateIds = []
        soloUpdate = []

        for building in buildings:
            if not building.pickupable():
                continue

            if random.randrange(1, 100) > 70:
                soloUpdate.append(building)
            else:
                updateIds.append(building.id)

        if len(updateIds) == 0:
            return []

        response = self.request('pickupProduction', [updateIds])

        for building in buildings:
            if building.id not in updateIds:
                continue

            print "%s multipicked up production" % (building)

            building.pickupUpdateState()

        for building in soloUpdate:
            sleep = random.uniform(0.5, 1)
            time.sleep(sleep)
            response = building.pickup()

        lastResponse = response

        return lastResponse

    def request(cls, method, data, klass=None):
        """
        """

        #body = "[{\"requestClass\":\"CityProductionService\",\"requestId\":9,\"requestData\":[[27]],\"__class__\":\"ServerRequest\",\"requestMethod\":\"pickupProduction\"}]"

        payload = [OrderedDict([
            ("requestClass", klass or cls.REQUEST_CLASS),
            ("requestId", Request.REQUEST_ID),
            ("requestData", data),
            ("__class__", "ServerRequest"),
            ("requestMethod", method)]
        )]

        response = Request.request(payload)

        return response