===============
Quick Reference
===============

Rect Transform Tool
===================

`Documentation <https://docs.unity3d.com/2021.1/Documentation/Manual/class-RectTransform.html>`_

..  note::

    A Transform in unity represents a single point. A Rect Transform represents a rectangle that a UI element can
    be placed inside. If a rect transform is inside a rect transform the child specifies how it should be positioned
    sized relative to the parent rectangle.

.. _Anchors:

Anchors
-------

`Graphical Explanation <https://docs.unity3d.com/Packages/com.unity.ugui@1.0/manual/UIBasicLayout.html#anchors>`_

What is an Anchor For
^^^^^^^^^^^^^^^^^^^^^

An Anchor is a rectangle that scales with its parent (rectangle). If an anchor is half the width of its parent
it stays half the width no matter how much parent stratches or constricts. This is useful for making scalable UI.

The UI element itself is a rectangle separate from the anchors. The 4 corners of the UI
are "Anchored" to the corners of the anchor rectangle in absolute terms.
This means that if a corner of an anchor moves 7 pixels to the left then the corner of the UI element
also moves left 7 pixels.

An easier way to think about anchors is in a 1 dimensional case:

*   When creating a UI line, if the line is ``10px`` longer than the anchor line it will always be ``10px`` longer than the
    anchor line. If the line were ``10px`` shorter it would always be 10px shorter.
*   When creating a UI line, if the line was 10px line and was was attached to an anchor point, the ui element
    would always be ``10px`` since the corners of the anchor point are not squeezed closer or further from each other.
    Still if the anchor point (with all of its corners) is translated ``10px`` to the left the ui line (with all of its
    corners) will be translated ``10px`` to the left

This behavior to some interesting scenarios:

*   **If an anchor rectangle is larger than the UI element**: If the anchor rectangle's width is reduced past the width
    of the ui element, the ui element will have 0 width and disappear. If the anchor width continues to decrease,
    even after the ui element has 0 width, the UI element will simply not render. If the parent ui element is scaled up or down,
    the UI element will appear to scale much faster.

*   **If the anchor rectangle is smaller than the UI element**: Even if the the anchor width is reduced to 0,
    the ui element will still have some width. If the parent ui element is scaled up or down,
    the UI element will appear to scale much slower.

*   **If the anchor rectangle matches the UI dimensions**: The ui element will scale the same as the anchor
    and its corners will always remain at the anchor points which are relative to the parent.


Some configurations of anchors rectangles are as follows:

*   **Anchor Rectangle**: An anchor rectangle scales with the parent. If you have a UI element with a rectangular
    anchor then its corners adjust with the anchor corners and will increase and decrease
    in size as the canvas increases and decreases in size. This is perfect for scaling elements along both dimensions.

*   **Anchor Line**: An anchor rectangle that has no width or no height. In this case a UI elemt with a anchor line
    scales with the parent along the same dimension as the line but its other dimension remains constant. This is useful
    for things like tabs and buttons which can have a variable width but remain at a fixed height (especially
    when the ui elements contain text or other elements of fixed size that do not scale vertically).

*   **Anchor Point**: An anchor point is an anchor rectangle with no width or height. While ui elements with an anchor
    point will not scale with the parent its relative position will be the same. If an anchor point and its UI element are
    3/4ths of the way down from the screen the element will remain 3/4ths of the way down.

Pivot
-----

Teh Pivot is the location around which the UI rectangle is rotated.
Its coordinates are scaled from 0 to 1 to whatever fraction of the UI
rectangle is specified.

..  note::

    If you use the to rotate the object manually (with a mouse) you will feel as if the pivot is always at the center, however
    if you only adjust the rotation values you will see the object rotating around the pivot we set.


Other attributes of the rect transform
--------------------------------------

The other attributes of the rect transform serve to place the rectangle of the UI element relative to the anchors
(see anchors above).

