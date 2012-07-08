#! /usr/bin/env python

import mox

import wx

import unittest

myWx = wx

def set_wx(my=wx):
    global myWx
    myWx = my

def sut_call_wxapp():
    app=myWx.App()
    return app

class moxTest(unittest.TestCase):
    def test_sut(self):
        myMox=mox.Mox()
        wxMox = myMox.CreateMock(wx) 
        wxMox.App().AndReturn("App Called")
        myMox.ReplayAll()
        set_wx(wxMox)
        self.assertEqual("App Called", sut_call_wxapp())
        myMox.VerifyAll()

def main():
    unittest.main()


if __name__=='__main__':
  main()

