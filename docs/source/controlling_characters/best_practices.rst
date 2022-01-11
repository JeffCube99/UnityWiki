==============
Best Practices
==============

Separation Input Handling and Character Commands
================================================

*   It is a good idea to separate how input is processed from game object logic.
*   An Example Setup:

    *   PlayerController.cs: A Script that handles player inputs and communicates with a separat Character Controlling Script

        *   There is no mention of rigidbody or sprites
        *   Calls methods of Character Controller like ``character_controller.move(input_2D)`` and places those
            methods inside functions like ``Update`` / ``FixedUpdate``

    *   CharacterController.cs: One of possibly many scripts for a variety of characters

        *   Controlls character state like ``is_falling``, ``facing_left``, ``on_ground``, ``crouch_speed``, etc ...
        *   Updates state inside ``Update`` / ``FixedUpdate`` where applicable
        *   Has methods player can call upon like ``Jump`` or ``Move``
