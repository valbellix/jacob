"""Just Another COde Browser
This is a simple Sublime Text 3 plugin that make code browsing easy

https://github.com/valbellix/jacob
"""
import sublime, sublime_plugin, os

def get_position_string(tuple):
    return ':' + str(tuple[0]) + ':' + str(tuple[1])

def get_file_with_position(location):
    return location[0] + get_position_string(location[2])

class Location(object):
    def __init__(self, loc):
        self.file_name = os.path.basename(loc[0])
        self.file_pos = get_file_with_position(loc)
        self.pretty_name = os.path.normpath(self.file_name)

    def to_display(self):
        return [self.file_name, self.pretty_name]

def get_location_list(locations):
    locs = []
    for i, loc in enumerate(locations):
        locs.append(loc.to_display())

    return locs;

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
        for loc in self.where_is(sym):
            self.locations.append(Location(loc))

        if len(self.locations) == 1:
            self.go_to(self.locations[0])
        elif len(self.locations) > 1:
            self.view.window().show_quick_panel(get_location_list(self.locations), self.on_select)
        else:
            pass

    def on_select(self, index):
        self.go_to(self.locations[index])

    def where_is(self, sym):
        locations = []
        
        if self.view.window().project_file_name() is not None:
            locations = self.view.window().lookup_symbol_in_index(sym)
        else:
            locations = self.view.window().lookup_symbol_in_open_files(sym)

        return locations;

    def go_to(self, loc):
        self.view.window().open_file(loc.file_pos, sublime.ENCODED_POSITION)
