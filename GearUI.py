from maya import cmds
from MayaUI import BaseWindow
from GearGenerator import Gear


class GearUI(BaseWindow):
    """
    This class represents a window UI for the Gear Generator.
    """
    window_name = "GearWindow"

    def __init__(self):
        self.slider = None
        self.label = None
        self.gear = None

    def build(self):
        column = cmds.columnLayout()
        cmds.text(label="Use the slider to modify the gear")

        row = cmds.rowLayout(numberOfColumns=4)
        self.label = cmds.text(label="10")

        self.slider = cmds.intSlider(min=5, max=30, value=10, step=1, dragCommand=self.modify_gear)
        cmds.button(label="Make Gear", command=self.make_gear)
        cmds.button(label="Reset", command=self.reset)

        cmds.setParent(column)
        cmds.button(label="Close", command=self.close)

    def make_gear(self, *args):
        teeth = cmds.intSlider(self.slider, query=True, value=True)
        self.gear = Gear()

        self.gear.create_gear(teeth=teeth)

    def modify_gear(self, teeth):
        if self.gear:
            self.gear.change_teeth(teeth=teeth)

        cmds.text(self.label, edit=True, label=teeth)

    def reset(self, *args):
        self.gear = None
        cmds.intSlider(self.slider, edit=True, value=10)
        cmds.text(self.label, edit=True, label=10)