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

"""A module for utility functions shared with storage test cases"""
from utils import call_ack_plugin, log


def is_multipathing(session, host):
    try:
        hconf = session.xenapi.host.get_other_config(host)
        log("Host.other_config: %s" % hconf)
        if hconf['multipathing'] == 'true' and hconf['multipathhandle'] == 'dmp':
            return True
    except Exception, e:
        log("Exception determining multipath status. Exception: %s" % str(e))
    return False


def enable_multipathing(session, host):
    try:
        session.xenapi.host.remove_from_other_config(host, 'multipathing')
        session.xenapi.host.remove_from_other_config(host, 'multipathhandle')
        session.xenapi.host.add_to_other_config(host, 'multipathing', 'true')
        session.xenapi.host.add_to_other_config(host, 'multipathhandle', 'dmp')
    except Exception, e:
        log("Exception enabling multipathing. Exception: %s" % str(e))


def disable_multipathing(session, host):
    try:
        session.xenapi.host.remove_from_other_config(host, 'multipathing')
        session.xenapi.host.remove_from_other_config(host, 'multipathhandle')
        session.xenapi.host.add_to_other_config(host, 'multipathing', 'false')
    except Exception, e:
        log("Exception disabling multipathing. Exception: %s" % str(e))


def createSR(session, host, TODO):
    # TODO
    pass


def attachSR(session, host, sr, TODO):
    # TODO
    pass
