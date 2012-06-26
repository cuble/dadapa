#! /usr/bin/env python
def showline(f):
  for line in f:
    line = line.strip()
    i=line.rfind('.')
    if i > 0: 
      try:
        int(line[0:i])
        line = line[i+1:].strip()
      except ValueError:
        pass
    print line

f=open("python_study_Backlog.txt")
showline(f)

