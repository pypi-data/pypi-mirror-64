'''
This file is a part of Arjuna
Copyright 2015-2020 Rahul Verma

Website: www.RahulVerma.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import pkg_resources
import time
import os
import sys

def join_paths(*paths):
    return os.path.abspath(os.path.join(*paths))

root_dir = join_paths(os.path.dirname(os.path.realpath(__file__)), "..")
importables_dir = join_paths(root_dir, "third_party")

sys.path.insert(0, importables_dir)
sys.path.insert(0, root_dir)

class ArjunFacade:

    def __init__(self):
        self.__version = pkg_resources.require("arjuna")[0].version

    def launch(self, raw_args):
        from arjuna.core.reader.textfile import TextResourceReader
        from arjuna.interface.cli import ArjunaCLI
        reader = TextResourceReader("header.txt")
        print(reader.read().format(version=self.__version))
        reader.close()

        print("Parsing CLI Options...")
        cli = ArjunaCLI(raw_args)
        # Initialize the Arjuna Core as per CLI options
        print("Intializing Arjuna...")
        cli.init()

        print("Executing Arjuna Command...")
        cli.execute()

from arjuna.engine import Arjuna

from arjuna.interact.gui.helpers import Attr, Point, Params, Formatter, Locator
from arjuna.interact.gui.gom import GuiApp, GuiPage, GuiSection, GuiWidget, GuiDialog

from arjuna.core.exceptions import *
from arjuna.core.enums import *
from arjuna.core.value import Value

from arjuna.core.audit import HardCoded

from arjuna.engine.hook import PytestHooks
from arjuna.engine.test import *
from arjuna.engine.data.markup import *
from arjuna.engine.data.record import *
from arjuna.engine.data.generator import Random, DataEntity, Locales
from arjuna.engine.relation import *
from arjuna.engine.fixture import *
from arjuna.core.xml import NodeLocator
from arjuna.core.adv.types import ProcessedKeyDict
from arjuna.core.json import Json
from arjuna.engine.logger import track

L = Arjuna.get_localized_str
C = Arjuna.get_config_value
R = Arjuna.get_dataref_value

class LogCall:

    def __init__(self, ctype):
        self.__ctype = ctype.lower()
    
    def __call__(self, msg, *args, contexts=None, **kwargs):
        from arjuna.core.audit import Stack
        if type(contexts) is str:
            contexts = (contexts,)
        elif contexts is None:
            contexts = ("default",)
        contexts = set(contexts)
        return getattr(Arjuna.get_logger(), self.__ctype)(msg, *args, extra={'invoker': Stack.get_invoker(), 'contexts':contexts, 'config':Arjuna.get_config()}, **kwargs)

log_trace = LogCall("trace")
log_debug = LogCall("debug")
log_info = LogCall("info")
log_warning = LogCall("warning")
log_error = LogCall("error")
log_fatal = LogCall("fatal")