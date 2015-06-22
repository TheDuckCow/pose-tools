bl_info = {
    "name": "PoseTools",
    "author": "Patrick W. Crawford <support@theduckcow.com>",
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

    print("q1")

# brute force copies all location/rotation/scale of all bones and returns list
def getPose(poseCurr):
    pose = []
    b = bpy.context.selected_pose_bones
    for a in b:
        pose.append([a.location.copy(), a.rotation_quaternion.copy(), a.scale.copy()])
    return pose

# generic function for mixing two poses
def mixToPose(ob, pose, value):

    def linmix(orig, new, factor):
        return orig*(1-factor)+new*factor

    autoinsert = bpy.context.scene.tool_settings.use_keyframe_insert_auto
    bones_select = bpy.context.selected_pose_bones
    #import time
    #t0 = time.time()
    for b,p in zip(bones_select,pose):
        
        # moved from for loops to hard coded in attempt to increase speed,
        # this is the critical section!
        #for x in range(len(p[1])): #position
        #    b.location[x] =linmix(b.location[x], p[1][x], value)
        b.location[0] =linmix(b.location[0], p[0][0], value)
        b.location[1] =linmix(b.location[1], p[0][1], value)
        b.location[2] =linmix(b.location[2], p[0][2], value)
        #for x in range(len(p[2])): #rotation_quaternion, not EULER
        #    b.rotation_quaternion[x] = linmix(b.rotation_quaternion[x], p[2][x], value)
        b.rotation_quaternion[0] = linmix(b.rotation_quaternion[0], p[1][0], value)
        b.rotation_quaternion[1] = linmix(b.rotation_quaternion[1], p[1][1], value)
        b.rotation_quaternion[2] = linmix(b.rotation_quaternion[2], p[1][2], value)
        b.rotation_quaternion[3] = linmix(b.rotation_quaternion[3], p[1][3], value)
        #for x in range(len(p[3])): #scale
        #    b.scale[x] = linmix(b.scale[x], p[3][x], value)
        b.scale[0] = linmix(b.scale[0], p[2][0], value)
        b.scale[1] = linmix(b.scale[1], p[2][1], value)
        b.scale[2] = linmix(b.scale[2], p[2][2], value)
    #t1 = time.time()
    #print("timing: {x}s".format(x=t1-t0))
    if autoinsert:
        bpy.ops.anim.keyframe_insert_menu(type='BUILTIN_KSI_VisualLocRotScale')



#######
# The tool for mixing poses
class mixCurrentPose(bpy.types.Operator):
    """Mix-apply the selected library pose on to the current pose"""
    bl_idname = "poselib.mixcurrpose"
    bl_label = "Mix current pose"
    bl_options = {'REGISTER', 'UNDO'}


    influence = bpy.props.FloatProperty(  
        name="Mix influence",  
        default=100,
        subtype='PERCENTAGE',  
        unit='NONE',
        min = 0,
        max = 100,
        description="influence"
        )
    pose_index = bpy.props.IntProperty(  
        name="Pose Index",  
        default= 0, # will be passed in
        min = 0,
        description="pose index"
        )
    # make a property here for which pose, like the input one?
    # or even make it a dropdown? and have the numbers become the poseindex below for builtin

    def execute(self, context):

        #get a COPY of the current pose
        ob = context.object
        prePose = getPose(ob.pose) # each element is a list of vectors, [loc, rot (quat.), scale]
        #apply the library selected pose
        bpy.ops.poselib.apply_pose(pose_index=self.pose_index)
        #bpy.ops.poselib.apply_pose(pose_index=context.object.pose_library.pose_markers.active_index)

        # mix back in the poses based on the posemixinfluence property
        mixToPose(ob, prePose, 1-self.influence/100)

        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context):
        return (context.object and context.object.type == 'ARMATURE' and context.object.mode == 'POSE' )
   # in the above, remove the last one once I get it working in object mode too (apply to all bones..)



#######
# The tool for mixing poses
class mixedPosePaste(bpy.types.Operator):
    """Mix-paste the stored pose on to the current pose"""
    bl_idname = "poselib.mixedposepaste"
    bl_label = "Mix current pose with copied pose"
    bl_options = {'REGISTER', 'UNDO'}

    influence = bpy.props.FloatProperty(  
        name="Mix influence",  
        default=100,
        subtype='PERCENTAGE',  
        unit='NONE',
        min = 0,
        max = 100,
        description="influence"
        )

    def execute(self, context):

        #get a COPY of the current pose
        ob = context.object
        prePose = getPose(ob.pose)
        #apply the buffer selected pose
        bpy.ops.pose.paste()
        # mix back in the poses based on the posemixinfluence property
        mixToPose(ob, prePose, 1-self.influence/100)

        return {'FINISHED'}



#######
# UI for new tools next to the built in pose-lib tools, under the aramture tab of properties window
def pose_tools_panel(self, context):
    layout = self.layout
    col = layout.split(align=True)
    p = col.operator("poselib.mixcurrpose",text="Apply mixed pose")
    p.influence = context.scene.posemixinfluence
    p.pose_index = context.object.pose_library.pose_markers.active_index
    col.prop(context.scene, "posemixinfluence", slider=True, text="Mix Influence")



#######
# Panel for placing in the shift-A add object menu
class poselibToolshelf(bpy.types.Panel):
    """Extra Pose Tools"""
    bl_label = "Pose Library Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "posemode"
    bl_category = 'Tools'

    def draw(self, context):
        
        layout = self.layout
        row = layout.row()
        row.label(text="Pose Library")

        ob = context.object
        poselib = ob.pose_library

        layout.template_ID(ob, "pose_library", new="poselib.new", unlink="poselib.unlink")

        if poselib:
            # list of poses in pose library
            row = layout.row()
            row.template_list("UI_UL_list", "pose_markers", poselib, "pose_markers",
                              poselib.pose_markers, "active_index", rows=3)
            col = row.column(align=True)
            col.active = (poselib.library is None)
            col.operator("poselib.pose_add", icon='ZOOMIN', text="")
            col.operator_context = 'EXEC_DEFAULT'  # exec not invoke, so that menu doesn't need showing
            pose_marker_active = poselib.pose_markers.active

            col2 = layout.column(align=True)
            if pose_marker_active is not None:
                col.operator("poselib.pose_remove", icon='ZOOMOUT', text="")

        col2 = layout.column(align=True)
        if poselib:
            if pose_marker_active is not None:
                p = col2.operator("poselib.mixcurrpose",text="Apply mixed pose")
                p.influence = context.scene.posemixinfluence
                p.pose_index = context.object.pose_library.pose_markers.active_index
        row = col2.row(align=True)
        row.operator("pose.copy", text="Copy Pose")
        row.operator("poselib.mixedposepaste",
                    text="Mixed Paste").influence = context.scene.posemixinfluence
        col2.prop(context.scene, "posemixinfluence", slider=True, text="Mix Influence")



# Registration
def register():
    bpy.types.Scene.posemixinfluence = bpy.props.FloatProperty(
        name="Mix",
        description="The mix factor between the original pose and the new pose",
        subtype='PERCENTAGE',
        min=0,
        max=100,
        default=100)
    
    bpy.utils.register_class(mixCurrentPose)
    bpy.utils.register_class(poselibToolshelf)
    bpy.utils.register_class(mixedPosePaste)
    bpy.types.DATA_PT_pose_library.append(pose_tools_panel)

def unregister():

    bpy.utils.unregister_class(poselibToolshelf)
    bpy.utils.unregister_class(mixCurrentPose)
    bpy.utils.unregister_class(mixedPosePaste)
    bpy.types.DATA_PT_pose_library.remove(pose_tools_panel)

    del bpy.types.Scene.posemixinfluence

if __name__ == "__main__":
    register()
