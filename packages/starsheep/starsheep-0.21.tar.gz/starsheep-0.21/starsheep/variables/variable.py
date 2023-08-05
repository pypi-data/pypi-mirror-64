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

import logging


class Variable(object):
    context = None
    variable_name = None

    def __init__(self, variable_name, document, context):
        self.context = context
        self.variable_name = variable_name
        logging.info('Created variable ' + self.variable_name)

    def __str__(self):
        return self.variable_name

    @property
    def value(self):
        raise Exception('Abstract method')

    @staticmethod
    def load(document, context):
        from starsheep.variables.static_variable import StaticVariable
        from starsheep.variables.model_vairable import ModelVariable
        from starsheep.variables.context_variable import ContextVariable
        from starsheep.variables.script_vairable import ScriptVariable
        from starsheep.variables.cmdline_variable import CmdLineVariable

        variables = {}

        if type(document) != dict:
            raise Exception('Variables is not a dictionary')

        for variable_name in document.keys():
            var = document[variable_name]
            if 'value' in var and type(var['value']) == str:
                variables[variable_name] = StaticVariable(variable_name, var, context)
            elif 'from_object' in var and type(var['from_object']) == dict:
                variables[variable_name] = ModelVariable(variable_name, var, context)
            elif 'from_script' in var and type(var['from_script']) == dict:
                variables[variable_name] = ScriptVariable(variable_name, var, context)
            elif 'from_changed' in var and type(var['from_changed']) == dict:
                variables[variable_name] = ContextVariable(variable_name, var, context)
            elif 'from_cmdline' in var and type(var['from_cmdline']) == str:
                variables[variable_name] = CmdLineVariable(variable_name, var, context)

        return variables
