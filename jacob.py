"""Just Another COde Browser"""

import sublime, sublime_plugin, os

def get_position_string(tuple):
    return ':' + str(tuple[0]) + ':' + str(tuple[1])

def get_file_with_position(location):
    return location[0] + get_position_string(location[2])

class JacobGoToCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.locations = []
        region = self.view.sel()[0]
        if region.begin() == region.end(): # is a point
            region = self.view.word(region)

        symbol = self.view.substr(region)
        
        if len(symbol) == 0:
            pass
        else:
            self.navigate_to(symbol)

    def navigate_to(self, sym):
        self.locations = []
        for loc in self.where_is(sym):
            file_and_pos = get_file_with_position(loc)

            self.locations.append([os.path.basename(file_and_pos), file_and_pos]);

        if len(self.locations) == 1:
            self.go_to(self.locations[0][1])
        elif len(self.locations) > 1:
            self.view.window().show_quick_panel(self.locations, self.on_select)
        else:
            pass

    def on_select(self, index):
        self.go_to(self.locations[index][1])

    def where_is(self, sym):
        locations = []
        
        if self.view.window().project_file_name() is not None:
            locations = self.view.window().lookup_symbol_in_index(sym)
        else:
            locations = self.view.window().lookup_symbol_in_open_files(sym)

        return locations;

    def go_to(self, loc):
        self.view.window().open_file(loc, sublime.ENCODED_POSITION)
