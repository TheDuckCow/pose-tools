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


def poseAddLimited(ob, frame):
    # ob is the object/armature, should get the list of currently selected bones.
    # frame is the pre-determined frame where 
    print("getting there eventually")


# generic function for mixing two poses
def mixToPose(ob, pose, value):
    # origin and new should both be lists containing all the channels of the 
    print("working on it")

    # if enabled, be sure that all new poses have keyframes inserted (may happen automatically)
    autoinset = bpy.context.scene.tool_settings.use_keyframe_insert_auto

    for i in range(len(pose.bones)):
        p = pose.bones[i]
        #print("selected? "+str(p.bone.select))
        #print("rot: ",p.location)
        #p.location
        #p.scale
        #p.rotation_quaternion

        for x in range(len(p.rotation_quaternion)):
            #test for now, later should be an actual mix of each value
            ob.pose.bones[i].rotation_quaternion[x] = p.rotation_quaternion[x]
            print("ROT: old, new",ob.pose.bones[i].rotation_quaternion[x],p.rotation_quaternion[x])
            # can't really tell if it's old or new data being operated on...
            # yes, data on pose seems to be updated to the new pose, need a deep copy of original...
        for x in range(len(p.location)):
            ob.pose.bones[i].location[x] = p.location[x]





class mixCurrentPose(bpy.types.Operator):
    """Mix the current pose and a library pose"""
    bl_idname = "poselib.mixcurrpose"
    bl_label = "Mix current pose"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("mixing poses!")

        # check context for pose mode, armature being selected

        ob = context.object
        poselib = ob.pose_library #probably not necessary
        print("INDEX: ",poselib.pose_markers.active_index)

        #get a COPY of the current pose
        #origin = getPose(ob)
        prePose = ob.pose

        #apply the library selected pose
        bpy.ops.poselib.apply_pose(pose_index=poselib.pose_markers.active_index)

        #necessary?
        context.scene.update()

        # mix back in the poses based on the posemixinfluence property
        mixToPose(ob, prePose, 1-context.scene.posemixinfluence)

        self.report({'INFO'}, "Not fully implemented yet, working on it.")

        return {'FINISHED'}


# UI for new tools, should be appended to the existing panel
def pose_tools_panel(self, context):

    layout = self.layout
    split = layout.split()
    col = split.column()
    # perhaps better to not have it here but only after the fact (post op)
    col.prop(context.scene, "posemixinfluence", slider=True, text="Mix Influence")
    col.operator("poselib.mixcurrpose", text="Apply Mixed pose")

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
