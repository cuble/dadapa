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


class item:
    def __init__(self, parent=None):
        self.subitems = []
        self.content = ""
        self.done_time = "0"
        self.parent_item = parent

    def set_content(self, content):
        self.content = content
        
    def set_item_done(self):
        self.done_time = "2012-6-26,00-00-00"

    def get_item_done_time(self):
        return self.done_time

    def init_from_file(self, filename):
        pass

    def read_a_item(self, fd):
        pass

    def show_item(self):
        pass


