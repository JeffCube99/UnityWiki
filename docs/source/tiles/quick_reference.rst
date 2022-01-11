======================
Tiling Quick Reference
======================

Basic Tile Structure
====================

*   **Sprite**: 2D graphic objects used for characters props projectiles, etc..
*   **Tile**: A square graphic. Tiles can be placed into a Tile Palette. In a scene one can select tiles from
    the palette and paint them into the scene in a grid. A tile contains a sprite. The sprite inside a tile
    can be swapped out so if you decide to change the graphic for a tile it will apply across all scenes with that tile.
*   **Tile Palette**: A way for a developer to organize tiles. Essentially a shortcut for selecting tiles to be placed
*   **AutoTile**: It appears as a single tile in a tile palette but the user can define logic so that different
    sprites are used depending on what tiles surround a given tile.

If Tiles Cover your Player
==========================

`Sorting Layers Tutorial <https://www.youtube.com/watch?v=5_BwFB-1dAo>`_

#.  Select the TileMap asset. Under the Tilemap Render Component Select the sorting layer dropdown and select
    **Add Sorting Layer...**.
#.  Inside the Sorting Layers window you can create a new layer like "Background" and place it at the top of the list.
    Things higher up on the list are drawn first and elements down the line get drawn over the earlier elements.

..  note::

    You can also sort objects within the same layer by changing the **Order in Layer** option. Here higher numbers
    are drawn on top of lower numbers.


Adding Custom Colliders To Tiles
================================

..  warning::::

    Adding a custom collider to a tile involves adjusting a sprite's custom physics shape so you will be modifying the
    sprite asset and not the tile asset.

#.  Select your tile and look in the Inspector window.
#.  Next to the sprite attribute click on the **Sprite Editor** button.
#.  Inside the sprite editor, open  the Sprite Editor Dropdown window and select **CustomSpritePhysicsShape**
#.  Click and drag over your sprite to create a bounding box. This will be your collider when you add a TileMapCollider2D
    component to your tilemap.
