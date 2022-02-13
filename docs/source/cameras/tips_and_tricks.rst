===============
Tips and Tricks
===============

Matching the Camera View with the Scene View
============================================

If you are working in a scene and want the camera to have the same view as the one presented in the scene view,
select the camera in the hierarchy and press **Ctrl+Shift+F**. Alternatively you can right click the camera
in the hierarchy and select **Align With View**

Fixing Jittery Cameras
======================

If your camera is following / attached to a physics object and it seems to jitter, try having the camera set its position
inside the `LateUpdate() <https://docs.unity3d.com/ScriptReference/MonoBehaviour.LateUpdate.html>`_
method which occurs after all physics calculations have occurred. Additionally if the physics object
updates its position inside a script make sure that logic lies in
`FixedUpdate() <https://docs.unity3d.com/ScriptReference/MonoBehaviour.FixedUpdate.html>`_
