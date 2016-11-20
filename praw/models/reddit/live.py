"""Provide the LiveThread class."""
from ...const import API_PATH
from ..listing.generator import ListingGenerator
from .base import RedditBase
from .redditor import Redditor


class LiveUpdate(RedditBase):
    """An individual LiveUpdate object."""

    STR_FIELD = 'name'

    def __setattr__(self, attribute, value):
        """Objectify author."""
        if attribute == 'author':
            value = Redditor(self._reddit, name=value)
        super(LiveUpdate, self).__setattr__(attribute, value)

    def __init__(self, reddit, _data):
        """Initialize a LiveUpdate instance.

        Note that an instance of this class doesn't retrieve missing
        attributes via ``RedditBase._fetch()``, so you should instantiate
        this class with full ``_data``.

        :param reddit: An instance of :class:`~.Reddit`.

        """
        super(LiveUpdate, self).__init__(reddit, _data)
        self._fetched = True


class LiveThread(RedditBase):
    """An individual LiveThread object."""

    STR_FIELD = 'id'

    def _info_path(self):
        # pylint: disable=redefined-builtin
        return API_PATH['liveabout'].format(id=self.id)

    def __init__(self, reddit, thread_id=None, _data=None):
        """Initialize a lazy :class:``LiveThread`` instance.

        :param reddit: An instance of :class:`~.Reddit`.
        :param id: A live thread ID, e.g., ``ukaeu1ik4sw5``
        """
        if bool(thread_id) == bool(_data):
            raise TypeError('Either `id` or `_data` must be provided.')
        super(LiveThread, self).__init__(reddit, _data)
        if thread_id is not None:
            self.id = thread_id  # pylint: disable=invalid-name

    def accept_contributor_invite(self):
        path = API_PATH['live_accept_contributor_invite'].format(id=self.id)
        return self._reddit.post(path)

    def close(self):
        path = API_PATH['live_close_thread'].format(id=self.id)
        return self._reddit.post(path)

    def contributors(self):
        path = API_PATH['live_contributors'].format(id=self.id)
        return self._reddit.get(path)

    def delete_update(self, update):
        path = API_PATH['live_delete_update'].format(id=self.id)
        data = {'id': str(update)}
        return self._reddit.post(path, data=data)

    def discussions(self, **generator_kwargs):
        """Return a ``ListingGenerator`` which yields ``Submission``s.

        :param generator_kwargs: keyword arguments passed to
            :class:`~.ListingGenerator` constructor.
        :returns: A :class:`~.ListingGenerator` object which yields
            :class:`~.Submission` object.

        """
        path = API_PATH['live_discussions'].format(id=self.id)
        return ListingGenerator(self._reddit, path, **generator_kwargs)

    def edit(self, description, nsfw, resources, title):
        path = API_PATH['live_edit'].format(id=self.id)
        data = {'description': description, 'nsfw': nsfw,
                'resources': resources, 'title': title}
        return self._reddit.post(path, data=data)

    def invite_contributor(self, name, permissions, type_):
        path = API_PATH['live_invite_contributor'].format(id=self.id)
        data = {'name': str(name), 'permissions': permissions, 'type': type_}
        return self._reddit.post(path, data=data)

    def post_update(self, body):
        path = API_PATH['live_post_upate'].format(id=self.id)
        data = {'body': body}
        return self._reddit.post(path, data=data)

    # def report(self, type):
    #    path = API_PATH['live_report'].format(id=self.id)
    #    data = {'type': type}
    #    return self._reddit.post(path, data=data)

    def remove_contributor(self, redditor_id):
        path = API_PATH['live_remove_contributor'].format(id=self.id)
        data = {'id': redditor_id}
        return self._reddit.post(path, data=data)

    def remove_contributor_invite(self, redditor_id):
        path = API_PATH['live_remove_contributor_invite'].format(id=self.id)
        data = {'id': redditor_id}
        return self._reddit.post(path, data=data)

    def set_contributor_permissions(self, name, permissions, type_):
        path = API_PATH['live_set_contributor_permissions'].format(id=self.id)
        data = {'name': name, 'permissions': permissions, 'type': type_}
        return self._reddit.post(path, data=data)

    def strike_update(self, update_id):
        path = API_PATH['live_strike_update'].format(id=self.id)
        data = {'id': update_id}
        return self._reddit.post(path, data=data)

    def updates(self, **generator_kwargs):
        """Return a ``ListingGenerator`` which yields :class:`~.LiveUpdate``s.

        :param generator_kwargs: keyword arguments passed to
            :class:`~.ListingGenerator` constructor.
        :returns: A :class:`ListingGenerator` object which yields
            :class:`~.LiveUpdate` object.
        """
        path = API_PATH['live_thread'].format(id=self.id)
        return ListingGenerator(self._reddit, path, **generator_kwargs)
