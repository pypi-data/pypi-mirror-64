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

class Context(object):
    debug = False
    variables = None
    scripts = None
    listeners = None
    models = None

    cmdline = []

    current_model = None
    current_field = None

    def __init__(self, debug=False):
        self.debug = debug

        self.variables = {}
        self.scripts = {}
        self.listeners = {}
        self.models = {}

    def __str__(self):
        r = ''
        r += 'Variables:\n'
        for v in self.variables:
            r += str(self.variables[v]) + '\n'

        r += '\nScripts:\n'
        for s in self.scripts:
            r += str(self.scripts[s]) + '\n'

        r += '\nListeners:\n'
        for l in self.listeners:
            r += str(self.listeners[l]) + '\n'

        r += '\nModels:\n'
        for m in self.models:
            r += str(self.models[m]) + '\n'

        return r