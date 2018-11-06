# Copy a hierarchical block's PCBnew modules relative positions.
# Select other copies of those block and apply the same relative positioning.

import HierPlace

class PathPicker(DialogUtils.ScrolledPicker):
    def __init__(self, parent, singleton=True):
        DialogUtils.ScrolledPicker.__init__(self, parent, singleton=singleton, cols=4)

        modules = [Module(m) for m in GetBoard().GetModules()]

        # Get modules in the PCB that are selected.
        # If no modules are selected, then operate on all the modules in the PCB.
        selected_modules = [m for m in modules if m.selected] or modules

        # Place the modules into groups based on hierarchy.
        groups = group_modules(selected_modules)

        for path in groups:
            self.AddSelector(path)

print('pathpicker added')

class MonkeyDialog(DialogUtils.BaseDialog):
    def __init__(self):
        super(MonkeyDialog, self).__init__("Monkey Dialog")

        self.copy = PathPicker(self, singleton=True)
        self.AddLabeled(item=self.copy,
                        label="Copy",
                        proportion=1,
                        flag=wx.EXPAND|wx.ALL,
                        border=2)

        self.paste = PathPicker(self, singleton=False)
        self.AddLabeled(item=self.paste,
                        label="Paths",
                        proportion=1,
                        flag=wx.EXPAND|wx.ALL,
                        border=2)

       # make the dialog a little taller than minimum to give the layer and net
       # lists a bit more space.
        self.IncSize(width=50, height=10)

def GetOffset(group):
  # Find the min x & y values to subtract from all components
    minx = sys.maxint 
    miny = sys.maxint 
    for mod in group:
        if minx > mod.center[0]:
            minx = mod.center[0]
            print('miny: {}'.format(minx))
        if miny > mod.center[1]:
            miny = mod.center[1]
            print('minx: {}'.format(miny))
    return minx, miny

class MonkeyPlace(ActionPlugin):
    def defaults(self):
        self.name = 'MonkeyPlace'
        self.category = 'Component Placement'
        self.description = 'Places components into clusters based on the hierarchical structure of the design.'

    def Run(self):
        PAGEWIDTH = 300000000
        SPACEX    = 50000000
        SPACEY    = 50000000
        
        print('MonkeyPlace start')

        # Place the modules into groups based on hierarchy.
        modules = [Module(m) for m in GetBoard().GetModules()]
        selected_modules = [m for m in modules if m.selected] or modules
        groups = group_modules(selected_modules)

        dlg = MonkeyDialog()
        print('MonkeyDialog created')
        res = dlg.ShowModal()
        print('ShowModal returns')

        cpath = dlg.copy.value
        cgrp = groups[cpath]
        print('copy: {}'.format(cpath))
        for mod in cgrp:
            print('pos: {}'.format(mod.center))

        x, y = GetOffset(cgrp)
        cgrp.move(-x + PAGEWIDTH, -y)

        print('paste:')
        paste = dlg.paste.value
        print(type(paste))
        print(paste)
        i = 1
        for key in paste:
            print('path: {}'.format(key))
            for mod in groups[key]:
                print('mod: {}'.format(mod.ref))
                print('pos: {}'.format(mod.center))
            x, y = GetOffset(groups[key])
            groups[key].move( (-x + PAGEWIDTH + SPACEX*i) , -y)

        # Display the hierarchically-placed modules.
        Refresh()


MonkeyPlace().register()
