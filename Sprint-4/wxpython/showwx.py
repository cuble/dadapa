#! /usr/bin/env python

import wx

evtlist=[]
idlist=[]
for key in dir(wx):
  if key.startswith('EVT_'): evtlist.append(key)
  if key.startswith('ID_'): idlist.append(key)

print "Event in wx:"
for evt in evtlist: print evt
print
print
print "ID in wx:"
for id in idlist: print id

