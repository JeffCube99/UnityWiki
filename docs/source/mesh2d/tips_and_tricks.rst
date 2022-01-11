=========================
2D Meshes Tips and Tricks
=========================

Create A View Cone Obscured By Colliders
========================================

Here is the code with comments that explain it:

..  code-block:: c#

    using UnityEngine;

    public class FOV_v2 : MonoBehaviour
    {
        private int ray_count = 50; // The more rays we have the more defined our fov but it becomes an intensive process
                                   // This does not include the origin point
        private Mesh mesh;
        [SerializeField] private LayerMask layer_mask;

        public float field_of_view = 90f; // FOV range in degrees
        public float view_distance = 5f;

        // Start is called before the first frame update
        void Start()
        {
            // Assign mesh to MeshFilter
            mesh = new Mesh();
            GetComponent<MeshFilter>().mesh = mesh;

            UpdateMesh();
        }

        public Vector3 GetVectorFromAngle(float angle)
        {
            // Returns a vector from the origin of the unit circle to a point on the circle edge at the angle specified.
            // This also means the magnitude of the vector is always 1.
            // We expect an angle from 0 to 360 degrees
            float angle_radians = angle * (Mathf.PI / 180f);
            return new Vector3(Mathf.Cos(angle_radians), Mathf.Sin(angle_radians));
        }

        // Creates the mesh for our FOV
        void UpdateMesh()
        {
            float angle = field_of_view / 2; // the forward vector of the game object is pointed towards the center of the fov
            float angle_increase = field_of_view / ray_count;
            Vector3 origin = Vector3.zero;  // Because vertex coordinates are in local space, this is the coordinates of the game object.

            Vector3[] vertices = new Vector3[ray_count + 2]; // Need one vertex for the origin and the top vertex of our first ray triangle
            Vector2[] uv = new Vector2[vertices.Length];
            int[] triangles = new int[ray_count * 3]; // Eeach ray is a triangle and each triangle has 3 vertices.

            vertices[0] = origin;

            int vertex_index = 1; // start at 1 since origin is already set
            int triangle_index = 0;
            for (int i = 0; i <= ray_count; i++)
            {
                Vector3 vertex;

                //// The raycast is dealing with global coordinates but our mesh vertices are in local coordinates so we need to translate
                Vector3 global_origin = transform.position;
                Vector3 local_angle_vector = GetVectorFromAngle(angle);
                Vector3 scaled_angle_vector = Vector3.Scale(local_angle_vector, transform.lossyScale); // lossy scale ~~ world scale
                Vector3 global_angle_vector = Quaternion.Euler(0, 0, transform.eulerAngles.z) * scaled_angle_vector; // eulerAngles ~~ world space
                float global_view_distance = Vector3.Magnitude(scaled_angle_vector) * view_distance;

                //RaycastHit2D raycast_hit2d = Physics2D.Raycast(global_origin, global_angle_vector, global_view_distance, layer_mask);


                RaycastHit2D raycast_hit2d = Physics2D.Raycast(global_origin, global_angle_vector, global_view_distance, layer_mask);

                if (raycast_hit2d.collider == null)
                {
                    // We did not hit anything so place the vertex at the edge of the view distance
                    // Recall we are drawing the vertices in the local coordinates
                    vertex = origin + GetVectorFromAngle(angle) * view_distance;
                }
                else
                {
                    // We hit something so we place it on the point where it was hit
                    // We need to convert this world point to a local point however
                    vertex = transform.InverseTransformPoint(raycast_hit2d.point);
                }
                vertices[vertex_index] = vertex;

                if (i > 0)
                {
                    triangles[triangle_index + 0] = 0; // root of triangle always at origin
                    triangles[triangle_index + 1] = vertex_index - 1; // Recall vertex_index starts at 1 so when i == 1 vertex_index == 2
                    triangles[triangle_index + 2] = vertex_index;
                    triangle_index += 3; // 3 Vertices per triangle
                }

                vertex_index++;
                angle -= angle_increase; // this makes the angle go clockwise in unity this is important because our triangle indices
                                         // should be clockwise (creates front facing mesh) for the shader to work properly
                                         // (since shaders works on front facing meshes by default)
            }

            mesh.vertices = vertices;
            mesh.uv = uv;
            mesh.triangles = triangles;
        }

        // Update is called once per frame
        void Update()
        {
            UpdateMesh();
        }
    }

Next in our scene:

#.  We create an empty game object
#.  We add a mesh filter component and mesh renderer component to the game object
#.  We apply whatever material our fov is to the mesh renderer material.
#.  We add our script as a component to the game object.

Layering Meshes with Sprites
============================

Somtimes you may encounter the issue that a sprite renders on top of a mesh and vice versa and you wish to change
the order. You can achieve this by raising a mesh above a sprite physically in 3d space. Set the z offset of the mesh
so that it is closer to the camera and it will render above the default layer containing the sprite.