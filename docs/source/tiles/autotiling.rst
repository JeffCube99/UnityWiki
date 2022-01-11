========
AutoTile
========

`Tutorial <https://www.youtube.com/watch?v=nfjAznD_MaU>`_

AutoTile Setup
==============

#.  Open the package manager by selecting **Window > Package Manager**
#.  Inside the Package Manager choose **Unity Registry** from the Packages dropdown and then search for "2D Tilemap Extras".
#.  Click the **Install** button in the lower right hand corner of the window.
#.  You should now see the 2D Tilemap Extras folder in side the Project window under the Packages folder.

Configuring AutoTile Rules
==========================

#.  Inside a folder right click and select **Create > 2D > Tiles > Rule Tile**.
#.  Inside the inspector drag and drop an example sprite into the Sprite window to give this asset an image to go off of
    and will aslo be the first sprite you create a rule for.
#.  Next create a new Tiling Rules entry. By default the first entry you make contains the sprite you dragged into it.
    You will see a grid next to the sprite and the rules are pretty straightforward and are as follows:

    *   **Single Click -> Green Arrow**: There should be tiles here next to this tile for it to be present.
    *   **Double Click -> Red X**: There should be no tile here if this tile is present.
    *   **Blank Space**: Any tile / No tile can go here.

    Do this for all of your tiles. Here are a few examples

    *   Top Left Corner::

            [ ][X][ ]
            [X][ ][>]
            [ ][>][ ]

    *   Left side::

            [ ][>][ ]
            [X][ ][>]
            [ ][>][ ]

    *   Floor Tile That is chipped on the lower right side::

            [ ][>][ ]
            [>][ ][>]
            [ ][>][X]

#.  Next open up the tile pallette by selecting **Window > 2D > Tile Pallette**. Inside the tile pallette we can
    add our Rule tile by dragging it from the Project window into the Tile Pallette window.

Placing Tiles In A Scene
========================

#.  Create a new scene and inside the hierarchy right click and select **2D > Tilemap > Rectangular**
#.  Next open the tile pallette by selecting **Window > 2D Object > Tile Pallette**.
#.  Inside the tile pallette select your rule tile you created in the previous step. Then at the top of the tile pallette
    select the brush tool.
#.  With your tile map in the scene view selected you can now paint your tiles to the scene.

Tile Collision
==============

`Tile Collision Tutorial <https://www.youtube.com/watch?v=VDdKv0DgY5I>`_

To create collisions with things like walls / ceilings you can create a separate tilemap and assign it to collide with
your player.

#.  Create a new tile map by going inside the hierarchy and selecting **2D Object > Tilemap > Rectangular**.
#.  Place down your wall tiles on this map
#.  Select the Tilemap and in the inspector add the **Tilemap Collider 2D** component which will automatically add
    a 2d box collider to all of your tiles.