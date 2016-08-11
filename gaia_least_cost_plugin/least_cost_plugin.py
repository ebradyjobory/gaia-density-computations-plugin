#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
#  Copyright Kitware Inc. and Epidemico Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
##############################################################################
from gaia.inputs import GaiaIO
from gaia.gaia_process import GaiaProcess
from gaia_least_cost_plugin import config


class LeastCostIO(GaiaIO):

    def __init__(self, uri='', **kwargs):
        super(LeastCostIO, self).__init__(uri=uri, **kwargs)
        print("Created LeastCostIO")
        print("Value of Gaia plugin config: {}".format(
            config.get('gaia_least_cost_plugin')))

    def read(self, *args, **kwargs):
        pass

    def write(self, *args, **kwargs):
        pass

    def delete(self):
        pass


class LeastCostProcess(GaiaProcess):

    def __init__(self, **kwargs):
        super(LeastCostProcess, self).__init__(**kwargs)
        print "Created LeastCostProcess"

    def compute(self):
        print ("Compute something with LeastCostProcess")


class HelperClassDoNotIncludeMe(object):

    def __init__(self):
        print("Don't include me as a valid class in Gaia Parser")


PLUGIN_CLASS_EXPORTS = [
    LeastCostProcess,
    LeastCostIO,
]

if __name__ == '__main__':
    LeastCostIO = LeastCostIO(uri='foo')
