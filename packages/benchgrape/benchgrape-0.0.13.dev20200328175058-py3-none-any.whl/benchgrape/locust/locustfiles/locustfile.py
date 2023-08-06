import logging
import random
import string

from locust import HttpLocust
from locust import task, seq_task

from benchgrape.core.statement import PreparedStatementsMixin
from benchgrape.core.wamp import WampTaskSet, PubSubMixin

logger = logging.getLogger(__name__)


DEFAULT_MIN_WAIT = 10
DEFAULT_MAX_WAIT = 100
# make everything slower
CHILL_FACTOR = 10


def get_random_section():
    return random.choice(string.ascii_letters + '#')


def get_random_message():
    word = ["mind", "woebegone", "answer", "grip", "remain", "annoying", "green", "fowl", "macho", "alert", "regular", "steam", "fast", "lumber", "neighborly", "scintillating", "shade", "ragged", "majestic", "unit", "pig", "flat", "accidental", "library", "disturbed", "cellar", "confess", "actor", "successful", "godly", "sick", "skin", "blood", "round", "vase", "appreciate", "gun", "whole", "competition", "obey", "misty", "gabby", "cynical", "blush", "stem", "striped", "groan", "knee", "dead", "faithful", "ugliest", "fill", "damaging", "jail", "cross", "precede", "cute", "experience", "careful", "adhesive", "type", "boring", "towering", "meeting", "cable", "anxious", "approval", "grease", "plausible", "pretty", "tease", "copper", "material", "fat", "move", "pump", "whirl", "cow", "sweater", "grade", "cherries", "nail", "spy", "belong", "nine", "weight", "opposite", "follow", "water", "jumpy", "nutty", "crow", "exciting", "rustic", "school", "chalk", "few", "mate", "country", "team"]
    return " ".join(random.sample(word, random.randint(1, 25))) + "."


class HistoryTaskSet(PubSubMixin, WampTaskSet, PreparedStatementsMixin):
    """
    simulate chat behaviour with posting, updating, typing, channel switching.
    """
    min_wait = DEFAULT_MIN_WAIT * CHILL_FACTOR
    max_wait = DEFAULT_MAX_WAIT * CHILL_FACTOR

    # wait_time = between(min_wait, max_wait)

    def on_start(self, *args, **kwargs):
        super().on_start(*args, **kwargs)
        self.utils__connect_stack()

    # @seq_task(1)
    # def setuptask(self):
    #     self.utils__connect_stack()

    @seq_task(2)
    @task(5)
    def get_overview(self):
        self.channels__get_overview()

    @seq_task(2)
    @task(15)
    def post_message(self):
        self.channels__post(self.get_random_channel(), get_random_message())

    @seq_task(2)
    @task(15)
    def get_channel(self):
        # todo actual user channels
        self.channels__get(self.get_random_channel())

    @seq_task(2)
    @task(20)
    def get_history_for_channel(self):
        self.channels__get_history(self.get_random_channel())

    @seq_task(2)
    @task(10)
    def search_channels(self):
        self.search__search_channels(self.get_random_channel())

    @seq_task(2)
    @task(15)
    def read_message(self):
        self.channels__read(self.get_random_channel(), msg_id='"fake"')

    @seq_task(2)
    @task(15)
    def typing(self):
        self.channels__set_typing(
            self.get_random_channel(), random.randint(0, 1)
        )

    @seq_task(3)
    def disconnect(self):
        self.utils__disconnect_stack()


# this is whats used, currently its just a reference
class StandardActivity(HttpLocust):
    task_set = HistoryTaskSet


#
# class ReconnectTaskSet(PubSubMixin, WampTaskSet, PreparedStatementsMixin):
#     """
#     simulate a connection outage and reconnecting clients.
#     """
#     min_wait = 5 * 1000
#     max_wait = 10 * 1000
#
#     @seq_task(1)
#     def disconnect(self):
#         self.utils__disconnect_stack()
#
#     @seq_task(2)
#     def connect(self):
#         self.utils__connect_stack()
#
#
# class StandardActivityTaskSet(WampTaskSet, PreparedStatementsMixin):
#     """
#     container of subsets and their weights to simulate a normal activity in
#     an organization. use this to benchmark server requirements for customers.
#     """
#     tasks = {
#         #PhoneBookTaskSet: 5,
#         ReconnectTaskSet: 10,
#         #HistoryTaskSet: 80,
#     }
#
#     def on_start(self):
#         super(StandardActivityTaskSet, self).on_start()
#         # generate the load the client would do as well
#         self.utils__connect_stack()
#
#
# class IdleActivityTaskSet(WampTaskSet, PreparedStatementsMixin):
#     """
#     just establish the websocket, nothing more. see how many websockets we
#     can handle in idle. - ping is still sent.
#     """
#     tasks = {}
#
#     @task()
#     def idle(self):
#         pass
#
#
# class PhoneBookTaskSet(WampTaskSet, PreparedStatementsMixin):
#     # user behaviour, how much time between the actions, we need kibana to
#     # monitor and fine tune this numbers to be realistic.
#     # i'd like to add kibana to our staging and measure how activity looks like
#     # in terms of API calls (which, how much time in between, how many at most
#     # for how many online users, etc...)
#     min_wait = 10
#     max_wait = 3600 * 1000
#
#     # users
#     @task()
#     def get_users_no_query_membership_true(self):
#         self.users__get_users(True)
#
#     @task()
#     def get_users_no_query_membership_false(self):
#         self.users__get_users(False)
#
#     @task()
#     def get_users_no_query_membership_none(self):
#         self.users__get_users(None)
#
#     @task()
#     def get_users_query_membership_true(self):
#         self.users__get_users(True, 'ad')
#
#     @task()
#     def get_users_query_membership_false(self):
#         self.users__get_users(False, 'ad')
#
#     @task()
#     def get_users_query_membership_none(self):
#         self.users__get_users(None, 'ad')
#
#     @task()
#     def get_users_sections(self):
#         self.users__get_users(None, {'section': get_random_section()})
#
#     @task()
#     def get_rooms_no_query_membership_true(self):
#         self.rooms__get_rooms(True)
#
#     @task()
#     def get_rooms_no_query_membership_false(self):
#         self.rooms__get_rooms(False)
#
#     @task()
#     def get_rooms_no_query_membership_none(self):
#         self.rooms__get_rooms()
#
#     @task()
#     def get_rooms_query_membership_true(self):
#         self.rooms__get_rooms(True, 'ad')
#
#     @task()
#     def get_rooms_query_membership_false(self):
#         self.rooms__get_rooms(False, 'ad')
#
#     @task()
#     def get_rooms_query_membership_none(self):
#         self.rooms__get_rooms(None, 'ad')
#
# class PhoneBookActivity(HttpLocust):
#     task_set = PhoneBookTaskSet
#
# class ChatActivity(HttpLocust):
#     task_set = HistoryTaskSet


