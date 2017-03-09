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

"""Module for interactive display of the kit. This will help user to
provide config, check running status of the kit with better UI created
using text."""

import sys
import os
import urwid
from lib.screen import *

SCR = AutoCertScreenConstants

class _ScreenBase(object):

    _SCREEN = None

    def __init__(self, config):
        self.messageT = []
        self.listbox_content = []
        self.customKeys = {}
        self._config = config
        self._buttons = []
        self._checkboxes = []
        self._nScreen = None
        self._bScreen = None
        self._loadPreviousMessage()
        self._initVariables()
        self.loadScreen()

    def _initVariables(self):
        print("screen type: %s" % self._SCREEN)
        self._default = SCR.getScreenCompClass(self._SCREEN)
        self.headerT = self._default.T_HEADER
        self.footerT = self._default.T_FOOTER
        self.titleT = self._default.T_TITLE
        self.navBtntxts = self._default.L_T_NAV_BUTTONS

    def _loadPreviousMessage(self):
        if "_action" in self._config and self._config["_action"] == SCR.ACTION_RELOAD:
            if self._getScrConf("messageT"):
                self.messageT.extend(self._getScrConf("messageT"))

    def _prepareKey(self, objTxt, obj):
        for t in objTxt:
            if type(t) == tuple and t[0] == SCR.P_KEY and obj:
                self.customKeys[t[1]] = obj.label

    def _prepareButton(self, objTxt):
        obj = urwid.Button(objTxt, self._buttonAction)
        self._prepareKey(objTxt, obj)
        self._buttons.append((obj, objTxt))
        return urwid.LineBox(obj)

    def _prepareCheckbox(self, objTxt, state=False):
        obj = urwid.CheckBox(objTxt, state, on_state_change=self._checkboxAction)
        self._prepareKey(objTxt, obj)
        self._checkboxes.append((obj, objTxt))
        return obj

    def _prepareCheckBoxGrid(self, checkBoxTxtList):
        objList = []
        for cbT in checkBoxTxtList:
            obj = urwid.AttrMap(self._prepareiCheckbox(cbT), SCR.P_ACTIVE, SCR.P_FOCUS)
            objList.append((len(self._getLableFromTxtList(cbT))+6, obj))
        return urwid.Columns(objList, dividechars=2)

    def _prepareButtonGrid(self, buttonTxtList):
        objList = []
        for bT in buttonTxtList:
            obj = urwid.AttrMap(self._prepareButton(bT), SCR.P_ACTIVE, SCR.P_FOCUS)
            objList.append((len(self._getLableFromTxtList(bT))+10, obj))
        return urwid.Columns(objList, dividechars=2)

    def _buttonAction(self, button):
        btnLbl = button.get_label()
        self._performAction(btnLbl)

    def _checkboxAction(self, cbObj, newState):
        pass

    def _getLableFromTxtList(self, txtList):
        return "".join([t[1] if type(t)==tuple and len(t)==2 else t for t in txtList])

    def _saveScrConf(self):
        self._config["_screenConfig"] = {}
        for var in ["messageT"]:
            self._config["_screenConfig"][var] = self.__dict__[var]

    def _getScrConf(self, key):
        if "_screenConfig" in self._config and key in self._config["_screenConfig"]:
            return self._config["_screenConfig"][key]
        return None

    def _back(self):
        self._config["_screen"] = self._bScreen if self._bScreen else SCR.getBackScreen(self._SCREEN)
        self._config["_action"] = SCR.ACTION_BACK
        raise urwid.ExitMainLoop()

    def _next(self):
        self._config["_screen"] = self._nScreen if self._nScreen else SCR.getNextScreen(self._SCREEN)
        self._config["_action"] = SCR.ACTION_NEXT
        raise urwid.ExitMainLoop()

    def _reload(self):
        self._config["_screen"] = self._SCREEN
        self._config["_action"] = SCR.ACTION_RELOAD
        self._saveScrConf()
        raise urwid.ExitMainLoop()

    def _performAction(self, keyword):
        for cb,cbT in self._checkboxes:
            if cb.label == keyword:
                cb.toggle_state()
                return True
        if not self._customActions(keyword):
            return self._defaultActions(keyword)
        return True

    def _defaultActions(self, keyword):
        if keyword == "Next" or keyword == "Continue":
            self._next()
        elif keyword == "Back":
            self._back()
        elif keyword == "Exit":
            os.system("clear")
            sys.exit(0)
        else:
            return False
        return True

    def _customActions(self, keyword):
        # override if needed, return True if keyword is handled.
        return False

    def _buildListbox(self):
        raise NotImplementedError

    def _handleCustomKey(self, key):
        for k, label in self.customKeys.iteritems():
            if k and key and label and k.lower() == key.lower():
                return self._performAction(label)
        return False

    def _buildNavigation(self):
        self.listbox_content.append(self._prepareButtonGrid(self.navBtntxts))
        self.listbox_content.append(urwid.Divider())

    def _buildLineBox(self, dataDict):
        pileO = urwid.Pile([v for val in dataDict["seq"] for v in (val, urwid.Divider())])
        return urwid.LineBox(pileO, dataDict["title"])

    def _loadMessage(self):
        if self.messageT:
            messageO = urwid.Padding(urwid.AttrMap(urwid.Text(
                self.messageT, align="center"), SCR.P_MESSAGE_RED), left=3, right=3, min_width=20)
            pileO = urwid.Pile([urwid.Divider(), messageO])
            self.listbox_content[0] = pileO

    def loadScreen(self):
        self._buildListbox()
        self.listbox_content.append(urwid.Divider())

        if self.navBtntxts:
            self._buildNavigation()

        headerO = urwid.AttrMap(urwid.Text(self.headerT), SCR.P_HEADER)
        footerO = urwid.AttrMap(urwid.Text(self.footerT), SCR.P_FOOTER)

        self.listbox_content.insert(0, urwid.Divider())
        self._loadMessage()

        listbox = urwid.ListBox(urwid.SimpleListWalker(self.listbox_content))
        frame = urwid.Frame(urwid.AttrMap(urwid.LineBox(listbox, self.titleT), SCR.P_BODY),
                            header=headerO, footer=footerO)

        def handleKey(key):
            if key == 'f8':
                os.system("clear")
                sys.exit(0)
            elif key == 'tab':
                old_widget, old_position = listbox.get_focus()
                if type(old_widget) in [urwid.Columns, urwid.Pile]:
                    try:
                        old_grid_position = old_widget.focus_position
                    except IndexError:
                        old_grid_position = -1
                    if old_grid_position +1 < len(old_widget.contents):
                        old_widget.focus_position += 1
                        return True
                pos = old_position
                while True:
                    pos = (pos+1)% len(self.listbox_content)
                    listbox.set_focus(pos)
                    w, pos = listbox.get_focus()
                    if type(w) not in [urwid.Divider, urwid.Padding] :
                        break
                if type(old_widget) in [urwid.Columns, urwid.Pile]:
                    w.focus_position = 0
                    listbox.set_focus(pos)
                return True
            elif key == 'shift tab':
                old_widget, old_position = listbox.get_focus()
                if type(old_widget) in [urwid.Columns, urwid.Pile]:
                    try:
                        old_grid_position = old_widget.focus_position
                    except IndexError:
                        old_grid_position = -1
                    if old_grid_position>0:
                        old_widget.focus_position -= 1
                        return True
                pos = old_position
                while True:
                    pos = (pos-1)% len(self.listbox_content)
                    listbox.set_focus(pos)
                    w, pos = listbox.get_focus()
                    if type(w) not in [urwid.Divider, urwid.Padding] :
                        break
                if type(old_widget) in [urwid.Columns, urwid.Pile]:
                    w.focus_position = len(w.contents) - 1
                    listbox.set_focus(pos)
                return True
            elif type(key) == str:
                return self._handleCustomKey(key)
            return False
        urwid.MainLoop(frame, SCR.PALETTE, unhandled_input=handleKey).run()


class WelcomeScreen(_ScreenBase):

    _SCREEN = SCR.TYPE_WELCOME

    def _initVariables(self):
        super(WelcomeScreen, self)._initVariables()
        self.introT = self._default.T_INTRO

    def _buildListbox(self):
        introP = urwid.Padding(urwid.Text(
            self.introT), left=2, right=2, min_width=20)
        self.listbox_content.append(introP)
        self.listbox_content.append(urwid.Divider(top=3))


class ConfigScreen(_ScreenBase):

    _SCREEN = SCR.TYPE_CONFIG

    def _initVariables(self):
        super(ConfigScreen, self)._initVariables()
        self.useVlanT = self._default.T_USE_VLAN
        self.debugT = self._default.T_DEBUG
        self.vlanE = self._default.T_VLAN_ID
        self.generateT = self._default.T_GENERATE
        self.modeT = self._default.T_MODE
        self.exclude = self._default.T_EXCLUDE
        self.generalConfig = {
            "title" : "General Configurations",
            "seq": [
                urwid.Divider(),
                self._optionDebug(),
                self._optionGenerate() ]
            }
        self.advancedConfig = {
            "title" : "Advanced Configurations",
            "seq": [
                urwid.Divider(),
                self._optionVlan(),
                self._optionMode() ]
            }
        self.networkConfig = {
            "title" : "Network Configurations",
            "seq": [
                urwid.Divider()]
            }
        self.storageConfig = {
            "title" : "Storage Configurations",
            "seq": [ urwid.Divider() ]
            }

    def _checkboxAction(self, cbObj, newState):
        if self._getLableFromTxtList(self.useVlanT) == cbObj.label:
            self._config["useVlantag"] = newState
            self._reload()
        elif self._getLableFromTxtList(self.debugT) == cbObj.label:
            self._config["debug"] = newState
        elif self._getLableFromTxtList(self.generateT) == cbObj.label:
            self._config["generate"] = newState
        elif self._getLableFromTxtList(self.modeT) == cbObj.label:
            self._config["mode"] = newState

    def _optionVlan(self):
        isVlanO = self._optionGenericCb(self.useVlanT, "useVlantag")
        val = self._config["useVlantag"] if "useVlantag" in self._config else False
        if val:
            self.vlanE = urwid.IntEdit(
                "VLAN (1-4094) : ", self._config['vlan_id'] if 'vlan_id' in self._config else None)
            vlanC = urwid.Columns([(25, urwid.AttrMap(self.vlanE, SCR.P_ACTIVE, SCR.P_FOCUS))])
            vlanO = urwid.Padding(vlanC, left=8, right=0, min_width=20)
            return urwid.Pile([isVlanO , vlanO])
        return isVlanO

    def _optionGenericCb(self, txt, configKey, default=False):
        val = self._config[configKey] if configKey in self._config else default
        cb = urwid.AttrMap(self._prepareCheckbox(txt, val), SCR.P_ACTIVE, SCR.P_FOCUS)
        cbC = urwid.Columns([(len(self._getLableFromTxtList(txt))+5, cb)])
        return urwid.Pile([urwid.Padding(cbC, left=2, right=2, min_width=60)])

    def _optionDebug(self):
        return self._optionGenericCb(self.debugT, "debug")

    def _optionGenerate(self):
        return self._optionGenericCb(self.generateT, "generate")

    def _optionMode(self):
        return self._optionGenericCb(self.modeT, "mode")

    def _buildListbox(self):
        self.listbox_content = [
            self._buildLineBox(self.generalConfig),
            urwid.Divider(),
            self._buildLineBox(self.advancedConfig) ]

class NetworkConfigScreen(ConfigScreen):

    _SCREEN = SCR.TYPE_NET_CONFIG

    def _buildListbox(self):
        self.listbox_content = [
            self._buildLineBox(self.networkConfig) ]

class StorageConfigScreen(ConfigScreen):

    _SCREEN = SCR.TYPE_STR_CONFIG

    def _buildListbox(self):
        self.listbox_content = [
            self._buildLineBox(self.storageConfig) ]


config = {'debug': True,
        '_screen': SCR.TYPE_WELCOME,
        '_focus': None,
        'useVlantag': False
          }

# optionalArgs: vlan_id generate 

while config["_screen"]:
    if config["_screen"] == SCR.TYPE_WELCOME:
        WelcomeScreen(config)
    elif config["_screen"] == SCR.TYPE_CONFIG:
        ConfigScreen(config)
    elif config["_screen"] == SCR.TYPE_NET_CONFIG:
        NetworkConfigScreen(config)
    elif config["_screen"] == SCR.TYPE_STR_CONFIG:
        StorageConfigScreen(config)
    else:
        break

print config
