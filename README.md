Just Another COde Browser
=========================

About
-----
Just Another COde Browser (aka jacob) is a Sublime Text 3 plugin that helps in code browsing. It works in a very naive way, leveraging on ST3 symbol indexer. It means that can browse through anything that can be indexed by ST3, and it does not need any third-parties software installed. You can obviously do this using CTags, but this is what I would like to avoid. Anyway CTags offer more than mere code browsing, and if you want something more elaborated you may want to use it, but what I really want to do is to get rid of ctags files that may be huge for very big projects.

Installation and setup
----------------------
There is really little to do to set up jacob. If you have git installed, just clone this repository into your ST3 package directory. Usually you can found it in:

* Windows: `%APPDATA%\Sublime Text 3\Packages`
* OS X: `~/Library/Application Support/Sublime Text 3/Packages`
* Linux: `~/.config/sublime-text-3/Packages`
* Portable Installation: `Sublime Text 3/Data/Packages`

and clone the repository:

    git clone https://github.com/valbellix/jacob.git

You can install this plugin manually downloading it [here](https://github.com/valbellix/jacob/archive/master.zip) and unzipping into its location (see above).

Usage
-----
Be on the symbol you need to look for, and press `ctrl+shift+period`. If your ST3 index has more than one location, a panel will show you where it is, otherwise it will navigate directly to the symbol definition. You can also use this keyboard+mouse combo: `ctrl+alt+right-click`.

Future
------
For the future, I would like to implement a "navigate back" feature...
