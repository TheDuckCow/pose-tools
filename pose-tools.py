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

# generic function for mixing two poses
def mixPoses(origin,new, value):
    # origin and new should both be lists containing all the channels of the 
    print("working on it")

    # if enabled, be sure that all new poses have keyframes inserted (may happen automatically)
    autoinset = bpy.context.scene.tool_settings.use_keyframe_insert_auto



class mixCurrentPose(bpy.types.Operator):
    """Mix the current pose and a library pose"""
    bl_idname = "poselib.mixcurrpose"
    bl_label = "Mix current pose"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("mixing poses!")

        # check context for pose mode, armature being selected

        ob = context.object
        poselib = ob.pose_library
        print("INDEX: ",poselib.pose_markers.active_index)

        #get a COPY of the current pose

        #apply the library selected pose
        bpy.ops.poselib.apply_pose(pose_index=poselib.pose_markers.active_index)

        # mix back in the poses based on the posemixinfluence property
        #mixPoses(origin,new) #perhaps only needs to take in new pose and assume new pose applied

        self.report({'INFO'}, "Not fully implemented yet, working on it.")

        return {'FINISHED'}


# UI for new tools, should be appended to the existing panel
def pose_tools_panel(self, context):

    layout = self.layout
    split = layout.split()
    col = split.column()
    col.prop(context.scene, "posemixinfluence", slider=True, text="Mix Influence")
    col.operator("poselib.mixcurrpose", text="Set new pose")

# Registration
def register():
    bpy.utils.register_class(mixCurrentPose)
    bpy.types.DATA_PT_pose_library.append(pose_tools_panel)

    bpy.types.Scene.posemixinfluence = bpy.props.FloatProperty(
        name="Mix Influence",
        description="The mix factor between the original pose and the new pose",
        min=0,
        max=1,
        default=1)

def unregister():
    bpy.utils.unregister_class(mixCurrentPose)
    bpy.types.DATA_PT_pose_library.remove(pose_tools_panel)
    del bpy.types.Scene.posemixinfluence

if __name__ == "__main__":
    register()
