#! /usr/bin/env python

import mox

import wx

import unittest

class myWx:
    def App(self):
        return wx.App()

def sut_call_wxapp(myWx):
    app=myWx.App()
    return app

class moxTest(unittest.TestCase):
    def setUp(self):
        self.mox=mox.Mox()
    def tearDown(self):
        self.mox.UnsetStubs()
        self.mox.VerifyAll()

    def test_mock_basic(self):
        self.wxMox = self.mox.CreateMock(myWx)
        self.wxMox.App().AndReturn("App Called Basic")
        self.mox.ReplayAll()
        self.assertEqual("App Called Basic", sut_call_wxapp(self.wxMox))

    def test_stub_out(self):
        testWx = myWx()
        self.mox.StubOutWithMock(testWx, "App")
        testWx.App().AndReturn("App Called By Stub")
        self.mox.ReplayAll()
        self.assertEqual("App Called By Stub", sut_call_wxapp(testWx)) 

    def test_mock_anything(self):
        testWx = myWx()
        mock_app=self.mox.CreateMockAnything()
        testWx.App = mock_app
        mock_app().AndReturn("App Called By Mock Anything")
        self.mox.ReplayAll()
        self.assertEqual("App Called By Mock Anything", sut_call_wxapp(testWx))

def main():
    unittest.main()


if __name__=='__main__':
  main()

