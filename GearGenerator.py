from maya import cmds


class Gear(object):
    """
    This is a Gear object that lets you create and modify a gear
    """
    def __init__(self):
        self.extrude = None
        self.constructor = None
        self.transform = None

    def create_gear(self, teeth=10, length=0.3):
        """
        This function will create a gear with the given parameters
        Args:
            teeth: the number of teeth to create
            length: the length of the teeth
        """
        spans = teeth * 2
        self.transform, self.constructor = cmds.polyPipe(subdivisionsAxis=spans)
        side_faces = range(spans * 2, spans * 3, 2)

        cmds.select(clear=True)
        for face in side_faces:
            cmds.select('%s.f[%s]' % (self.transform, face), add=True)

        self.extrude = cmds.polyExtrudeFacet(ltz=length)[0]

    def change_teeth(self, teeth=10, length=0.3):
        """
        This function will edit the number of teeth for a gear
        Args:
            teeth: the updated number of teeth
            length: the length of the teeth
        """
        spans = teeth * 2

        cmds.polyPipe(self.constructor, edit=True, subdivisionsAxis=spans)

        side_faces = range(spans * 2, spans * 3, 2)
        face_names = []

        for face in side_faces:
            face_name = 'f[%s]' % face
            face_names.append(face_name)

        cmds.setAttr('%s.inputComponents' % self.extrude,
                     len(face_names),
                     *face_names,
                     type="componentList")

        cmds.setExtrudeFacet(self.extrude, edit=True, ltz=length)
