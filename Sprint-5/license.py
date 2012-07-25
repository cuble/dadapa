#! /usr/bin/env python

license_txt='''
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

'''

import os
import re

def license_a_file(f,  result):
    tmpfileName=f.name+'.tmp'
    tmpfile=open(tmpfileName, 'w')
    f.seek(0)
    lines = []
    for l in f:
        lines.append(l)
    if len(lines)==0 or not lines[0].startswith('#!'): lines.insert(0,'#! /usr/bin/env python\n')
    copyrightPresent = False
    for line in lines:
        if line.rfind('Copyright 2012 Chen Gang(fouryusteel@gmail.com)') != -1: copyrightPresent=True
    if not copyrightPresent:
        lines.insert(1,  license_txt)
        result['Succeed'].append(f.name)
    else:
        result['Ignored'].append(f.name)
    tmpfile.writelines(lines)
    tmpfile.close()
    f.close()
    cmd='mv '+tmpfileName+' '+f.name
    os.system(cmd)

def get_pattern(orgPat):
    newPattern=orgPat.replace('*','[a-z,A-Z,-,_,0-9]*')
    print newPattern
    return newPattern + '$'

if __name__=='__main__':
    import sys
    print sys.argv
    if len(sys.argv) < 2: sys.argv.append('.')
    if len(sys.argv) < 3: sys.argv.append('*.py')
    files = os.listdir(sys.argv[1])
    pattern = get_pattern(sys.argv[2])
    result = {'Succeed':[], 'Ignored':[]}
    os.chdir(sys.argv[1])
    for name in files:
        if re.match(pattern, name):
            f = open(name)
            license_a_file(f,  result)
    print result

