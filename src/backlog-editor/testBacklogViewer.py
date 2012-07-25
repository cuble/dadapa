#! /usr/bin/env python

#   Copyright 2012 Chen Gang(fouryusteel@gmail.com)
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


import unittest
import mox
from backlogViewer import viewer
import backlogViewer
import wx

class backlogViewerTest(unittest.TestCase):
    def test_viewer_main(self):
        self.mox=mox.Mox()
        guiMock=self.mox.CreateMock(wx)
        appMock = self.mox.CreateMockAnything()
        self.mox.StubOutClassWithMocks(backlogViewer, 'mainWindow')
        
        guiMock.App(False).AndReturn(appMock)
        backlogViewer.mainWindow()
        appMock.MainLoop()
        self.mox.ReplayAll()
        
        myView = viewer(guiMock)
        myView.main()
        self.mox.VerifyAll()

if __name__=='__main__':
    unittest.main()
