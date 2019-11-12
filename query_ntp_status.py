#!/usr/bin/python

#   Copyright 2018 Kevin Godden
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import subprocess
import json
import re
import sys

# Shell out to 'ntpq -p'
proc = subprocess.Popen(['ntpq', '-p'], stdout=subprocess.PIPE)

# Get the output
stdout_value = proc.communicate()[0].decode("utf-8")

#remove the header lines
start = stdout_value.find("===\n")

if start == -1:
    # We may be running on windows (\r\n), try \r...
    start = stdout_value.find("===\r")

    if start == -1:
        # No, go, exit with error
        result = {'query_result': 'failed', 'data': {}}
        print(json.dumps(result))
        sys.exit(1)

# Get the data part of the string
#pay_dirt = stdout_value[start+4:]
pay_dirt = stdout_value[start:]

# search for NTP line starting with * (primary server)
exp = ("\*((?P<remote>\S+)\s+)"
       "((?P<refid>\S+)\s+)"
       "((?P<st>\S+)\s+)"
       "((?P<t>\S+)\s+)"
       "((?P<when>\S+)\s+)"
       "((?P<poll>\S+)\s+)"
       "((?P<reach>\S+)\s+)"
       "((?P<delay>\S+)\s+)"
       "((?P<offset>\S+)\s+)"
       "((?P<jitter>\S+)\s+)")

regex = re.compile(exp, re.MULTILINE)
r = regex.search(pay_dirt)

# Did we get anything?
if not r:
    # No, try again without the * at the beginning, get
    # the first entry instead
    exp = (" ((?P<remote>\S+)\s+)"
           "((?P<refid>\S+)\s+)"
           "((?P<st>\S+)\s+)"
           "((?P<t>\S+)\s+)"
           "((?P<when>\S+)\s+)"
           "((?P<poll>\S+)\s+)"
           "((?P<reach>\S+)\s+)"
           "((?P<delay>\S+)\s+)"
           "((?P<offset>\S+)\s+)"
           "((?P<jitter>\S+)\s+)")

    regex = re.compile(exp, re.MULTILINE)
    r = regex.search(pay_dirt)

data = {}

if r:
    data = r.groupdict()

# Output Result
result = {'query_result': 'ok' if r else 'failed', 'data': data}

print(json.dumps(result))
