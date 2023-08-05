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

from starsheep.variables.variable import Variable


class CmdLineVariable(Variable):
    _value = None

    def __init__(self, variable_name, document, context):
        super(CmdLineVariable, self).__init__(variable_name, document, context)
        if 'from_cmdline' not in document:
            raise Exception('Missing "option" in variable')

        for o in context.cmdline:
            if o.startswith('--' + document['from_cmdline']):
                self._value = o.split('=')[1]
        if self._value is None:
            raise Exception('Missing option for variable ' + variable_name + " --" + document['from_cmdline'] + '=...')

    @property
    def value(self):
        return self._value