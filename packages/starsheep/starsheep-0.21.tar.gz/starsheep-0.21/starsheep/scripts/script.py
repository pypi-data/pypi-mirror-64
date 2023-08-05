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

import tempfile
import os
import subprocess
import logging


class Script(object):
    context = None
    script_name = None
    interpreter = None
    variables = None
    script_contents = None
    timeout = None

    def __init__(self, script_name, document, variables, context):
        self.context = context
        self.script_name = script_name
        self.interpreter = document['interpreter']
        self.script_contents = document['script']
        self.variables = variables

        if 'timeout' in document:
            self.timeout = document['timeout']
        else:
            timeout = 60

        logging.info('Created script ' + self.script_name)

    def __str__(self):
        return self.script_name

    def execute(self, variables={}, for_variable=None):
        '''
        :param variables: List of additional, local variables for this script
        :param for_variable: Name of variable. Used only by ScriptVariable class to aviod recursion
        :return:
        '''
        path_t = tempfile.mkstemp(prefix='starsheep-script-')
        os.close(path_t[0])
        f = open(path_t[1], 'w')
        f.write(self.script_contents)
        f.close()

        env = {}
        for v in self.context.variables:
            if v != for_variable:
                env['' + v.upper()] = self.context.variables[v].value
        for v in self.variables:
            if v != for_variable:
                env['' + v.upper()] = self.variables[v].value
        for v in variables:
            env['' + v.upper()] = variables[v]

        output = ''

        if os.path.exists(self.interpreter):
            call = subprocess.Popen([self.interpreter, path_t[1]], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                rc = call.wait(timeout=self.timeout)
            except subprocess.TimeoutExpired as e:
                logging.info('Script output: ' + call.stdout.read().decode('utf-8'))
                logging.info('Script error: ' + call.stderr.read().decode('utf-8'))
                
                os.remove(path_t[1])
                raise Exception('Script ' + self.script_name + ' timeout ' + str(self.timeout) + 's')

            if rc != 0:
                logging.info('Script output: ' + call.stdout.read().decode('utf-8'))
                logging.info('Script error: ' + call.stderr.read().decode('utf-8'))
                os.remove(path_t[1])
                raise Exception('Script ' + self.script_name + ' failed')

            std_out = call.stdout.read().decode('utf-8')
            std_err = call.stderr.read().decode('utf-8')
            logging.info('Script output: ' + std_out)
            logging.info('Script error: ' + std_err)

            os.remove(path_t[1])

            return std_out
        else:
            os.remove(path_t[1])
            return ''

    @staticmethod
    def load(document, context):
        from starsheep.variables.variable import Variable

        if context.scripts is None:
            context.scripts = {}

        for script_name in document.keys():
            if 'script' not in document[script_name]:
                logging.error('Missing "script" in ' + script_name)
                continue
            if 'interpreter' not in document[script_name]:
                logging.error('Missing "interpreter" in ' + script_name)
                continue

            variables = {}

            if 'variables' in document[script_name]:
                variables.update(Variable.load(document[script_name]['variables'], context))

            context.scripts[script_name] = Script(script_name, document[script_name], variables, context)

