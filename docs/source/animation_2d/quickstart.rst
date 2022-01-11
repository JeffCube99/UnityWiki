=======================
2D Animation Quickstart
=======================

Basic Animation Structure
=========================

*   **Animation Controller**: Decides what animations play at any point in time. Creates transitions between animations
    using arrows with parameters (e.g. if on idle animation and velocity param becomes > 0 we switch to the walk
    animation). Parameters can be set by script. Can also blend animations together in multidimensional space, but
    because it is 2d it will switch sharply between options.
*   **Animation** Series sprite frames over time. In the animation you can set framerate, keyframes, etc...


Setting Default Animation
=========================

Inside a animation controller, to set an animation as the first animation to play right click it and set it as the
default animation.

Creating Animations From A Single PNG of Images
===============================================

#.  Add the PNG to your assets
#.  Select the PNG. Inside the Inspector set the Sprite Mode dropdown to **Multiple**, set the Pixels Per Unit
    to some standard value (32 in my case), and set the Filter Mode dropdown to **Point (no filter)** So that your
    art is not blurred (when you are doing pixel art). Finally hit the **Apply** button at the bottom of the inspector.
#.  Next inside the inspector click the **Sprite Editor** button to open the Sprite Editor window. At the top of the
    window select **Slice > Grid By Cell Count**. From there select the number of rows and columns to divide your image
    by. When you have the settings you want, click the **Apply** button in the upper right hand side of the Sprite
    Editor Window.
#.  Next drag your PNG into a scene. You will then be prompted to specify a location where you will
    create a new animation asset. Select the location and the animation as well as an animation controller will be
    created.

    ..  note::

        When clicking on a **.anim** asset, you may not see a preview in the inspector but only
        text like::

            ``No modiel is avaliable for preview``

        We have not found a solution to this yet but you will be able to preview it once it is in the scene



Setting Up Basic Animation
==========================

`Tutorial Link <https://www.youtube.com/watch?v=hkaysu1Z-N8&t=653s>`_


Blend Tree for Multidirectional Movement
========================================

`Tutorial Link <https://www.youtube.com/watch?v=whzomFgjT50&t=183s>`_

#.  Create a new Animation
#.  Inside the Animator window, go to the Parameters tab and add 2 new float parameters by clicking the plus icon.
#.  We will name the parameters velocity_x, velocity_y
#.  Next from inside the animator window rigkt click and select **Create State > From New Blend Tree**.
#.  Double Click on the Blend Tree. Inside it we can click on the Blend Tree node. Inside the inspector window
    change the Blend Type to "2D Simple Directional".
#.  Next we will add 4 Motion Fields. Each field will belong to a specific direction by setting PosX and PosY parameters
    as follows:

    *   Up Motion == (0, 1)
    *   Down Motion == (0, -1)
    *   Left Motion == (-1, 0)
    *   Right Motion == (1, 0)

#.  Finally we can add the animations to each of the 4 mothon fields


Instant Animation Transitions
=============================

If you do not want any delay when switching between transitions do the following:

#.  Select the transtion in the Animator window and go to the inspector
#.  In the transition settings apply the following settings:

    *   Has Exit Time == False
    *   Fixed Duration == False
    *   Transition Duration == 0
    *   Transition Offset == 0


Importing A Sprite
==================

#.  Get an image you want to import like a .PNG or .JPG.
#.  Drage the image into your assets folder.
#.  You have now created a new Texture 2D. Look at the inspector and make sure the settings are correct. For pixel
    art games you should have the Pixels Per Unit consistent across your projects. Additionally make sure to set Filter
    Mode to **Point (no filter)** and Compression to **None** to prevent blurring and compression of your pixel art.

..  note::

    To turn a sprite into a tile drag it into a tile pallette

