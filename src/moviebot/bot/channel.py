"""
Helper class for determining the type of channel,
based on settings
"""

import os
from enum import Enum


class ChannelType(Enum):
    """
    Enumeration of channel types, used
    in place of specific channel names
    """

    COMMANDS_CHANNEL = 1
    REQUESTS_CHANNEL = 2 # TODO: Rename to SUGGESTIONS_CHANNEL


def channel_type(name):
    """
    Determines channel type given a channel name, using the
    COMMANDS_CHANNEL and REQUESTS_CHANNEL env variables

    This is a placeholder implementation until I need better
    multi-channel support
    """
    if name in os.environ["COMMANDS_CHANNEL"]:
        return ChannelType.COMMANDS_CHANNEL
    if name in os.environ["SUGGESTIONS_CHANNEL"]:
        return ChannelType.REQUESTS_CHANNEL
    return None


def sort_channels(channels):
    """
    Takes a list of channels, and returns a dictionary with keys of
    ChannelType and values of List[Channel]
    """

    output = {}
    for channel in channels:
        chan_type = channel_type(channel.name)
        output[chan_type] = output.get(chan_type, []) + [channel]
