import logging
from locust import HttpLocust, task

from benchgrape.core.statement import PreparedStatementsMixin
from benchgrape.core.wamp import WampTaskSet

logger = logging.getLogger(__name__)


DEFAULT_MIN_WAIT = 10
DEFAULT_MAX_WAIT = 100
# make everything slower
CHILL_FACTOR = 10


class StabilityTaskSet(WampTaskSet, PreparedStatementsMixin):
    """
    stays connected. not more.
    """
    tasks = {}
    min_wait = DEFAULT_MIN_WAIT * CHILL_FACTOR
    max_wait = DEFAULT_MAX_WAIT * CHILL_FACTOR

    @task()
    def idle(self):
        pass


class StabilityActivity(HttpLocust):
    task_set = StabilityTaskSet
