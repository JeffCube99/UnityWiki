###########################
Scriptable Object Utilities
###########################

..  contents::
    :local:

What Are Scriptable Object Utilities For?
#########################################

Lets say you have a menu button that is tied to loading a scene. On the OnClick unity event you may drag a
reference to a SceneManager game object and have it execute a LoadMenuScene function. When you create a new scene
and drag in a new menu button you also have to add the scene manager to the scene again to get the reference.
Alternatively you could add the scene manager logic to a scriptable object. You can then drag the scriptable object
into the OnClick unity event without having to create a game object in the scene.

.. _Scene_Management_Utilities:

Scene Management Utilities
##########################

Click to download :download:`ScriptableObjectSceneManagementUtilities.unitypackage </_downloads/ScriptableObjectSceneManagementUtilities.unitypackage>`.

..  important::

    To get the example scenes working you must add both scenes to the build settings.
    Navigate to **File > Build Settings** and click on the **Add Open Scenes** button after opening each scene.

With the above you have access to a scriptable object with functions that can:

*   Load scenes by string or index.