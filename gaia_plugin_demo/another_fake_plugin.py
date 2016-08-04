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


class AnotherFakeIO(GaiaIO):

    def __init__(self, uri='', **kwargs):
        print "Created AnotherFakeIO"

    def read(self, *args, **kwargs):
        pass

    def write(self, *args, **kwargs):
        pass

    def delete(self):
        pass


class AnotherFakeProcess(GaiaProcess):

    def __init__(self, **kwargs):
        super(AnotherFakeProcess, self).__init__(**kwargs)
        print "Created AnotherFakeProcess"

    def compute(self):
        print ("Compute something with AnotherFakeProcess")


PLUGIN_CLASS_EXPORTS = [
    AnotherFakeIO,
    AnotherFakeProcess
]