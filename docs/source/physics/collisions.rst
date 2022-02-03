==========
Collisions
==========

..  contents::
    :local:

Colliders
=========

What is a Collider?
-------------------

*   2D or 3D components that define the shape of the game object for the purpose of physical collisions.
*   Be careful not to confuse an object's appearance with the boundaries of its collider. The collider component is
    typically invisible unless the game object is selected in the scene view.

..  image:: /_images/collider.png

When Do Colliders Collide?
--------------------------

*   Lets say we have 2 game objects. Game object A has a collider and game object B also has a collider.
    The game objects will collide with each other only if at least 1 object has a Rigidbody component
    that has the ``Is Kinematic`` parameter set to false.

..  note::

    The ``Is Trigger`` parameter inside the collider components are set to false. For more information
    on triggers see :ref:`triggers`


..  image:: /_images/collision_matrix.png

What Happens when a Colliders Collide?
--------------------------------------

*   Lets say we have 2 game objects. When the colliders of game objects A and B collide, scripts in **both** A and B
    will call the following methods:

    *   `OnCollisionEnter <https://docs.unity3d.com/ScriptReference/Collider.OnCollisionEnter.html>`_:
        Called when the colliders of A and B begin to touch each other.
    *   `OnCollisionStay <https://docs.unity3d.com/ScriptReference/Collider.OnCollisionStay.html>`_:
        Called every frame the colliders of A and B are touching each other.
    *   `OnCollisionExit <https://docs.unity3d.com/ScriptReference/Collider.OnCollisionExit.html>`_:
        Called when the colliders of A and B stop touching each other.

.. _triggers:

Triggers
========

What Is a Trigger?
------------------

*   A trigger is a collider with the parameter ``Is Trigger`` set to true.
*   A trigger can detect when another collider or trigger enters its boundaries.
*   A trigger does not collide with other colliders.

..  image:: /_images/trigger.png

When Is a Trigger Activated?
----------------------------

*   Lets say we have 2 game objects. Game Object A contains a trigger. The second Game Object
    B can activate Object A's trigger only if all of the following conditions are met:

    *   Object B has a collider or trigger.
    *   Object B's collider / trigger intersects with the boundaries of Object A's trigger.
    *   At least one object (A or B) has a Rigidbody component.


What Happens when a Trigger is Activated?
-----------------------------------------

*   Lets say we have 2 game objects. Game Object A contains a trigger and Game Object B
    has activated Game Object A's trigger. Scripts in **both** A and B will call the
    following methods:

    *   `OnTriggerEnter <https://docs.unity3d.com/ScriptReference/Collider.OnTriggerEnter.html>`_:
        Called when the colliders of A and B begin to intersect.
    *   `OnTriggerStay <https://docs.unity3d.com/ScriptReference/Collider.OnTriggerStay.html>`_:
        Called (almost) every frame the colliders of A and B are intersecting.
    *   `OnTriggerExit <https://docs.unity3d.com/ScriptReference/Collider.OnTriggerExit.html>`_:
        Called when the colliders of A and B stop intersecting.

