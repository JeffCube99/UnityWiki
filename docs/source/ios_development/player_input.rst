################
iOS Player Input
################

..  contents::
    :local:

Simulate Player Input With Mouse
################################

If you don't have access to a phone you can simulate a touch screen inside the Unity Editor with the mouse by going to
**Window > Analysis > Input Debugger**. This will bring up an Input Debug window. Inside window click the **Options** dropdown and select
**Simulate Touch Input from Mouse or Pen**. Now clicking the mouse in play mode will simulate touching the screen.
Unfortunately you cannot simulate multi touch using the mouse so to do that you must use :ref:`Unity_Remote` or build
the project to your phone (:ref:`Unity_iOS_Build`).

.. _Touch_Utilities:

Touch Utilities
###############

The script below provided the following functionalities:

*   Project a ray from the camera through the touch point and gets the location of where the ray intersects
    a plane specified by the user.

..  dropdown:: **TouchUtilities.cs**

    ..  code-block:: c#

        using System.Collections;
        using System.Collections.Generic;
        using UnityEngine;

        public static class TouchUtilities
        {
            public static Vector3 GetTouchPositionOnPlane(Plane plane, Vector2 touchPosition)
            {
                Ray ray = Camera.main.ScreenPointToRay(touchPosition);
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
        }


Get Touch Data Using Input Action Assets
########################################

Using Unity's Input System (See: :ref:`Unity_Input_System`), we can listen into touch events that allow
us to detect when a touch begins and ends while also reading data from the input system to determine more
information about the touche's starting point, ending point, delta, etc.

Key Takeaways:
**************

*   We create an Action Map containing Touch Actions.
*   We connect Touch actions to Input Events (See :ref:`Scriptable_Object_Input_Events_V2`) that trigger when touches
    begin and end (when the finger is placed on the screen, and released from the screen)
*   **TouchVisualizer.cs** connects activates / deactivates the touch visualization assets when detecting the touches
    happening. Additionally it reads in the `TouchState <https://docs.unity3d.com/Packages/com.unity.inputsystem@1.0/api/UnityEngine.InputSystem.LowLevel.TouchState.html#fields>`_
    property (``touchAction.ReadValue<TouchState>()``) from a Touch Action to get current and start position data.

..  dropdown:: **TouchVisualizer.cs**

    ..  code-block:: c#

        using System.Collections;
        using System.Collections.Generic;
        using UnityEngine;
        using TMPro;
        using UnityEngine.InputSystem;
        using UnityEngine.InputSystem.LowLevel;

        public class TouchVisualizer : MonoBehaviour
        {
            [SerializeField] private TextMeshProUGUI startPositionText;
            [SerializeField] private TextMeshProUGUI currentPositionText;
            [SerializeField] private InputActionReference touchActionReference;
            [SerializeField] private GameObject startSprite;
            [SerializeField] private GameObject endSprite;
            [SerializeField] private GameObject lineRendererObject;

            private LineRenderer lineRenderer;
            private InputAction touchAction;
            private bool isTouching;
            private Plane xyPlane;

            void Start()
            {
                // Save the action to a variable so we don't have to keep referring to the '.action' property
                touchAction = touchActionReference.action;
                // We need to make sure the touch action is enabled otherwise the input will not be processed.
                touchAction.Enable();

                xyPlane = new Plane(Vector3.forward, Vector3.zero);
                lineRenderer = lineRendererObject.GetComponent<LineRenderer>();

                // We assume the user is not touching the screen at the start
                OnTouchEnd();
            }

            public void OnTouchStart()
            {
                isTouching = true;
                EnableVisuals();
            }

            public void OnTouchEnd()
            {
                isTouching = false;
                DisableVisuals();
            }

            private void EnableVisuals()
            {
                startSprite.SetActive(true);
                endSprite.SetActive(true);
                lineRendererObject.SetActive(true);
            }

            private void DisableVisuals()
            {
                startPositionText.text = "Touch The Screen";
                currentPositionText.text = "Touch The Screen";
                startSprite.SetActive(false);
                endSprite.SetActive(false);
                lineRendererObject.SetActive(false);
            }

            void Update()
            {
                if (isTouching)
                {
                    // Gather touch data from touch action
                    TouchState touchState = touchAction.ReadValue<TouchState>();
                    Vector2 startPosition = touchState.position;
                    Vector2 currentPosition = touchState.startPosition;

                    // Set text
                    startPositionText.text = $"Start Position: {startPosition}";
                    currentPositionText.text = $"Current Position: {currentPosition}";

                    // Update positions of sprites and lines
                    Vector3 startWorldPosition = TouchUtilities.GetTouchPositionOnPlane(xyPlane, startPosition);
                    Vector3 currentWorldPosition = TouchUtilities.GetTouchPositionOnPlane(xyPlane, currentPosition);
                    startSprite.transform.position = startWorldPosition;
                    endSprite.transform.position = currentWorldPosition;
                    lineRenderer.SetPosition(0, startWorldPosition);
                    lineRenderer.SetPosition(1, currentWorldPosition);
                }
            }
        }

Example
*******

..  important::

    This example requires the following packages to be installed:

    *   TextMeshPro Essentials
    *   Input System

..  warning::

    This example also includes the following packages:

    *   ScriptableObjectInputSystemV2Example.unitypackage (See :ref:`Scriptable_Object_Input_Events_V2`)

..  note::

    This example also includes utilities for processing touch inputs as seen in :ref:`Touch_Utilities`

Click to download :download:`InputActionTouchDataExample.unitypackage </_downloads/InputActionTouchDataExample.unitypackage>`.

Get Touch Data Using EnhancedTouch
##################################

Unity's Input System (See: :ref:`Unity_Input_System`) comes with support for a class called
`EnhancedTouch.Touch <https://docs.unity3d.com/Packages/com.unity.inputsystem@1.0/manual/Touch.html#enhancedtouchtouch-class>`_.
With this class we can detect how many fingers are touching the screen as well as the touch information associated with each
finger.

Key Takeaways:
**************

*   We enable Enhanced Touch features by calling ``EnhancedTouchSupport.Enable();``
*   We connect Touch events to functions when enabling the TouchVisualizer (``Touch.onFingerDown += OnFingerDown;``).
*   We store a reference to a target "`Finger <https://docs.unity3d.com/Packages/com.unity.inputsystem@1.0/api/UnityEngine.InputSystem.EnhancedTouch.Finger.html>`_"
    and then extract touch information from the finger (``Touch touch = currentFinger.currentTouch;``) to get current and start
    position data.

..  dropdown:: **TouchVisualizer.cs**

    ..  code-block:: c#

        using System.Collections;
        using System.Collections.Generic;
        using UnityEngine;
        using TMPro;
        using UnityEngine.InputSystem.EnhancedTouch;
        using Touch = UnityEngine.InputSystem.EnhancedTouch.Touch;

        public class TouchVisualizer : MonoBehaviour
        {
            [SerializeField] private TextMeshProUGUI startPositionText;
            [SerializeField] private TextMeshProUGUI currentPositionText;
            [SerializeField] private GameObject startSprite;
            [SerializeField] private GameObject endSprite;
            [SerializeField] private GameObject lineRendererObject;
            [SerializeField] private int fingerIndex;

            private LineRenderer lineRenderer;
            private bool isTouching;
            private Plane xyPlane;
            private Finger currentFinger;

            private void Awake()
            {
                // We need to call EnhancedTouchSupport.Enable() to use the EnhancedTouch.Touch API.
                EnhancedTouchSupport.Enable();
            }

            void Start()
            {
                xyPlane = new Plane(Vector3.forward, Vector3.zero);
                lineRenderer = lineRendererObject.GetComponent<LineRenderer>();

                // We assume the user is not touching the screen at the start
                isTouching = false;
                DisableVisuals();
            }

            // Connect Touch events to functions inside this class
            private void OnEnable()
            {
                Touch.onFingerDown += OnFingerDown;
                Touch.onFingerUp += OnFingerUp;
            }

            // Remove links to Touch events when this class is disabled
            private void OnDisable()
            {
                Touch.onFingerDown -= OnFingerDown;
                Touch.onFingerUp -= OnFingerUp;
            }

            public void OnFingerDown(Finger finger)
            {
                if (finger.index == fingerIndex)
                {
                    currentFinger = finger;
                    isTouching = true;
                    EnableVisuals();
                }
            }

            public void OnFingerUp(Finger finger)
            {
                if (finger.index == fingerIndex)
                {
                    isTouching = false;
                    DisableVisuals();
                }
            }

            private void EnableVisuals()
            {
                startSprite.SetActive(true);
                endSprite.SetActive(true);
                lineRendererObject.SetActive(true);
            }

            private void DisableVisuals()
            {
                startPositionText.text = "Touch The Screen";
                currentPositionText.text = "Touch The Screen";
                startSprite.SetActive(false);
                endSprite.SetActive(false);
                lineRendererObject.SetActive(false);
            }

            void Update()
            {
                if (isTouching)
                {
                    // Gather touch data from the current finger
                    Touch touch = currentFinger.currentTouch;
                    Vector2 startPosition = touch.startScreenPosition;
                    Vector2 currentPosition = touch.screenPosition;

                    // Set text
                    startPositionText.text = $"Start Position: {startPosition}";
                    currentPositionText.text = $"Current Position: {currentPosition}";

                    // Update positions of sprites and lines
                    Vector3 startWorldPosition = TouchUtilities.GetTouchPositionOnPlane(xyPlane, startPosition);
                    Vector3 currentWorldPosition = TouchUtilities.GetTouchPositionOnPlane(xyPlane, currentPosition);
                    startSprite.transform.position = startWorldPosition;
                    endSprite.transform.position = currentWorldPosition;
                    lineRenderer.SetPosition(0, startWorldPosition);
                    lineRenderer.SetPosition(1, currentWorldPosition);
                }
            }
        }

Example
*******

..  important::

    This example requires the following packages to be installed:

    *   TextMeshPro Essentials
    *   Input System

..  note::

    This example also includes utilities for processing touch inputs as seen in :ref:`Touch_Utilities`

Click to download :download:`EnhancedTouchDataExample.unitypackage </_downloads/EnhancedTouchDataExample.unitypackage>`.


Processing Touch Data Example
#############################

In the following code we are able to do more with processing touch input from the `EnhancedTouch.Touch <https://docs.unity3d.com/Packages/com.unity.inputsystem@1.0/manual/Touch.html#enhancedtouchtouch-class>`_
class. We have different behaviors for handling a single vs multiple touches.

Key Takeaways:
**************

*   We enable Enhanced Touch features by calling ``EnhancedTouchSupport.Enable();``
*   We connect Touch events to functions when enabling the TouchVisualizer (``Touch.onFingerDown += OnFingerDown;``).
*   We detect how many touches are occuring using ``Touch.activeTouches.Count`` and execute different behaviors
    depending on the amount of touches detected.
*   We extract touch data from individual touches using ``Touch.activeTouches[n]``.

..  note::

    In this example we gather touch data from ``Touch.activeTouches instead`` of ``Touch.activeFingers``
    since, at the time, touch data from fingers behaved in an odd way. For example, when the user's finger stopped moving,
    the `TouchPhase <https://docs.unity3d.com/ScriptReference/TouchPhase.html>`_ property of the touch data from ``Touch.activeFingers`` still registered as being
    ``Moved`` instead of stationary. Additionally the `delta <https://docs.unity3d.com/Packages/com.unity.inputsystem@1.0/api/UnityEngine.InputSystem.EnhancedTouch.Touch.html#UnityEngine_InputSystem_EnhancedTouch_Touch_delta>`_
    property would never reach 0. This was in contrast to touch data gathered from ``Touch.activeTouches`` which had phases and deltas that behaved
    as expected when a user's finger stopped moving.

..  dropdown:: **MultiTouchController.cs**

    ..  code-block:: c#

        using System.Collections;
        using System.Collections.Generic;
        using UnityEngine;
        using UnityEngine.InputSystem.EnhancedTouch;
        using Touch = UnityEngine.InputSystem.EnhancedTouch.Touch;
        using TouchPhase = UnityEngine.InputSystem.TouchPhase;

        public class MultiTouchController : MonoBehaviour
        {
            [SerializeField] private GameObject targetObject;
            [SerializeField] private Camera mainCamera;
            [SerializeField] private float rotationScaling;
            [SerializeField] private float zoomScaling;
            [SerializeField] private float maxFov;
            [SerializeField] private float minFov;

            private bool isTouching;
            private Plane xyPlane;

            private void Awake()
            {
                // We need to call EnhancedTouchSupport.Enable() to use the EnhancedTouch.Touch API.
                EnhancedTouchSupport.Enable();
            }

            void Start()
            {
                // We assume the user is not touching the screen at the start
                isTouching = false;

                xyPlane = new Plane(Vector3.forward, Vector3.zero);
            }

            // Connect Touch events to functions inside this class
            private void OnEnable()
            {
                Touch.onFingerDown += OnFingerDown;
                Touch.onFingerUp += OnFingerUp;
            }

            // Remove links to Touch events when this class is disabled
            private void OnDisable()
            {
                Touch.onFingerDown -= OnFingerDown;
                Touch.onFingerUp -= OnFingerUp;
            }

            public void OnFingerDown(Finger finger)
            {
                isTouching = true;
            }

            public void OnFingerUp(Finger finger)
            {
                if (Touch.activeFingers.Count == 0)
                {
                    isTouching = false;
                }
            }

            private void Handle2ActiveTouches()
            {
                Touch touch0 = Touch.activeTouches[0];
                Touch touch1 = Touch.activeTouches[1];
                if (touch0.phase == TouchPhase.Moved || touch1.phase == TouchPhase.Moved)
                {
                    // handle position
                    Vector2 currentPosition = (touch1.screenPosition + touch0.screenPosition) / 2;
                    Vector2 previousPosition = (touch1.screenPosition - touch1.delta + touch0.screenPosition - touch0.delta) / 2;
                    Vector3 currentWorldPosition = TouchUtilities.GetTouchPositionOnPlane(xyPlane, currentPosition);
                    Vector3 previousWorldPosition = TouchUtilities.GetTouchPositionOnPlane(xyPlane, previousPosition);
                    Vector3 delta = currentWorldPosition - previousWorldPosition;
                    targetObject.transform.position += new Vector3(delta.x, delta.y, 0);

                    // handle rotation
                    Vector2 currentDirection = touch1.screenPosition - touch0.screenPosition;
                    Vector2 previousDirection = (touch1.screenPosition - touch1.delta) - (touch0.screenPosition - touch0.delta);
                    float angle = Vector2.SignedAngle(previousDirection, currentDirection);
                    targetObject.transform.Rotate(new Vector3(0, 0, angle), Space.World);

                    // handle zoom
                    float currentDistance = currentDirection.magnitude;
                    float previousDistance = previousDirection.magnitude;
                    float zoomMagnitude = (currentDistance - previousDistance) * zoomScaling;
                    float newFov = mainCamera.fieldOfView / (1+zoomMagnitude);
                    if (zoomMagnitude < 0)
                    {
                        newFov = mainCamera.fieldOfView * (1-zoomMagnitude);
                    }
                    mainCamera.fieldOfView = Mathf.Clamp(newFov, minFov, maxFov);
                }
            }

            private void Handle1ActiveTouch()
            {
                Touch touch0 = Touch.activeTouches[0];
                if (touch0.phase == TouchPhase.Moved)
                {
                    // handle position
                    Vector3 currentWorldPosition = TouchUtilities.GetTouchPositionOnPlane(xyPlane, touch0.screenPosition);
                    Vector3 previousWorldPosition = TouchUtilities.GetTouchPositionOnPlane(xyPlane, touch0.screenPosition - touch0.delta);
                    Vector3 delta = currentWorldPosition - previousWorldPosition;
                    targetObject.transform.position += new Vector3(delta.x, delta.y, 0);
                }
            }

            void Update()
            {
                if (isTouching)
                {
                    int activeTouches = Touch.activeTouches.Count;
                    if (activeTouches >= 2)
                    {
                        Handle2ActiveTouches();
                    }
                    else if (activeTouches == 1)
                    {
                        Handle1ActiveTouch();
                    }
                }
            }
        }

..  important::

    This example requires the following packages to be installed:

    *   Input System

..  note::

    This example also includes utilities for processing touch inputs as seen in :ref:`Touch_Utilities`

Click to download :download:`EnhancedMultiTouchExample.unitypackage </_downloads/EnhancedMultiTouchExample.unitypackage>`.