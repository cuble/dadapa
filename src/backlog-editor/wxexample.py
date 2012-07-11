#! /usr/bin/env python

import os
import wx
from wx.lib.wordwrap import wordwrap

class myPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        hSizer=wx.BoxSizer(wx.HORIZONTAL)
        
        self.button=wx.Button(self, label="Clear", size=(70,30))
        self.Bind(wx.EVT_BUTTON, self.onClear,self.button)
        hSizer.Add(self.button,0)

        self.checkBox=wx.CheckBox(self, label="Is it checked?")
        self.Bind(wx.EVT_CHECKBOX, self.onCheckBox, self.checkBox)
        hSizer.Add(self.checkBox, 0, wx.ALIGN_CENTER_VERTICAL)
        
        self.SetSizerAndFit(hSizer)
        
    def onClear(self, event):
        self.Parent.onClear()

    def onCheckBox(self, event):
        self.Parent.onCheckBox(self.checkBox.GetValue())

class myFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        self.dirname = os.getcwdu()
        self.path=''
        if os.path.isfile('./wxpdemo.ico'):
            self.ico = wx.Icon('wxpdemo.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.ico)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel = myPanel(self)
        vSizer.Add(self.panel,0,wx.EXPAND)
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE, size=(600,600))
        vSizer.Add(self.control,1, wx.EXPAND)
        self.CreateStatusBar()
        
        filemenu = wx.Menu()

        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", " Open a file")
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        
        menuSave = filemenu.Append(wx.ID_SAVE, "&Save", " Save file")
        self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)
        self.SetSizerAndFit(vSizer)
        # self.SetSizer(vSizer)
        # self.SetAutoLayout(True)
        # vSizer.Fit(self)
        self.Show(True)
        
    def setFileName(self, name):
        self.path = name
        self.Title = name
        
    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "Sample Editor"
        info.Version = "0.1.0"
        info.Copyright = "(C) 2012 Programmers and Coders Everywhere"
        info.Description = wordwrap(
        'The "Sample Editor" is my wxPython study example for my backlog-viewer'
        'I will try needed features in this simple project'
        'Then try to confirm the architecture of backlog-viewer',
        350, wx.ClientDC(self))
        info.WebSite = ("https://myspace.inside.nokiasiemensnetworks.com/Person.aspx?accountname=nsn-intra\g1cheng", "My Home Page")
        info.Developers = ["Chen Gang"]        
        wx.AboutBox(info)

    def OnExit(self, event):
        self.Close(True)

    def OnOpen(self,event):
        """ Open a file"""
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.txt", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.setFileName(dlg.GetPath())
            if self.path : 
                f = open(self.path, 'r')
                self.control.SetValue(f.read())
                f.close()
        dlg.Destroy()
        
    def OnSave(self, event):
        if self.path == '':
            dlg = wx.FileDialog(self, "Save the file", self.dirname, "", "*.txt", wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:
                self.setFileName(dlg.GetPath())
            else:
                return             
        f=open(self.path, 'w+')
        f.write(self.control.GetValue())
        f.close()
        
    def onClear(self):
        self.control.SetValue("")
        
    def onCheckBox(self, isChecked):
        if isChecked: self.control.AppendText("The checkBox Checked\n")
        else: self.control.AppendText("The checkBox Unchecked\n")

if __name__=='__main__':
    app = wx.App(False)
    myFrame(None, "Sample Editor")
    app.MainLoop()

