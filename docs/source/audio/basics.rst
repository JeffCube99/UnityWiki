============
Audio Basics
============

..  contents::
    :local:

Adding Music to a Scene
=======================

#.  Create an empty game object.
#.  Add an **Audio Source** component.
#.  Add your music file to the **AudioClip** parameter of the Audio Source Component.
#.  Make sure the **Play On Awake** option of the Audio Souce component is selected. This way the music begins to play
    when the game starts to run.
#.  Make sure the Spatial Blend slider is set to 2D. This way the music can be heard from anywhere in the scene.

..  image:: /images/adding_music_to_scene.png


Adding 3D Sounds to a Scene
===========================

#.  Create an empty game object.
#.  Add an **Audio Source** component.
#.  Add your sound file to the **AudioClip** parameter of the Audio Source Component.
#.  If you want the sound to play when the game starts to run, Make sure the **Play On Awake** option of the Audio Souce
    component is selected.
#.  Make sure the Spatial Blend slider is set to 3D. This way the sound is affected by the distance between the
    Audio Listener (positioned on the camera by default) and the Audio Source.

..  image:: /images/adding_3d_sound_to_scene.png


Mute Audio in Game View
=======================

In the **Game View**, click the **Mute Audio** Button

..  image:: /images/mute_game_view_audio.png
