
ABAP_GIT_DEFAULT_XML='''<?xml version="1.0" encoding="utf-8"?>
<asx:abap xmlns:asx="http://www.sap.com/abapxml" version="1.0">
 <asx:values>
  <DATA>
   <MASTER_LANGUAGE>E</MASTER_LANGUAGE>
   <STARTING_FOLDER>/src/</STARTING_FOLDER>
   <FOLDER_LOGIC>PREFIX</FOLDER_LOGIC>
   <IGNORE>
    <item>/.travis.yml</item>
    <item>/CONTRIBUTING.md</item>
    <item>/LICENSE</item>
    <item>/README.md</item>
   </IGNORE>
  </DATA>
 </asx:values>
</asx:abap>
'''

# Minimal stubs for test imports
class PatcherTestCase:
    def setUp(self):
        pass
    def patch(self, *args, **kwargs):
        from unittest.mock import patch
        p = patch(*args, **kwargs)
        started = p.start()
        self.addCleanup(p.stop)
        return started
    def addCleanup(self, func):
        pass

class ConsoleOutputTestCase:
    def setUp(self):
        self.console = type('Console', (), {'capout': '', 'caperr': ''})()
    def patch_console(self, console=None):
        self.console = console or self.console
    def assertConsoleContents(self, console, stdout=None, stderr=None):
        if stdout:
            assert stdout in getattr(console, 'capout', '')
        if stderr:
            assert stderr in getattr(console, 'caperr', '')

def generate_parse_args(command_group):
    def parser(*args, **kwargs):
        class Args:
            def execute(self, conn, args):
                return 0
        return Args()
    return parser
