=======================
2D Mesh Quick Reference
=======================

..  sectnum::

..  contents::
    :local:

Mesh Basics
===========

`Tutorial <https://www.youtube.com/watch?v=11c9rWRotJ8>`_

How to Render a Mesh On Screen
------------------------------

#.  Create a new scene
#.  Add an empty game object
#.  Add a **Mesh Filter** Component and a **Mesh Renderer** Copmponent
#.  Inside the MeshFilter select the builtin **Quad** mesh
#.  Inside the Mesh Render apply any material

Things to Notice

*   You need both a Mesh (Mesh Filter) and a Mesh Render to have a mesh displayed in a scene.
*   The Mesh is what defined the shape that is rendered. It is made up of polygons (triangles). The Quad mesh is a square
    and required 2 triangles to make a square shape. you can see this inside the scene view if you click on the dropdown
    and select the **Wireframe** option.
*   The Mesh Renderer material contains the texture data that is to be applied to that mesh.

How to Create a Mesh in a Script
--------------------------------

There are 3 fields you must set when creating a Mesh in code:

*   **mesh.vertices (Vector3[])**: Array of Vector3 that represent each vertex of our mesh
*   **mesh.uv (Vector2[])**: Array of Vector2 that outlines the parts of the texture that match with a certain vertex.
    Textures are displayed in a square with normalized coordinates. That means that the lower left corner of a texture
    corresponds to a uv of (0,0) and the upper right corner of a texture corresponds to a uv of (1, 1).
*   **mesh.triangles (int[])**: Array of integers that define the vertex indices. 3 make up a polygon. Every 3
    indices creates a triangle.

    ..  note::

        Each polygon has a front face and a back face. Some shaders do not color the back face of a polygon.
        A polygon is front facing if the vertices are clockwise so always set the indices in a clockwise order.::

                                    1---2
                                    |  /
            vertex num ==           | /
                                    |/
                                    0

            triangles[0] = 0;                       1---2
            triangles[1] = 1;                       |  /
            triangles[2] = 2;   clockwise ==        | /
                                                    |/
                                                    0

            triangles[0] = 0;                       2---1
            triangles[1] = 2;                       |  /
            triangles[2] = 1;  counter clockwise == | /
                                                    |/
                                                    0

Below is a script with comments explaining the code:

..  code-block:: c#

    using System.Collections;
    using System.Collections.Generic;
    using UnityEngine;

    public class MeshTest : MonoBehaviour
    {
        // Start is called before the first frame update
        void Start()
        {
            Mesh mesh = new Mesh();

            // We are making a square. this requires 4 vertices and 2 triangles
            Vector3[] vertices = new Vector3[4];
            Vector2[] uv = new Vector2[4];
            int[] triangles = new int[6]; // We need to make 2 triangles and each triangle needs 3 points


            // Setting the coordinates of the vertices in the x, y plane
            vertices[0] = new Vector3(0, 0);
            vertices[1] = new Vector3(0, 100);
            vertices[2] = new Vector3(100, 100);
            vertices[3] = new Vector3(100, 0);

            // Textures are squares with normalized coordinates. (0,0) is the bottom left and (1,1) is the top right.
            uv[0] = new Vector2(0, 0);
            uv[1] = new Vector2(0, 1);
            uv[2] = new Vector2(1, 1);
            uv[3] = new Vector2(1, 0);

            // Setting the vertices of the first triangle (in clockwise order)
            triangles[0] = 0;
            triangles[1] = 1;
            triangles[2] = 2;

            // Setting the vertices of the second triangle (in clockwise order)
            triangles[3] = 0;
            triangles[4] = 2;
            triangles[5] = 3;

            mesh.vertices = vertices;   // Array of Vector3 that represent each vertex of our mesh
            mesh.uv = uv;               // Array of Vector2 that outlines the parts of the texture that match with a certain vertex
            mesh.triangles = triangles; // Array of integers that define the vertex indices.

            // We expect the game object to have a mesh filter component.
            GetComponent<MeshFilter>().mesh = mesh;
        }
    }

To use this script we:

#.  Create a new scene
#.  Add an empty game object to the scene
#.  Add your script to the game object
#.  Add a mesh filter component to the game object
#.  Add a mesh renderer component to the game object
#.  Add a material to the mesh renderer.

..  note::

    If you have a texture and you want to quickly convert it into a material, create a new material
    (**Create > Material**), set the Shader Dropdown to **Unlit/Texture**, and drag your texture into
    the Texture field.

Important Notes About Meshes
============================

*   The coordinates of the vertices are local coordinates not world coordinates.
*   Textures are organized into a square with normalized coordinates. That means that the lower left corner of a texture
    corresponds to a uv of (0,0) and the upper left corner of a texture corresponds to a uv of (1, 1).
*   If you make any changes to vertices, triangles, or uvs, you need to update the mesh variable. e.g.: ::

        mesh.vertices = updated vertices;


