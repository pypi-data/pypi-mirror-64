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


class ScriptVariable(Variable):
    script_name = None
    now_calculated = False

    def __init__(self, variable_name, document, context):
        super(ScriptVariable, self).__init__(variable_name, document, context)
        if 'script_name' not in document['from_script']:
            raise Exception('Missing "script_name" in variable definition ' + variable_name)

        self.script_name = document['from_script']['script_name']

    @property
    def value(self):
        # TODO: change to locks/mutex/atomic
        if self.now_calculated:
            return ''
        else:
            self.now_calculated = True
        if self.script_name not in self.context.scripts:
            raise Exception('Missing script ' + self.script_name + ' to calculate variable ' + self.variable_name)

        script = self.context.scripts[self.script_name]
        value = script.execute(for_variable=self.variable_name)
        self.now_calculated = False
        return value
