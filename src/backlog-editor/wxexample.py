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


import os
import wx
import wx.stc as stc
import codecs

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

class myStcConfiguration:
    def __init__(self):
        self.activeItemBackground = wx.LIGHT_GREY
        self.tabIndentLen = 4
        self.textFonts = []
        self.textFonts.append(('Times New Roman', 12))
        self.textFonts.append(('Times New Roman', 10))

class myStc(stc.StyledTextCtrl):
    def __init__(self, parent, config, size=(600,400)):
        stc.StyledTextCtrl.__init__(self, parent, size=size)
        self.config = config
        
        self.maxDepth = len(self.config.textFonts)
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%s, size:%d" % ('Times New Roma', 12))
        self.StyleClearAll()
        fontIdx = 1
        for font in self.config.textFonts:
            self.StyleSetSpec(fontIdx, "bold,face:%s,size:%d,fore:#0000FF" % (font[0], font[1]))
    
        self.SetCaretLineBackground(self.config.activeItemBackground)
        #self.SetCaretLineBackAlpha(80)
        self.SetCaretLineVisible(True)

        self.mode = 'View'
        
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down, self)
        self.show_work_mode()
        
        font = self.GetFont()
        print 

    def show_work_mode(self):
        parent = self.GetParent()
        parent.statusBar.SetStatusText("Current work mode is: " + self.mode)

    def work_in_view_mode(self, evt):
        keyCode = evt.GetKeyCode()
        if keyCode in (wx.WXK_SPACE, wx.WXK_INSERT): 
            self.mode = 'Edit'
            if keyCode == wx.WXK_INSERT:
                self.LineEnd()
                self.AddText('\n')
        if keyCode in (wx.WXK_UP, wx.WXK_DOWN, wx.WXK_LEFT, wx.WXK_RIGHT):
            evt.Skip()
        if keyCode in (wx.WXK_DELETE, wx.WXK_BACK):
            self.Home()
            self.DelLineRight()
            evt.Skip()
        if keyCode in (ord('Z'), ord('Y')) and evt.ControlDown():
            evt.Skip()
        if keyCode == wx.WXK_TAB:
            lineIdx = self.GetCurrentLine()
            curIndent = self.GetLineIndentation(lineIdx)
            indent = curIndent + self.config.tabIndentLen
            if evt.ShiftDown():
                indent = curIndent - self.config.tabIndentLen*2
            self.SetLineIndentation(lineIdx, indent)
        self.show_work_mode()
        
    def move_in_edit_mode(self, evt):
        key = evt.GetKeyCode()
        if key == wx.WXK_UP: self.Home()
        elif key == wx.WXK_DOWN: self.LineEnd()
        else:
            curLine, curPos = self.GetCurLine()
            if curPos == 0 and key in (wx.WXK_LEFT, wx.WXK_BACK): pass
            elif curPos == len(curLine)-1 and key in (wx.WXK_RIGHT, wx.WXK_DELETE): pass
            else: evt.Skip()
        
    def work_in_edit_mode(self, evt):
        keyCode = evt.GetKeyCode()
        if keyCode in (wx.WXK_RETURN, wx.WXK_ESCAPE):
            if keyCode == wx.WXK_RETURN: 
                self.LineEnd()
                curLine = self.GetCurLine()[0]
                if len(curLine.strip()): evt.Skip()
            self.mode = 'View'
        elif keyCode in (wx.WXK_UP, wx.WXK_DOWN, wx.WXK_LEFT, wx.WXK_RIGHT, wx.WXK_BACK, wx.WXK_DELETE):
            self.move_in_edit_mode(evt)
        else:
            evt.Skip()
        self.show_work_mode()

    def on_key_down(self, evt):
        if self.mode == 'View':
            self.work_in_view_mode(evt)
        else:
            self.work_in_edit_mode(evt)
            
    def AddText(self, text):
        if self.mode == 'View': return
        else: super(myStc, self).AddText(text)

class myFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        self.dirname = os.getcwdu()
        self.path=''
        if os.path.isfile('./wxpdemo.ico'):
            self.ico = wx.Icon('wxpdemo.ico', wx.BITMAP_TYPE_ICO)
            self.SetIcon(self.ico)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        self.statusBar = self.CreateStatusBar()
        self.panel = myPanel(self)
        vSizer.Add(self.panel,0,wx.EXPAND)
        self.stcConfig = myStcConfiguration()
        self.stc = myStc(self, self.stcConfig)
        vSizer.Add(self.stc,1, wx.EXPAND)
        self.stc.SetFocus()

        
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
                f = codecs.open(self.path, 'r', 'utf-8-sig')
                self.stc.SetText(f.read())
                f.close()
        dlg.Destroy()
        
    def OnSave(self, event):
        if self.path == '':
            dlg = wx.FileDialog(self, "Save the file", self.dirname, "", "*.txt", wx.SAVE)
            if dlg.ShowModal() == wx.ID_OK:
                self.setFileName(dlg.GetPath())
            else:
                return             
        f=codecs.open(self.path, 'w', "utf-8-sig")
        text = self.stc.GetText()
        f.write(text)
        f.close()
        
    def onClear(self):
        self.stc.ClearAll()
        
    def onCheckBox(self, isChecked):
        if isChecked: self.stc.AddText("The checkBox Checked\n")
        else: self.stc.AddText("The checkBox Unchecked\n")

if __name__=='__main__':
    app = wx.App(False)
    myFrame(None, "Sample Editor")
    app.MainLoop()

