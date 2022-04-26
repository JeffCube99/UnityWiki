=================================
Character Control Tips And Tricks
=================================

Character Slow When Rubbing Against Surfaces
============================================

#.  If a character is slowed down when running against surfaces then
    your best bet is to apply a frictionaless material to the character's collider.

For 2D Friction
---------------

#.  Inside your project window create a new physics material by right clicking and selecting
    **Create > 2D > Physics Material 2D**.
#.  Inside the material set bounciness to 0 and Friction to 0
#.  Inside your character's collider, set the physics material to the one you just created.

Orient Characters With The Mouse Position
=========================================

Here is a quick script that gets you the mouse's in game position along the x,y plane. It does this by projecting
a ray from the camera though the mouse and checks where the ray intersects with the plane. If no intersection occurs
it just returns a zero vector.

..  dropdown:: **MouseUtilities.cs**

    ..  code-block:: c#

        using System.Collections;
        using System.Collections.Generic;
        using UnityEngine;
        using UnityEngine.InputSystem;

        public static class MouseUtilities
        {
            // Projects a ray from the camera through the mouse cursor.
            // Gets the position of the raycast that intersects along the x and z plane.
            public static Vector3 GetMousePosition()
            {
                Ray ray = Camera.main.ScreenPointToRay(Mouse.current.position.ReadValue());
                // create a plane at 0,0,0 whose normal points to +Z:
                Plane xyPlane = new Plane(Vector3.forward, Vector3.zero);
                // Plane.Raycast stores the distance from ray.origin to the hit point in this variable:
                float distance = 0;
                // if the ray hits the plane...
                if (xyPlane.Raycast(ray, out distance))
                {
                    // get the hit point:
                    return ray.GetPoint(distance);
                }
                else
                {
                    // Return Zero if no intersection occurs
                    return Vector3.zero;
                }
            }
        }

