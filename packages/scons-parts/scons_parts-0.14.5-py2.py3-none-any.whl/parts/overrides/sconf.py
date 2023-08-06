﻿
from __future__ import absolute_import, division, print_function

import SCons.SConf

# test to see if we have the function.. else backport it
# this is needed to support any version pre-Scons 2.4
try:
    SCons.SConf.NeedConfigHBuilder
except BaseException:

    def NeedConfigBuilder():
        return len(SCons.SConf._ac_config_hs) != 0

    SCons.SConf.NeedConfigHBuilder = NeedConfigBuilder
