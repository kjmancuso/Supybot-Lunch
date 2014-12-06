###
# Copyright (c) 2014, Kevin Mancuso
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import random

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Lunch')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class Lunch(callbacks.Plugin):
    """Add the help for "@plugin help Lunch" here
    This should describe *how* to use this plugin."""

    def get_places(self, chan):
        places = self.registryValue('places', chan)
        return places

    def lunch(self, irc, msg, args):
        # Reject query if privmsg
        if not ircutils.isChannel(msg.args[0]):
            irc.reply('I will not reply to your soft whispers.')
            return

        # Look for channel in arguments, else assume current channel is target
        for i in args:
            if ircutils.isChannel(i):
                chan = i
                args.remove(i)
                break
        else:
            chan = msg.args[0]

        # Look for arguments else spit list
        if not args:
            places = self.get_places(chan)
            if len(places) == 0:
                irc.reply('My list is empty, why not tell me what you like to',
                          'eat?')
            else:
                eatme = random.choice(places)
                irc.reply(eatme)
        elif 'add' in args:
            args.remove('add')
            place = ' '.join(args)
            places = self.get_places(chan)
            if place in places:
                irc.reply('%s already in list for %s' % (place, chan))
                return
            places.append(place)
            self.setRegistryValue('places', places, chan)
            irc.reply('Added %s to %s\'s list.' % (place, chan))
        elif 'remove' in args:
            args.remove('remove')
            place = ' '.join(args)
            places = self.get_places(chan)
            if place not in places:
                irc.reply('%s not found in list for %s' % (place, chan))
                return
            places.remove(place)
            self.setRegistryValue('places', places, chan)
            irc.reply('Removed %s from %s\'s list.' % (place, chan))
        elif 'list' in args:
            places = ', '.join(self.get_places(chan))
            if len(places) == 0:
                irc.reply('List for %s is empty.' % chan)
            else:
                irc.reply(places)
        else:
            irc.reply('Unknown command.')


Class = Lunch


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
