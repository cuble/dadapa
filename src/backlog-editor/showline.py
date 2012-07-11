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

if __name__ == '__main__':
    f=open("backlog_editor_Backlog.txt")
    showline(f)

