import wx
import os

class myFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,600))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.CreateStatusBar()
        
        filemenu = wx.Menu()

        menuOpen = filemenu.Append(wx.ID_OPEN, "&Open", " Open a file")
	self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)
        self.Show(True)
        
    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "A small text editor", "About Sample Editor", wx.OK)
        dlg.ShowModal()
	dlg.Destroy()

    def OnExit(self, event):
        self.Close(True)

    def OnOpen(self,e):
        """ Open a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
	    self.filename = dlg.GetFilename()
	    self.dirname = dlg.GetDirectory()
	    f = open(os.path.join(self.dirname, self.filename), 'r')
	    self.control.SetValue(f.read())
	    f.close()
        dlg.Destroy()

app = wx.App(False)
frame = myFrame(None, "Sample Editor")
app.MainLoop()

