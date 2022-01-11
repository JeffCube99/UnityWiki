===========
Scalable UI
===========

..  note::

    To understand the basics of how the UI scales please review the section on :ref:`Anchors`.

Quickstart
==========

#.  Create a new Scene
#.  Create a canvas by right clicking in the hierarchy and selecting **UI > Canvas**
#.  Select the Canvas. Inside the inspector under the Canvas Scalar component select the UI Scale Mode
    dropdown and select **Scale with Screen Size**
#.  Next in the Reference Resolution section select some common resolution like **1920 x 1080**.
#.  In the match section set the width height slider to 0.5 so that things scale proportionately depending on the
    resolution the user plays with.
#.  Next adjust the game view to the target resolution by selecting one (1920x1080) from the resolution dropdown.
#.  Next add your elements to the canvas the way you want them to appear. Choose your anchors wisely. If you want an
    object to stick to the left side of the screen make sure it's anchors are to the left and vice versa. With
    this method you can use anchor points instead of anchor rectangles since the Canvas Scaler is handling the scaling
    for you.

From this point on when you switch your game view over to other resolutions you should see your ui elements scale with
the screen size.