==============
Package Errors
==============

..  contents::
    :local:
    :depth: 1

Errors when Importing Asset Unlock: 3D Prototyping Pack
=======================================================

*   `Unity Forum Link <https://forum.unity.com/threads/what-does-this-mean-and-how-do-i-fix-it.1033156/>`_

Steps Taken To Produce Error:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#.  Create a new Unity Project from the 3D Template (On Windows 10, Using Unity Version 2020.2.25f1).
#.  Open the Unity Package Manger (**Window > Package Manager**)
#.  Import the `Asset Unlock: 3D Prototyping Pack <https://assetstore.unity.com/packages/essentials/tutorial-projects/asset-unlock-3d-prototyping-pack-183069>`_
    (The package has version 1.0).
#.  Select the **Install/Upgrade** Option when given the prompt: ``This Unity Package has Package Manager dependencies``.

At this point if we look in the console we see errors like the following:

..  error::

    GUID [d3b47ff860a51904395688d633cb1018] for asset
    'Packages/com.unity.render-pipelines.universal/Editor/ShaderGraph/Templates/BuildSurfaceDescriptionInputs.template.hlsl.meta'
    conflicts with:

    'Packages/com.unity.shadergraph/Editor/Generation/Templates/BuildSurfaceDescriptionInputs.template.hlsl.meta'
    We can't assign a new GUID because the asset is in an immutable folder. The asset will be ignored.


Steps Taken To Overcome Error:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#.  Open the Unity Package Manger (**Window > Package Manager**)
#.  In the Packages dropdown select **Packages: In Project**
#.  Select the **Universal RP** package and update the package (as of this writing updated to version 10.7.0).

Now when you select **Clear** in the Console window all of the error messages will disappear.


