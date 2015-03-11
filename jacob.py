"""Just Another COde Browser
This is a simple Sublime Text 3 plugin that make code browsing easy.

Zero configuration, just wait for the index to be built and browse!

https://github.com/valbellix/jacob
"""
import sublime, sublime_plugin, os

def get_position_string(tuple):
    '''It returns an encoded line:column string'''
    return ':' + str(tuple[0]) + ':' + str(tuple[1])

def get_line_suffix(tuple):
    '''It extracts the line information and 
    creates a pretty suffix to append to a file name'''
    return ':' + str(tuple[0])

def get_file_with_position(location):
    '''It returns a filename with position encoded as line:column'''
    return location[0] + get_position_string(location[2])

class Location(object):
    '''This class manages the elements to display in the panel
    when a symbol is defined in multiple locations'''
    def __init__(self, loc):
        line = get_line_suffix(loc[2])
        self.file_name = os.path.basename(loc[0]) + line
        self.file_pos = get_file_with_position(loc)
        self.pretty_name = os.path.normpath(loc[0]) + line

    def to_display(self):
        '''It returns a list suitable for show_quick_panel list element'''
        return [self.file_name, self.pretty_name]

def get_location_list(locations):
    '''It builds a list suitable for show_quick_panel'''
    locs = []
    for i, loc in enumerate(locations):
        locs.append(loc.to_display())

    return locs;

class JacobGoToCommand(sublime_plugin.TextCommand):
    '''This is the place where the magic happens...'''
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
        '''This method brings you directly to the definition
        it is unique across the project or opened file set, 
        otherwise it will open a panel where you have to choose
        where to go'''
        for loc in self.where_is(sym):
            self.locations.append(Location(loc))

        if len(self.locations) == 1:
            self.go_to(self.locations[0])
        elif len(self.locations) > 1:
            self.view.window().show_quick_panel(get_location_list(self.locations), self.on_select)
        else:
            pass

    def on_select(self, index):
        '''It is the callback of show_quick_panel'''
        self.go_to(self.locations[index])

    def where_is(self, sym):
        '''This method will look for the symbol in the project
        or among the set of opened files'''
        locations = []
        
        if self.view.window().project_file_name() is not None:
            locations = self.view.window().lookup_symbol_in_index(sym)
        else:
            locations = self.view.window().lookup_symbol_in_open_files(sym)

        return locations;

    def go_to(self, loc):
        '''This is the method that will bring you to the 
        point where is defined the symbol you are looking for'''
        self.view.window().open_file(loc.file_pos, sublime.ENCODED_POSITION)
