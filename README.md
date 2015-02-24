# pose-tools
This is a blender addon which hosts a few tools for improving and extending the use of the blender pose library for character animation.

The source for this code is available at [https://github.com/TheDuckCow/pose-tools](https://github.com/TheDuckCow/pose-tools), developed by [Patrick W. Crawford](http://www.theduckcow.com)

# Functions/operators
- **Apply Mixed Pose**: *(Functional, in dev)* Apply a percentage mix between the current pose and the selected library pose. *View the mix slider in the F6/post-op menu.*
- **Limited Add Pose**: *(planned)* Create a new pose based only on position of selected bones. The default behavior is a new pose will store a keyframe for all bone channels, selected/visible or not.
- **Sync-linked Pose Lib**: *(planned)* If a pose library is linked or appended, auto or manually resync it with updated poses if the external pose library changed.
- **Visual Pose Library**: *(planned)* Functionally a tool that allows one to preview all poses at once via saved images of the active pose. Should also help generate these previews when creating new poses.

# Addon goals
- Create a tool that easily mixes library poses with current poses
- Allow easy and more direct library linking/accessing of external pose libraries
- Improve the ease and clarify of use of the library pose tools

# Todo list
- Make the pose tool faster, check for other optimizations
- Make it work properly from object mode, too (like the original tool), add in read-last menu pose index too
- Better error handling when attempting to add pose when no library created (ie gray it out!)


# Miscallaneous links and references
- [Blender 2.49 pose library description](http://wiki.blender.org/index.php/Doc:2.4/Manual/Rigging/Posing/Pose_Library)
- [Blender 2.6+ pose library description, not as detailed](http://wiki.blender.org/index.php/Doc:2.6/Manual/Rigging/Posing/Pose_Library)
- [Reference pose manager tool in Maya](https://www.youtube.com/watch?v=e4MY8Ar0k7g)
- [Reference of pose commands in python](http://www.blender.org/api/blender_python_api_2_59_0/bpy.ops.pose.html)