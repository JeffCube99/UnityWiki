=====================
Mouse Tips And Tricks
=====================

Mouse Utilities
===============

The script below provided the following functionalities:

*   Project a ray from the camera through the mouse cursor and gets the location of where the ray intersects
    a plane specified by the user.
*   Gets the position of the mouse in the world. This must be supplied a depth value since the mouse
    exists on the X, Y plane of the screen

..  dropdown:: **MouseUtilities.cs**

    ..  code-block:: c#

        using System.Collections;
        using System.Collections.Generic;
        using UnityEngine;
        using UnityEngine.InputSystem;

        public static class MouseUtilities
        {
            // Projects a ray from the camera through the mouse cursor.
            // Gets the position of the raycast that intersects with the given plane.
            public static Vector3 GetMousePositionOnPlane(Plane plane)
            {
                Ray ray = Camera.main.ScreenPointToRay(Mouse.current.position.ReadValue());
                // Plane.Raycast stores the distance from ray.origin to the hit point in this variable:
                float distance = 0;
                // if the ray hits the plane...
                if (plane.Raycast(ray, out distance))
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

            // Gets the position of the mouse in the world. Must be supplied a depth value
            // since the mouse exists only on the x,y plane of the screen.
            public static Vector3 GetMouseWorldPosition(float depth)
            {
                Vector3 mousePosition = Mouse.current.position.ReadValue();
                mousePosition.z = depth;
                return Camera.main.ScreenToWorldPoint(mousePosition);
            }
        }


