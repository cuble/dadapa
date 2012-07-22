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

def license_a_file(f,  result=[]):
    tmpfileName=f.name+'.tmp'
    tmpfile=open(tmpfileName, 'w')
    f.seek(0)
    lines = []
    for l in f:
        lines.append(l)
    if not lines[0].startswith('#!'): lines.insert(0,'#! /usr/bin/env python')
    copyrightPresent = False
    for line in lines:
        if line.rfind('Copyright 2012 Chen Gang(fouryusteel@gmail.com)') != -1: copyrightPresent=True
    if not copyrightPresent:
        lines.insert(1,  license_txt)
        result.append("{0} add license txt successful".format(f.name))
    else:
        result.append("{0} already contain license info".format(f.name))
    tmpfile.writelines(lines)
    tmpfile.close()
    f.close()
    cmd='mv '+tmpfileName+' '+f.name
    os.system(cmd)

if __name__=='__main__':
    import sys
    if len(sys.argv) < 2: sys.argv[1] = '*.py'
    files = os.listdir('.')
    result = []
    for name in files:
        if name.match(sys.argv[1]):
            f = open(name)
            license_a_file(f,  result)
    print result

