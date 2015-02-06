bl_info = {
    "name": "Pose Tools",
    "author": "Patrick W. Crawford",
    "version": (1, 0),
    "blender": (2, 72, 0),
    "location": "Armature > Pose Library",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Animation"}


import bpy



class mixCurrentPose(bpy.types.Operator):
    """Mix the current pose and a pose library pose"""
    bl_idname = "mesh.add_object"
    bl_label = "Mix current pose"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pritn("mixing poses!")
        return {'FINISHED'}


# Registration

def register():
    bpy.utils.register_class(mixCurrentPose)

def unregister():
    bpy.utils.unregister_class(mixCurrentPose)

if __name__ == "__main__":
    register()
