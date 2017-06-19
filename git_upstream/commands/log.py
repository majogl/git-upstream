#
# Copyright (c) 2012-2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from __future__ import print_function
from git_upstream import lib
from git_upstream.commands import GitUpstreamCommand
from git_upstream.log import LogDedentMixin
from git_upstream.lib.utils import GitMixin
import subprocess


class Log(LogDedentMixin, GitMixin):

    pretty = 'format:%C(yellow)%h%Creset|%Cgreen%ad%Creset|%Cred%><(6,trunc)%N%-%Creset|%Cblue%an%Cgreen%d%x09%Creset%s'

    def __init__(self, log_command, *args, **kwargs):

        # make sure to correctly initialize inherited objects before performing
        # any computation
        super(Log, self).__init__(*args, **kwargs)
        self.log_command = log_command

    def show(self):
		args = ["git", "log", "--pretty=" + self.pretty, "--show-notes=*", "--date=short"]
		# TODO: replace with git_upstream.log ?
		proc = subprocess.Popen(args + self.log_command,stdout=subprocess.PIPE)
		for line in proc.stdout:
			print(line,end='')
		print('\n')
		#TODO: replace("Dropp..>", "Dropped")


class LogCommand(LogDedentMixin, GitUpstreamCommand):
    """Display pretty formatted log."""
    name = "log"

    def __init__(self, *args, **kwargs):
        super(LogCommand, self).__init__(*args, **kwargs)

        self.parser.add_argument('log_command', metavar='<log_command>', nargs='*',
            help="What should be passed to git log <log_command>")

    def execute(self, parent_parser=None):
        #print self.args.length
        log = Log(self.args.log_command)
        log.show()
