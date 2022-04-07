#####
Audio
#####

.. _Managing_Audio_With_Scriptable_Objects:

Managing Audio With Scriptable Objects
######################################

High level overview:

*   Using scriptable objects you can use events to play 2D+3D SFX and music without having
    audio sources start in your scene. Also music will persist between scenes.
*   Using scriptable objects you can use UI sliders + events to interface with the audio mixer.
    This makes setting the volume across multiple groups easy.

Example
*******

Description of Major Components:

*   AudioMixerManager.cs

    *   A scriptable object
    *   Has reference to a audio mixer
    *   Use sliders + events to set audio levels + set slider values on start.

*   AudioSourceManager.cs

    *   A scriptable object
    *   Has a pool of 2D audio sources it attaches to the audio listener in a scene
    *   Uses object pooling to access 3D audio sources
    *   For Music audio it uses a prefab audio source that is a singleton + is not destroyed on load

*   SoundAsset.cs

    *   A Scriptable object
    *   Has a reference to an audio clip, audio mixer group, volume level, and AudioSourceManager
    *   When it plays audio it asks for sources from the AudioSourceManager and applies the above
        settings to the source before playing it.

Click to download :download:`ScriptableObjectAudioManagementExample.unitypackage </_downloads/ScriptableObjectAudioManagementExample.unitypackage>`.

..  warning::

    This example also includes the following packages:

    *   ScriptableObjectPoolingExample.unitypackage (See :ref:`Object_Pooling_Scriptable_Objects`)
    *   ScriptableObjectSceneManagementUtilities.unitypackage (See :ref:`Scene_Management_Utilities`)

    So when you are importing, take care to make sure things are not overwritten / duplicated if you have downloaded
    those packages in the past.

