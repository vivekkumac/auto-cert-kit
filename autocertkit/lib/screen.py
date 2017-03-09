#!/usr/bin/python

# Copyright (c) Citrix Systems Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided
# that the following conditions are met:
#
# *   Redistributions of source code must retain the above
#     copyright notice, this list of conditions and the
#     following disclaimer.
# *   Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the
#     following disclaimer in the documentation and/or other
#     materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

""" Library Module for interactive display of the kit."""

class AutoCertScreenConstants(object):
    TYPE_WELCOME = "welcomeScreen"
    TYPE_EULA = "eulaScreen"
    TYPE_CONFIG = "configScreen"
    TYPE_NET_CONFIG = "networkConfigScreen"
    TYPE_STR_CONFIG = "storageConfigScreen"
    TYPE_TEST_LIST = "testListScreen"
    SEQUENCE = [TYPE_WELCOME, TYPE_CONFIG, TYPE_NET_CONFIG, TYPE_STR_CONFIG]

    ACTION_RELOAD = "reload"
    ACTION_NEXT = "next"
    ACTION_BACK = "back"

    PALETTE = [
        ('BODY', 'white', 'dark blue', 'standout'),
        ('FOCUS', 'black', 'light gray', 'standout'),
        ('INVERSE', 'dark blue', 'white', 'standout'),
        ('HEADER', 'white', 'black', 'bold'),
        ('FOOTER', 'white', 'dark blue', 'bold'),
        ('IMPORTANT', 'white', 'dark blue', ('standout', 'underline')),
        ('MESSAGE_RED', 'dark red', 'dark blue', 'bold'),
        ('ACTIVE', 'white', 'dark blue'),
        ('KEY', 'light cyan', 'dark blue', 'bold'),
    ]

    @classmethod
    def initClassVariables(cls):
        setattr(cls, "ALL_TYPE", [cls.__dict__[k] for k in cls.__dict__ if k.startswith("TYPE_")])
        setattr(cls, "ALL_ACTION", [cls.__dict__[k] for k in cls.__dict__ if k.startswith("ACTION_")])
        for p in cls.PALETTE:
            setattr(cls,  "P_%s" % p[0], p[0])

    @classmethod
    def getNextScreen(cls, screen):
        if screen not in cls.ALL_TYPE:
            raise Exception("Unkown ACK Screen: '%s'" % screen)
        if cls.SEQUENCE.count(screen)==1 and cls.SEQUENCE[-1] != screen:
            return cls.SEQUENCE[cls.SEQUENCE.index(screen)+1]
        return None

    @classmethod
    def getBackScreen(cls, screen):
        if screen not in cls.ALL_TYPE:
            raise Exception("Unkown ACK Screen: '%s'" % screen)
        if cls.SEQUENCE.count(screen)==1 and cls.SEQUENCE[0] != screen:
            return cls.SEQUENCE[cls.SEQUENCE.index(screen)-1]
        return None

    @classmethod
    def getScreenCompClass(cls, screen):
        if screen not in cls.ALL_TYPE:
            raise Exception("Unkown ACK Screen: '%s'" % screen)
        if screen == cls.TYPE_WELCOME:
            return WelcomeScreenComponents
        elif screen in [cls.TYPE_CONFIG, cls.TYPE_NET_CONFIG, cls.TYPE_STR_CONFIG]:
            return ConfigScreenComponents
        return None

AutoCertScreenConstants.initClassVariables()

class _ScreenComponents(object):

    T_HEADER = " Automated Certification Kit @KIT_VERSION@ "
    T_FOOTER = " SCROLL<arrow keys> | EXIT<f8> | SELECT<space/enter> "


class WelcomeScreenComponents(_ScreenComponents):
    T_TITLE = "INTRODUCTION"
    L_T_NAV_BUTTONS = [[('KEY', "N"), "ext"],
                           ["E", ('KEY', "x"), "it"]]
    T_INTRO = [('IMPORTANT', "The Automated Certification Kit (ACK)"),
                  """ is an automated test harness for certifying Servers, Network Cards and Storage devices for use with """,
                  ('IMPORTANT', 'XenServer'),
                  """.

The kit is designed to run automatically once the user has correctly configured their server, and external environment according to the instructions.

Whilst we do our best to ensure the kit is bug free, we are still working on improving the kit's robustness. if you encounter any issues, then we'd ask that you raise an appropriate bug ticket for us to investigate. """,
                  ('IMPORTANT', 'Citrix'),
                  """ is committed to improving both, kit's quality and value to both vendors and itself.

A number of vendors have expressed interested in integrating this kit into their own test systems. As much as possible, we have designed kit to be easy to integrate. If you feel there could be modifications made to the kit that would improve its usefulness for you, then please let us know.

If you are interested in contributing improvements to the kit, then please take a look at the project on GitHub:
""", ('INVERSE', 'https://github.com/xenserver/auto-cert-kit')]


class ConfigScreenComponents(_ScreenComponents):
    T_TITLE = "CONFIGURATION"
    T_USE_VLAN = [
        ('KEY', "U"), "se a VLAN tag ID for which switches have beem configured"]
    T_DEBUG = [ "Run in ",('KEY', "d"),"ebug mode, exit on failure"]
    T_VLAN_ID = None
    T_GENERATE = [('KEY', "G"), "enerate the config file only. Do not run the tests yet."]
    T_MODE = [('KEY', "S"),"pecify the type of certification you wish to perform. (ALL (default) | NET | LSTOR | CPU | OPS)."]
    T_EXCLUDE = [('KEY', "E"),"xclude one or multiple set of tests. (OVS | BRIDGE | LSTOR | CPU | OPS | CRASH)."]
    L_T_NAV_BUTTONS = [[('KEY', "B"), "ack"],[('KEY', "N"), "ext"]]


