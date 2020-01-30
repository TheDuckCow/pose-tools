# pose-tools
This is a blender addon which hosts a few tools for improving and extending the use of the blender pose library for character animation.

The source for this code is available at [https://github.com/TheDuckCow/pose-tools](https://github.com/TheDuckCow/pose-tools), developed by [Patrick W. Crawford](http://www.theduckcow.com). **To install, [download the pose-tools.py addon](https://raw.githubusercontent.com/TheDuckCow/pose-tools/master/pose-tools.py) and install directly into blender (as a .py file, not a zip).** Currently supports blender 2.7 and 2.8 simultaneously.

[See this demo video](https://www.youtube.com/watch?v=oT7-IlVgIw0) of the addon for example uses.

Using blender 2.8? Then check out the "Tool" tab of the toolshelf in the 3D window, or underneath the pose library panel in the armature properties tab.

# Functions/operators
- **Apply Mixed Pose**: Apply a percentage mix between the current pose and the selected library pose.
- **Mixed Paste Pose**: Apply a percentage mix between the current pose and the previously copied pose
- For both tools: *Slider in the redo-last menu is for interactive changing of the pose, slider in the animation tab is for pre-setting the mix percentage but you can still use the redo-last menu slider.*

*Mixed Pose (library)*

![Mob spawner gif](/libraryPoseMix.gif)

*Mixed pose (copy/paste)*

![Mob spawner gif](/pastePoseMix.gif)


# Addon goals
- Create a tool that easily mixes library poses with current poses
- Allow easy and more direct library linking/accessing of external pose libraries
- Improve the ease and clarify of use of the library pose tools


# Miscellaneous links and references
- [Blender 2.49 pose library description](http://wiki.blender.org/index.php/Doc:2.4/Manual/Rigging/Posing/Pose_Library)
- [Blender 2.6+ pose library description, not as detailed](http://wiki.blender.org/index.php/Doc:2.6/Manual/Rigging/Posing/Pose_Library)
- [Reference pose manager tool in Maya](https://www.youtube.com/watch?v=e4MY8Ar0k7g)
- [Reference of pose commands in python](http://www.blender.org/api/blender_python_api_2_59_0/bpy.ops.pose.html)
