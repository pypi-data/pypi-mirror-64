"""Tools for the UK's DVB-T network (Freeview)."""

from enum import Enum
import time

from . import _util as networkutil

LANGUAGE = 'eng'


class Genre (Enum):
    """Possible values for a programme's genre."""

    UNKNOWN = None
    """Genre didn't match any known value."""

    ARTS = b'\x02\x00\x00\x00\x00\x01p'
    CHILDRENS = b'\x02\x00\x00\x00\x00\x01P'
    EDUCATION = b'\x02\x00\x00\x00\x00\x01\x90'
    FILM = b'\x02\x00\x00\x00\x00\x01\x10'
    """Also used for most fictional series."""
    GAME_SHOW = b'\x02\x00\x00\x00\x00\x010'
    HOBBIES = b'\x02\x00\x00\x00\x00\x01\xa0'
    MUSIC = b'\x02\x00\x00\x00\x00\x01`'
    NEWS = b'\x02\x00\x00\x00\x00\x01 '
    POLITICAL = b'\x02\x00\x00\x00\x00\x01\x80'
    SPORT = b'\x02\x00\x00\x00\x00\x01@'


def _localise (strings):
    """Localise a localisable string for this network."""
    return networkutil.localise(LANGUAGE, strings)


def _normalise_desc (title, subtitle, summary):
    """Remove non-content and duplicated data from descriptive fields.

Returns (title, subtitle, summary).
"""
    # when subtitle and summary are the same, they're a description
    if subtitle == summary:
        subtitle = ''

    # title sometimes starts with an indicator that this is part of a new series
    norm_title = title.lower()
    if (norm_title.startswith('new: ') or
        norm_title.startswith('new. ')
    ):
        title = title[5:].lstrip()

    # title is sometimes continued in the subtitle
    if title.endswith('...') and subtitle.startswith('...'):
        subtitle_parts = subtitle.split('. ', maxsplit=1)
        if len(subtitle_parts) == 2:
            title = title[:-3].rstrip() + ' ' + subtitle_parts[0][3:].lstrip()
            subtitle = subtitle_parts[1].lstrip()

    return (title, subtitle, summary)


class Programme:
    """:class:`pyepgdb.values.Programme` wrapper specific to this network."""

    def __init__ (self, raw_programme):
        episode = raw_programme.episode
        broadcast = raw_programme.broadcast

        self.id_ = networkutil.read_value(
            episode, 'uri', networkutil.validate(str))
        """Unique identifier."""
        self.genre = Genre(networkutil.read_value(
            episode, 'genre', networkutil.validate(bytes, True, None)))
        """:class:`Genre` of the programme."""
        raw_title = _localise(networkutil.read_value(
            episode, 'title',
            networkutil.validate_map(networkutil.validate(str), True, {})))
        raw_subtitle = _localise(networkutil.read_value(
            episode, 'subtitle',
            networkutil.validate_map(networkutil.validate(str), True, {})))
        raw_summary = _localise(networkutil.read_value(
            broadcast, 'summary',
            networkutil.validate_map(networkutil.validate(str), True, {})))
        title, subtitle, summary = _normalise_desc(
            raw_title, raw_subtitle, raw_summary)
        self.title = title
        """Localised programme title."""
        self.subtitle = subtitle
        """Localised programme subtitle.  Often empty."""

        self.start = time.gmtime(networkutil.read_value(
            broadcast, 'start', networkutil.validate(int)))
        """:class:`time.struct_time` the broadcast starts."""
        self.stop = time.gmtime(networkutil.read_value(
            broadcast, 'stop', networkutil.validate(int)))
        """:class:`time.struct_time` the broadcast ends."""
        self.channel = networkutil.read_value(
            broadcast, 'channel', networkutil.validate(str))
        """Identifier corresponding to the channel hosting the broadcast."""
        self.summary = summary
        """Localised broadcast description."""
        self.widescreen = bool(networkutil.read_value(
            broadcast, 'is_widescreen', networkutil.validate(int, True, 0)))
        """Whether the broadcast is in widescreen."""
        self.subtitled = bool(networkutil.read_value(
            broadcast, 'is_subtitled', networkutil.validate(int, True, 0)))
        """Whether the broadcast has subtitles."""
        self.audio_desc = bool(networkutil.read_value(
            broadcast, 'is_audio_desc', networkutil.validate(int, True, 0)))
        """Whether the broadcast includes an audio description."""
        self.signed = bool(networkutil.read_value(
            broadcast, 'is_deafsigned', networkutil.validate(int, True, 0)))
        """Whether the broadcast includes sign language."""


def parse (programmes):
    """Validate and parse known programme fields specific to this network.

:arg pyepgdb.values.Programme programmes:
    Programmes parsed in a non-network-specific manner

:rtype: dvbtuk.Programme

"""

    for raw_programme in programmes:
        yield Programme(raw_programme)
