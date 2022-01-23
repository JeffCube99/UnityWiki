===============
How Audio Works
===============

Audio Sources and Listeners
===========================

*   An **Audio Listener** is a component that is attached to a game object and recieves inputs from **Audio Sources**
    in the scene. Sounds picked up by the audio listener are played through the computer's speakers.

..  image:: /images/audio_diagram.png

*   By default you can find the audio listener attached to the Main Camera in the scene.

..  image:: /images/default_audio_listener.png

2D vs 3D Audio Sources
======================

*   2D Audio Sources can be heard anywhere regardless of the distance between it and the Audio Listener.
    This makes 2D sources great for game music that should be heard regardless of the player's position.
*   3D Audio Sources are affected by the distance between it and the Audio Listener. This makes 3D sources
    useful for adding realism to sounds like car horns, campfires, and gunshots which sound quieter the further they
    are from the player.
*   You can make the audio source appear more 2D or 3D by adjusting it's Spatial Blend slider.

..  image:: /images/spatial_blend_slider.png