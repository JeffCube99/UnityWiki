============
Player Input
============

..  sectnum::

..  contents::
    :local:

Input System
============

`Tutorial Link <https://learn.unity.com/project/using-the-input-system-in-unity>`_

Setup and Install the Input System
----------------------------------

#.  Select **Edit > Project Settings** to open the "Project Settings" window.
#.  Next go to the sidebar and select "Player".
#.  Inside the Player window go to API Compability Level dropdown and select the ".Net 4.x." option
#.  Next select **Window > Package Manager** to open the "Package Manager" window.
#.  Inside the Package Manager window, select the dropdown menu to the right of the plus sign dropdown menu and select the
    "Packages: Unity Registry" option. Afterwards type input into the search bar. In the results sidebar click on
    Input System and in the lower right hand corner of the window click the "Install" button.
#.  Once the installation is finished you will be prompted to restart the unity editor which will disable the old input
    APIs. Click yes to continue with the restart.
#.  After the editor restarts check to see that the Input System was installed by going to **Edit > Project Settings**.
    In the sidebar click on the Input Manager where you should see that it is disabled. In the sidebar check that the
    Input System Package now exists.
#.  Next go to the Player settings in the sidebar and under the "Active Input Handling" dropdown and select the Both
    option if you want to allow for the continued use of the old input system.
#.  Finally a new input settings asset by going to **Editor > ProjectSettings**, select the Input System Package tab
    in the sidebar, and click on the "Create settings asset" button. This creates an asset called
    "InputSystem.inputsettings.asset" and saves it to your Assets/ folder.

Move A 2D Game Object
---------------------

Creating a New Input Actions Asset
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#.  Open a New Scene
#.  Add a Circle Sprite (**2D Objects > Sprite > Circle**) to the scene and call it CirclePlayer
#.  With CirclePlayer selected, in the inspector press the "Add Component" button and select "Player Input"
    from the dropdown menu.
#.  Inside the Player Input component select **Create Actions** button to create a game-ready input action asset. This
    creates a pop-up window. Inside the window create a new folder called Inputs inside your assets and click **Save**.
#.  Next inside the Player Input Component drag the newly created input actions into the **Actions** field.
#.  Double click the input actions object to open it. Take a look at the defaults assigned to it.

Scripting Player Movement
^^^^^^^^^^^^^^^^^^^^^^^^^

#.  Somewhere inside your project directory create a new C# script and then attach it to your CirclePlayer.
#.  Add a RigidBody2D to your Circle player to enable physics for your character (velocity, impulse, etc). On the
    rigidbody set **Gravity Scale** to 0.
#.  Inside your script we have the following:

    *   The full player controller script is as follows. We break down its components below.

        ..  code-block:: c#

            using System.Collections;
            using System.Collections.Generic;
            using UnityEngine;
            using UnityEngine.InputSystem;

            public class PlayerController_JS : MonoBehaviour
            {
                private Rigidbody2D rb;
                private float movementX;
                private float movementY;
                public float speed = 1;

                void Start()
                {
                    rb = GetComponent<Rigidbody2D>();
                }

                private void OnMove(InputValue movementValue)
                {
                    Vector2 movementVector = movementValue.Get<Vector2>();

                    movementX = movementVector.x;
                    movementY = movementVector.y;
                }

                void FixedUpdate()
                {
                    Vector2 movement = new Vector2(movementX, movementY);
                    rb.AddForce(movement * speed);
                }
            }

    *   To access Input System classes and methods add this line to the top of your file

        ..  code-block:: c#

            using UnityEngine.InputSystem;

    *   Set RigidBody2D as a private variaible and initialize it in the start function to the value of the
        RigidBody2D component attached to the object held by this script

        ..  code-block:: c#

                private Rigidbody2D rb;

                // Start is called before the first frame update
                void Start()
                {
                    rb = GetComponent<Rigidbody2D>();
                }

    *   Add movement and speed variables. Speed is public so we can modify it in the editor.

        ..  code-block:: c#

           private float movementX;
           private float movementY;
           public float speed = 1;

    *   Create a ``OnMove`` function that takes in a 2D movement value from the Input System and saves it to the movement
        varaibles we created.

        ..  code-block:: c#

            private void OnMove(InputValue movementValue)
            {
               Vector2 movementVector = movementValue.Get<Vector2>();

                 movementX = movementVector.x;
                 movementY = movementVector.y;
            }

    *   Call this function within the FixedUpdate function since FixedUpdate is for physics actions. Additionally
        add a line that adds a force to the object in the direction given by the movement varaibles we update in
        the ``OnMove`` function.

        ..  code-block:: c#

            void FixedUpdate()
            {
                Vector3 movement = new Vector3(movementX, 0.0f, movementY);
                rb.AddForce(movement * speed);
            }

#.  Save and exit the script.
#.  Press play and use the arrow keys to move your character in the scene view.

Scripting Movement From Scratch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Link to Tutorial <https://learn.unity.com/tutorial/customizing-new-input-actions>`_

When you want to use your own custom InputAction game object do the following:

#.  Right click inside of the project window and select **Create > Input Actions**
#.  Double click the new InpuActions object in the project window to open up the Input Actions window.
#.  Inside the Input Actions window click the plus button next to Action Maps to create a new Action Map.
    Actions Maps categorize and group together actions. Lets name this action map Player.
#.  Under the Actions column rename the newly created action. For now we will call this action "Movement".
#.  With the "Movement" action selected, looking at the rightmost Properties column we want to set the Action Type dropdown
    to value since movement should be continuous. Next we set the control type for movement to be Vector 2 since
    for this example we will be moving in 2 dimensions.
#.  When we expand the Move action we see a section that says ``<No Binding>``. We will delete this and then we will
    click the plus button to the right of the Move action and select Add 2D Vector Composite. We will call this composite
    "WASD".
#.  Inside "WASD" we see 4 bindings (Up, Down, Left, Right). We can assign each binding to a different key. After selecting
    the Up binding, under the Properties section we select the Path dropdown and search for the W key. We then do the
    same for each of the other directions. To also support the arrow keys we create 4 new bindings
    (by duplicating the same bindings) for each direction.
    We can specify the direction of the new bindings by selecting the Composite Part section under the Properties page.
#.  To make sure our work is automatically saved, we click the Auto-Save button in the upper right hand portion of the
    input action window.
#.  Next select your custom input action from within the project window and in the inspector window click the checkbox
    **Generate C# Class** and select the Apply button. This provides you a reference class that enables you to streamline
    commands from other custom scripts you write. Note that this file is named Player_Controller_JS.cs
#.  Now we create another C# script to move our player. We call it SquarePlayerController_JS.
#.  Next lets navigate back to our 2D scene. Create a Square Sprite (**Right Click > 2D Objects > Sprite > Square**)
    and assign to it a RigidBody2D and set its gravity scale to 0. Afterwards add a Player Input component and select
    your custom input component for the Actions argument. Finally add the new SquarePlayerController_JS script to the object.
#.  Now the contents of SquarePlayerController_JS can take multiple forms.

    *   The simplest is the following:

        ..  code-block:: c#

            using System.Collections;
            using System.Collections.Generic;
            using UnityEngine;
            using UnityEngine.InputSystem;

            public class SquarePlayerController_JS : MonoBehaviour
            {
                private Rigidbody2D rb;
                private float movementX;
                private float movementY;
                public float speed = 1;

                void Start()
                {
                    rb = GetComponent<Rigidbody2D>();
                }

                private void OnMovement(InputValue movementValue)
                {
                    Vector2 movementVector = movementValue.Get<Vector2>();

                    movementX = movementVector.x;
                    movementY = movementVector.y;
                }

                void FixedUpdate()
                {
                    Vector2 movement = new Vector2(movementX, movementY);
                    rb.AddForce(movement * speed);
                }
            }

        *   In this form we see that that main thing to consider is the ``OnMovement`` function. While there
            is no reference to our custom input component class ``Player_Controller_JS.cs`` looking into that class
            we see that this class has a call to instance.OnMovement which our class somehow gains access to
            probably since this object has player input and reference to our custom input action class.

    *   A script that lends the user more controll and is much clearer in intentions is the following:

        ..  code-block::

            using System.Collections;
            using System.Collections.Generic;
            using UnityEngine;
            using UnityEngine.InputSystem;

            public class SquarePlayerController_JS : MonoBehaviour
            {
                Player_Controls_JS controls;
                Vector2 move;
                public float speed = 10;

                // Called before Start
                void Awake()
                {
                    controls = new Player_Controls_JS();
                    controls.Player.Movement.performed += ctx => move = ctx.ReadValue<Vector2>();
                    controls.Player.Movement.canceled += ctx => move = Vector2.zero;
                }

                private void OnEnable()
                {
                    controls.Player.Enable();
                }

                private void OnDisable()
                {
                    controls.Player.Disable();
                }

                void FixedUpdate()
                {
                    Vector2 movement = new Vector2(move.x, move.y) * speed * Time.deltaTime;
                    transform.Translate(movement, Space.World);
                }
            }

        *   This class references our auto generated Player_Controls_JS script directly.
        *   Additionally we can direct functions to be called by adding them to the action context. Additionally
            the context matches the same naming convention we establish in the Input Actions window: ``controls.Player.Movement.performed``
            and ``controls.Player.Movement.canceled`` reference that we have an Action Map called Player and a
            Movement action belonging to that Player action map.

        ..  note::

            The ``OnEnable`` and ``OnDisable`` Logic is crucial to make sure the input system is enabled.
            The input system is also modular so in the future you
            could implement the ability to swap between different input assets or control schemes in the future.



