bl_info = {
    "name": "Pose Tools",
    "author": "Patrick W. Crawford",
    "version": (1, 1),
    "blender": (2, 72, 0),
    "location": "Armature > Pose Library",
    "description": "Allows dynamic mixing between poses",
    "warning": "",
    "wiki_url": "https://github.com/TheDuckCow/pose-tools",
    "category": "Animation"}


import bpy


def poseAddLimited(ob, frame):
    # ob is the object/armature, should get the list of currently selected bones.
    # frame is the pre-determined frame where 
    print("getting there eventually")

# brute force copies all location/rotation/scale of all bones and returns list
def getPose(poseCurr):
    pose = []
    b = poseCurr.bones
    for i in range(len(b)):
        # generate weird UI box around curser point.... what?
        # continue if not selected!!
        if not b[i].bone.select: continue
        pose.append([ i, b[i].location.copy(), b[i].rotation_quaternion.copy(), b[i].scale.copy()])
    return pose

# generic function for mixing two poses
def mixToPose(ob, pose, value):

    def linmix(orig, new, factor):
        return orig*(1-factor)+new*factor

    # if enabled, be sure that all new poses have keyframes inserted (may happen automatically)
    autoinset = bpy.context.scene.tool_settings.use_keyframe_insert_auto

    for bone in pose:
        i = bone[0]
        p = bone
        b = ob.pose.bones[bone[0]]

        # if not selected, don't set the pose!
        if not ob.pose.bones[i].bone.select: continue

        for x in range(len(p[1])): #position
            b.location[x] =linmix(b.location[x], p[1][x], value)
        for x in range(len(p[2])): #rotation_quaternion, not EULER
            b.rotation_quaternion[x] = linmix(b.rotation_quaternion[x], p[2][x], value)
        for x in range(len(p[3])): #scale
            b.scale[x] = linmix(b.scale[x], p[3][x], value)

        # INSERT KEYFRAMES FOR ALL CHANNELS!
        if autoinset:
            bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualLocRotScale')


class mixCurrentPosePOST(bpy.types.Operator):
    """Mix the current pose and a library pose, faster for complex rigs but less interactive"""
    bl_idname = "poselib.mixcurrposepost"
    bl_label = "Mix current pose"
    bl_options = {'REGISTER', 'UNDO'}

    influence = bpy.props.FloatProperty(  
        name="Mix influence",  
        #default=bpy.context.scene.posemixinfluence*100,
        default=100,
        subtype='PERCENTAGE',  
        unit='NONE',
        min = 0,
        max = 100,
        description="influence")

    def execute(self, context):

        #get a COPY of the current pose
        ob = context.object
        prePose = getPose(ob.pose) # each element is a list of vectors, [loc, rot (quat.), scale]

        #apply the library selected pose
        bpy.ops.poselib.apply_pose(pose_index=ob.pose_library.pose_markers.active_index)

        # mix back in the poses based on the posemixinfluence property
        mixToPose(ob, prePose, 1-self.influence/100)

        return {'FINISHED'}

     # @classmethod  
     #    def poll(cls, context):  
     #        ob = context.active_object  
     #        return ob is not None and ob.mode == 'OBJECT' 


class mixCurrentPosePRE(bpy.types.Operator):
    """Mix the current pose and a library pose, using the interactive redo-last menu"""
    bl_idname = "poselib.mixcurrposepre"
    bl_label = "Mix current pose"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        #get a COPY of the current pose
        ob = context.object
        prePose = getPose(ob.pose) # each element is a list of vectors, [loc, rot (quat.), scale]

        #apply the library selected pose
        bpy.ops.poselib.apply_pose(pose_index=ob.pose_library.pose_markers.active_index)

        # mix back in the poses based on the posemixinfluence property
        mixToPose(ob, prePose, 1-context.scene.posemixinfluence/100)

        return {'FINISHED'}

     # @classmethod  
     #    def poll(cls, context):  
     #        ob = context.active_object  
     #        return ob is not None and ob.mode == 'OBJECT' 


# UI for new tools, should be appended to the existing panel
def pose_tools_panel(self, context):

    layout = self.layout
    layout.label(text="Use redo-last menu")
    layout.prop(context.scene,"redolastbool")
    if bpy.context.scene.redolastbool:
        layout.operator("poselib.mixcurrposepost", text="Apply Mixed pose")
        layout.label(text="Check F6 / the post op menu for mix factor")
    else:
        layout.operator("poselib.mixcurrposepre", text="Apply Mixed pose")
        layout.prop(context.scene, "posemixinfluence", slider=True, text="Mix Influence")

# Registration
def register():
    bpy.types.Scene.posemixinfluence = bpy.props.FloatProperty(
        name="Mix Influence",
        description="The mix factor between the original pose and the new pose",
        subtype='PERCENTAGE',
        min=0,
        max=100,
        default=100)
    bpy.types.Scene.redolastbool = bpy.props.BoolProperty(
        name="Mix Pose use redo last menu",
        description="Enable redo-last menu (F6) slider",
        default=True
        )
    
    bpy.utils.register_class(mixCurrentPosePOST)
    bpy.utils.register_class(mixCurrentPosePRE)
    bpy.types.DATA_PT_pose_library.append(pose_tools_panel)

def unregister():
    del bpy.types.Scene.posemixinfluence
    del bpy.types.Scene.redolastbool

    bpy.utils.unregister_class(mixCurrentPosePOST)
    bpy.utils.unregister_class(mixCurrentPosePRE)
    bpy.types.DATA_PT_pose_library.remove(pose_tools_panel)


if __name__ == "__main__":
    register()
