from maya import cmds


class BaseWindow(object):
    """
    This class represents a base window UI in Maya.
    """
    window_name = "BaseWindow"

    def show(self):
        if cmds.window(self.window_name, query=True, exists=True):
            cmds.deleteUI(self.window_name)

        cmds.window(self.window_name)
        self.build()
        cmds.showWindow()

    def build(self):
        pass

    def reset(self, *args):
        pass

    def close(self, *args):
        cmds.deleteUI(self.window_name)