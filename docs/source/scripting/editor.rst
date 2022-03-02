================
Editor Scripting
================

Quitting The Application in Play Mode
=====================================

The ``Application.Quit()`` function only works in the built application, not when you’re testing in the Editor.
To make the game quit in the editor you must use ``EditorApplication.ExitPlaymode()``. You can use
conditional compiling to branch code based on where the code is compiled (in the editor or for a build)

..  code-block::

        #if UNITY_EDITOR
        using UnityEditor;
        #endif

        ...

        #if UNITY_EDITOR
                EditorApplication.ExitPlaymode();
        #else
                Application.Quit();
        #endif