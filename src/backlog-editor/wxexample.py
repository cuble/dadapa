import wx

class myFrame(wx.Frame):
    def __init__(self, parent, title):
	wx.Frame.__init__(self, parent, title=title, size=(200,100))
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.Show(True)

app = wx.App(False)
frame = myFrame(None, "Small Editor")
app.MainLoop()

