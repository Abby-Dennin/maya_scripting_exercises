from maya import cmds

SUFFIXES = {
    "mesh": "GEO",
    "joint": "JNT",
    "camera": None
}

DEFAULT_SUFFIX = "GRP"


def rename(selection=False):
    """
    This function will rename any objects to have the correct suffix
    Args:
        selection: whether we use the current selection or not

    Returns:
        A list of all the objects we operated on
    """
    objects = cmds.ls(selection=selection, dag=True, long=True)

    # Cannot run if there is no selection and no objects
    if selection and not objects:
        raise RuntimeError("You don't have anything selected")

    objects.sort(key=len, reverse=True)

    for obj in objects:
        short_name = obj.split("|")[-1]
        children = cmds.listRelatives(obj, children=True, fullPath=True) or []

        if len(children) == 1:
            child = children[0]
            obj_type = cmds.objectType(child)
        else:
            obj_type = cmds.objectType(obj)

        suffix = SUFFIXES.get(obj_type, DEFAULT_SUFFIX)

        if not suffix:
            continue

        if obj.endswith('_'+suffix):
            continue

        new_name = "%s_%s" % (short_name, suffix)
        cmds.rename(obj, new_name)

        index = objects.index(obj)
        objects[index] = obj.replace(short_name, new_name)

    return objects
