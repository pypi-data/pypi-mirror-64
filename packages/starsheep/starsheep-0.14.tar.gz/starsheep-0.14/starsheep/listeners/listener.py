# Copyright (c) 2020 cloudover.io
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import dinemic
import logging

class Listener(dinemic.DAction):
    listener_name = None
    call_on = None
    action = None
    context = None
    trigger = None

    def __init__(self, listener_name, document, context):
        super(Listener, self).__init__()

        self.context = context
        self.listener_name = listener_name

        self.action = document['action']
        self.trigger = document['trigger']

        if type(document['call_on']) == list:
            self.call_on = document['call_on']
        else:
            self.call_on = [document['call_on']]

        logging.info('New listener ' + self.listener_name)

        if self.trigger != "!":
            self.starsheep_apply(self.trigger)
            logging.info('Registered listener ' + self.listener_name + ' on ' + self.trigger)

    def __str__(self):
        return self.listener_name

    def call(self):
        raise Exception('Abstract method')

    def starsheep_apply(self, listener_filter):
        raise Exception('Abstract method')

    @staticmethod
    def load(document, context):
        from starsheep.listeners.reject_listener import RejectListener
        from starsheep.listeners.script_listener import ScriptListener

        if context.listeners is None:
            context.listeners = {}

        for listener_name in document.keys():
            if 'call_on' not in document[listener_name]:
                print('Missing "call_on" in ' + listener_name)
                continue
            if 'trigger' not in document[listener_name]:
                print('Missing "trigger" in ' + listener_name)
                continue
            if 'action' not in document[listener_name]:
                print('Missing "action" in ' + listener_name)
                continue

            if document[listener_name]['action'] == 'reject':
                context.listeners[listener_name] = RejectListener(listener_name, document[listener_name], context)
            elif document[listener_name]['action'] == 'script':
                context.listeners[listener_name] = ScriptListener(listener_name, document[listener_name], context)

