#! /usr/bin/env python

class item:
    def __init__(self, parent=none):
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
}

