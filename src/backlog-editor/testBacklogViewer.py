#! /usr/bin/env python

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
