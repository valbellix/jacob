"""Just Another COde Browser"""

import sublime, sublime_plugin

class JacobGoToCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        region = self.view.sel()[0]
        if region.begin() == region.end(): # is a point
            region = self.view.word(region)

        symbol = self.view.substr(region)
        navigate_to(self.view, symbol)

def where_is(sym, view):
    locations = []
    if len(view.window().project_file_name()) > 0:
        locations = view.window().lookup_symbol_in_index(sym)
    else:
        locations = view.window().lookup_symbol_in_open_files(sym)

    return locations;

def get_position_string(tuple):
    return ':' + str(tuple[0]) + ':' + str(tuple[1])

def get_file_with_position(location):
    return location[0] + get_position_string(location[2])

def navigate_to(view, sym):
    locations = where_is(sym, view)

    print(locations)

    if len(locations) == 1:
        view.window().open_file(get_file_with_position(locations[0]), sublime.ENCODED_POSITION)
    elif len(locations) > 1:
        # TODO
        pass
    else:
        pass
