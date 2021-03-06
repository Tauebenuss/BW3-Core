#!/usr/bin/python
# -*- coding: utf-8 -*-
"""!
    ____  ____  ______       __      __       __       _____
   / __ )/ __ \/ ___/ |     / /___ _/ /______/ /_     |__  /
  / __  / / / /\__ \| | /| / / __ `/ __/ ___/ __ \     /_ <
 / /_/ / /_/ /___/ /| |/ |/ / /_/ / /_/ /__/ / / /   ___/ /
/_____/\____//____/ |__/|__/\__,_/\__/\___/_/ /_/   /____/
                German BOS Information Script
                     by Bastian Schroll

@file:        test_config.py
@date:        08.01.2017
@author:      Bastian Schroll
@description: Unittests for BOSWatch. File must be _run as "pytest" unittest
"""
import logging

from boswatch.utils import paths
from boswatch.config import Config


class Test_Config:
    """!Unittests for the config"""

    def setup_method(self, method):
        logging.debug("[TEST] %s.%s", type(self).__name__, method.__name__)

    def test_loadLocalConfig(self):
        """!load a local config file"""
        bwConfig = Config()
        bwConfig.loadConfigFile(paths.TEST_PATH + "test.ini")
        assert bwConfig._config is not None

    def test_getLocalConfig(self):
        """!get values from local config file"""
        bwConfig = Config()
        bwConfig.loadConfigFile(paths.TEST_PATH + "test.ini")
        assert bwConfig.getInt("test", "one") == 1
        assert bwConfig.getBool("test", "one") is True
        assert bwConfig.getStr("test", "two") == "two"
        assert bwConfig.getStr("testcase", "test") == "ok"

    def test_getLocalConfigFailed(self):
        """!fail while get values from local config file"""
        bwConfig = Config()
        bwConfig.loadConfigFile(paths.TEST_PATH + "test.ini")
        assert bwConfig.getStr("test", "abc") is None
        assert bwConfig.getStr("abc", "test") is None

    def test_shareConfig(self):
        """!load local config file and share it"""
        bwConfig = Config()
        bwConfig.loadConfigFile(paths.TEST_PATH + "test.ini", "test_shareConfig")
        assert bwConfig._sharePoints["test_shareConfig"] is not None

    def test_shareConfigUsed(self):
        """!load local config file and tr to share it twice with same name"""
        bwConfig1 = Config()
        bwConfig1.loadConfigFile(paths.TEST_PATH + "test.ini", "test_shareConfigUsed")
        assert bwConfig1._sharePoints["test_shareConfigUsed"] is not None
        bwConfig2 = Config()
        bwConfig2.loadConfigFile(paths.TEST_PATH + "test.ini")
        assert not bwConfig2._shareConfig("test_shareConfigUsed")

    def test_getNotSetSharedConfig(self):
        """!try to get values from shared config where not exists"""
        bwConfig = Config()
        bwConfig.loadConfigFile(paths.TEST_PATH + "test.ini")
        assert bwConfig.getInt("test", "one") == 1
        assert bwConfig.getInt("test", "one", "NotSetSharedConfig") is None

    def test_getSharedConfig(self):
        """!get values from shared config file"""
        bwConfig1 = Config()
        bwConfig1.loadConfigFile(paths.TEST_PATH + "test.ini", "test_getSharedConfig")
        assert bwConfig1._sharePoints["test_getSharedConfig"] is not None

        bwConfig2 = Config()
        assert bwConfig2.getStr("test", "one") is None
        assert bwConfig2.getInt("test", "one", "test_getSharedConfig") == 1

    def test_getSharedConfigFailed(self):
        """!fail while get values from shared config file"""
        bwConfig1 = Config()
        bwConfig1.loadConfigFile(paths.TEST_PATH + "test.ini", "test_getSharedConfigFailed")
        assert bwConfig1._sharePoints["test_getSharedConfigFailed"] is not None

        bwConfig2 = Config()
        assert bwConfig2.getStr("test", "abc", "test_getSharedConfigFailed") is None
        assert bwConfig2.getStr("abc", "test", "test_getSharedConfigFailed") is None

    def test_getDataTypes(self):
        bwConfig = Config()
        bwConfig.loadConfigFile(paths.TEST_PATH + "test.ini")
        assert bwConfig.getStr("testcase", "test") == "ok"
        assert bwConfig.getInt("test", "one") == 1
        assert bwConfig.getInt("boolTest", "three") == 0
        assert bwConfig.getBool("boolTest", "one")
        assert bwConfig.getBool("boolTest", "two")
        assert not bwConfig.getBool("boolTest", "three")
        assert not bwConfig.getBool("boolTest", "four")

    def test_getAllSharepoints(self):
        bwConfig = Config()
        bwConfig.loadConfigFile(paths.TEST_PATH + "test.ini", "test_shareConfig")
        assert bwConfig.getAllSharepoints() is not None
