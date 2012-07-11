#! /usr/bin/env python

class mainWindow:
    def __init__(self):
        pass

class viewer:
    def __init__(self, gui):
        self.gui = gui
        
    def main(self):
        app=self.gui.App(False)
        mainWindow()
        app.MainLoop()
