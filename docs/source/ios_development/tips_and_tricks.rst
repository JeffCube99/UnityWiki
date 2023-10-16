===================
iOS Tips And Tricks
===================

Configuring Game Orientation
============================

If you want to force your iOS game to remain in landscape mode or portrait mode or some combination of the two
do the following:

#.  Go to **Edit > Project Settings** and select the **Player** column.
#.  Select the **iOS** tab from the row of platforms.
#.  Expand the section titled **Resolution and Presentation**.

    *   If you want to restrict the user to a single orientation: Under the **Default Orientation** dropdown
        select the preferred Landscape / Portrait setting. Under **Allowed Orientations for Auto Rotation**
    *   If you want to allow the user to orient the game in multiple ways: Under the **Default Orientation** dropdown
        select **Auto Rotation**. Then under **Allowed Orientations for Auto Rotation** select the checkboxes next to the
        orientations you wish to enable.

Hiding the Home Indicator
=========================

.. note::

    For more information see Matthiew Oger's `blog post <https://matthieuoger.com/2018/10/unity-iphone-x-home-indicator/>`_

Sometimes you may see this pesky little white / black bar is always highlighted at the bottom of your game:

..  image:: /_images/homeindicator.jpg

This is the home Indicator bar. To make it so that it is only highlighted when the user wants to see it,
do the following:

#.  Go to **Edit > Project Settings** and select the **Player** column.
#.  Select the **iOS** tab from the row of platforms.
#.  Expand the section titled **Other Settings**.
#.  Under Defer system gestures on edges, check the **Bottom Edge** option.