##########
Events 2.0
##########


**"Something has happened and I would like you (script) to respond now"**

..  contents::
    :local:

What Are Events For?
####################

Events are useful for alerting other classes / game objects that something has happened. With scripting you
can configure some classes to raise events while others respond to events being raised. Here are some example
applications:

*   **Displaying Player Health**: Your game could have a UI element that displays a player's health bar.
    Instead of updating the health bar every frame, the UI element is configured to update whenever a
    ``OnPlayerHealthChanged`` event is raised.
*   **Pausing The Game**: When the player pauses the game, your game may require that all game objects must stop moving,
    player input must be disabled, and many more systems must change. Instead of a single game manager calling
    functions in scripts across the scene to pause the game, it could raise a ``OnGamePaused`` event and the other
    scripts listen for that event and respond accordingly.

Event Architecture: Action Events
#################################

..  note::

    For more about Action Events see `Delegates, Events, Actions and Funcs - The Observer Pattern (Unity & C#) <https://youtu.be/UWMmib1RYFE>`_

..  image:: /_images/action_event_system_diagram.png

..  dropdown:: **Publisher.cs**

    ..  code-block:: c#

        using UnityEngine;
        using System;

        public class Publisher : MonoBehaviour
        {
            public static event Action eventWithNoArguments;
            public static event Action<int> eventWithIntArgument;

            private void Update()
            {
                // When any key is pressed, invoke our events
                if (Input.anyKeyDown)
                {
                    // We use the (?) to check to see if our event has subscribers.
                    // If there are no subscribers we do not invoke the event. Otherwise we do invoke the event.
                    eventWithNoArguments?.Invoke();
                    eventWithIntArgument?.Invoke(42);
                }
            }
        }

..  dropdown:: **Subscriber.cs**

    ..  code-block:: c#

        using UnityEngine;

        public class Subscriber : MonoBehaviour
        {
            // We subscribe functions to action events in the Publisher class
            private void OnEnable()
            {
                Publisher.eventWithNoArguments += LogEventWithNoArguments;
                Publisher.eventWithIntArgument += LogEventWithIntArgument;
            }

            // We unsubscribe subscribe functions from action events in the Publisher class
            // If you do not unsubscribe and the subscriber class instance is destroyed, invoking the
            // Publisher class events will throw an error!
            private void OnDisable()
            {
                Publisher.eventWithNoArguments -= LogEventWithNoArguments;
                Publisher.eventWithIntArgument -= LogEventWithIntArgument;
            }

            private void LogEventWithNoArguments()
            {
                Debug.Log("eventWithNoArguments has been invoked");
            }

            private void LogEventWithIntArgument(int number)
            {
                Debug.Log($"eventWithIntArgument has been invoked with value {number}");
            }
        }

Example
*******

Click to download :download:`ActionEventSystemExample.unitypackage </_downloads/ActionEventSystemExample.unitypackage>`.

..  image:: /_images/action_event_system_example_diagram.png

.. _UnityEvents:

Event Architecture: Unity Events
################################

..  image:: /_images/unity_event_system_diagram.png

..  dropdown:: **Publisher.cs**

    ..  code-block:: c#

        using UnityEngine;
        using UnityEngine.Events;

        public class Publisher : MonoBehaviour
        {
            public UnityEvent eventWithNoArguments;
            public UnityEvent<int> eventWithIntArgument;

            void Update()
            {
                // When any key is pressed, invoke our events
                if (Input.anyKeyDown)
                {
                    // We use the (?) to check to see if our event has subscribers.
                    // If there are no subscribers we do not invoke the event. Otherwise we do invoke the event.
                    eventWithNoArguments?.Invoke();
                    eventWithIntArgument?.Invoke(42);
                }
            }
        }

..  dropdown:: **Subscriber.cs**

    ..  code-block:: c#

        using UnityEngine;

        // Note: We do not reference PublisherClass events in this class.
        // Event references are created in the unity editor.
        public class Subscriber : MonoBehaviour
        {
            public void LogEventWithNoArguments()
            {
                Debug.Log("eventWithNoArguments has been invoked");
            }

            public void LogEventWithIntArgument(int number)
            {
                Debug.Log($"eventWithIntArgument has been invoked with value {number}");
            }
        }

Example
*******

Click to download :download:`UnityEventSystemExample.unitypackage </_downloads/UnityEventSystemExample.unitypackage>`.

..  image:: /_images/unity_event_system_example_diagram.png


Event Architecture: Scriptable Objects
######################################

..  note::

    This section includes the use of Unity Events. See :ref:`UnityEvents` for more information.

..  note::

    For a video demo see  `ScriptableObject Events In Unity (C# Tutorial) | Unity Scriptable Objects <https://youtu.be/gXD2z_kkAXs>`_

..  image:: /_images/scriptable_object_event_system_diagram.png


..  dropdown:: **GameEvent.cs + GameEventListener.cs (Zero Argument Scriptable Object Event System)**

    ..  code-block:: c#

        using System.Collections.Generic;
        using UnityEngine;

        // GameEvent
        // GameEventListeners subscribe to the GameEvent asset
        // Other Scripts call the GameEvent's Raise() method

        // The CreateAssetMenu attribute allows us to create scriptable object assets in the editor
        // In the Editor: Right Click > Create > ScriptableObjects > GameEvent
        [CreateAssetMenu(fileName = "New GameEvent", menuName = "ScriptableObjects/GameEvent")]
        public class GameEvent : ScriptableObject
        {
            private readonly List<GameEventListener> eventListeners = new List<GameEventListener>();

            public void Raise()
            {
                // We go through the listeners in reverse in case some destroy themselves after the event is raised.
                for (int i = eventListeners.Count - 1; i >= 0; i--)
                {
                    eventListeners[i].OnEventRaised();
                }
            }

            public void RegisterListener(GameEventListener listener)
            {
                // Check to see that the eventListeners list does not already contain the target listener
                if (!eventListeners.Contains(listener))
                {
                    eventListeners.Add(listener);
                }
            }

            public void UnregisterListener(GameEventListener listener)
            {
                // Check to see that the eventListeners list contains the target listener
                if (eventListeners.Contains(listener))
                {
                    eventListeners.Remove(listener);
                }
            }
        }

    ..  code-block:: c#

        using UnityEngine;
        using UnityEngine.Events;

        public class GameEventListener : MonoBehaviour
        {
            [Tooltip("Event to register with.")]
            public GameEvent Event;

            [Tooltip("Response to invoke when event is raised.")]
            public UnityEvent Response;

            private void OnEnable()
            {
                // Registers instance to the GameEvent so OnEventRaised() is called if the GameEvent is raised
                Event.RegisterListener(this);
            }

            private void OnDisable()
            {
                // Unregisters instance to the GameEvent since OnEventRaised() does not need to be invoked when disabled.
                Event.UnregisterListener(this);
            }

            // We invoke the UnityEvent when we the GameEvent is raised
            public void OnEventRaised()
            {
                Response.Invoke();
            }
        }

..  dropdown:: **GenericGameEvent.cs + GenericGameEventListener.cs (Single Argument Scriptable Object Event System)**

    ..  code-block:: c#

        using System.Collections.Generic;
        using UnityEngine;

        // GenericGameEvent
        // GenericGameEventListeners subscribe to the GenericGameEvent asset
        // Other Scripts call the GameEvent's Raise() method with a parameter of type T
        public class GenericGameEvent<T> : ScriptableObject
        {
            private readonly List<GenericGameEventListener<T>> eventListeners = new List<GenericGameEventListener<T>>();

            public void Raise(T value)
            {
                // We go through the listeners in reverse in case some destroy themselves after the event is raised.
                for (int i = eventListeners.Count - 1; i >= 0; i--)
                {
                    eventListeners[i].OnEventRaised(value);
                }
            }

            public void RegisterListener(GenericGameEventListener<T> listener)
            {
                // Check to see that the eventListeners list does not already contain the target listener
                if (!eventListeners.Contains(listener))
                {
                    eventListeners.Add(listener);
                }
            }

            public void UnregisterListener(GenericGameEventListener<T> listener)
            {
                // Check to see that the eventListeners list contains the target listener
                if (eventListeners.Contains(listener))
                {
                    eventListeners.Remove(listener);
                }
            }
        }

    ..  code-block:: c#

        using UnityEngine;
        using UnityEngine.Events;

        public class GenericGameEventListener<T> : MonoBehaviour
        {
            [Tooltip("Event to register with.")]
            public GenericGameEvent<T> Event;

            [Tooltip("Response to invoke when event is raised.")]
            public UnityEvent<T> Response;

            private void OnEnable()
            {
                // Registers instance to the GameEvent so OnEventRaised() is called if the GameEvent is raised
                Event.RegisterListener(this);
            }

            private void OnDisable()
            {
                // Unregisters instance to the GameEvent since OnEventRaised() does not need to be invoked when disabled.
                Event.UnregisterListener(this);
            }

            // We invoke the UnityEvent when we the GameEvent is raised
            public void OnEventRaised(T value)
            {
                Response.Invoke(value);
            }
        }

..  dropdown:: **IntGameEvent.cs + IntGameEventListener.cs (Single Int Argument Scriptable Object Event System)**

    ..  code-block:: c#

        using UnityEngine;

        // GameEvent
        // IntGameEventListeners subscribe to the IntGameEvent asset
        // Other Scripts call the IntGameEvent's Raise(int) method

        // The CreateAssetMenu attribute allows us to create scriptable object assets in the editor
        // In the Editor: Right Click > Create > ScriptableObjects > IntGameEvent
        [CreateAssetMenu(fileName = "New IntGameEvent", menuName = "ScriptableObjects/IntGameEvent")]
        public class IntGameEvent : GenericGameEvent<int>
        {

        }

    ..  code-block:: c#

        public class IntGameEventListener : GenericGameEventListener<int>
        {

        }

..  dropdown:: **Publisher.cs + Subscriber.cs**

    ..  code-block:: c#

        using UnityEngine;
        using UnityEngine.Events;

        // Note: We do not reference scriptable object events in this class.
        // Scriptable object event references are set in the unity editor.
        public class Publisher : MonoBehaviour
        {
            public UnityEvent buttonPressNoArugmentEvent;
            public UnityEvent<int> buttonPressIntEvent;

            void Update()
            {
                // When any key is pressed, raise the GameEvent asset
                if (Input.anyKeyDown)
                {
                    buttonPressNoArugmentEvent.Invoke();
                    buttonPressIntEvent.Invoke(42);
                }
            }
        }

    ..  code-block:: c#

        using UnityEngine;

        // Note: We do not reference scriptable object events in this class.
        // Scriptable object event references are set in the unity editor.
        public class Subscriber : MonoBehaviour
        {
            public void LogEventWithNoArguments()
            {
                Debug.Log("eventWithNoArguments has been invoked");
            }

            public void LogEventWithIntArgument(int number)
            {
                Debug.Log($"eventWithIntArgument has been invoked with value {number}");
            }
        }

Example
*******

Click to download :download:`ScriptableObjectEventSystemExample.unitypackage </_downloads/ScriptableObjectEventSystemExample.unitypackage>`.

..  image:: /_images/scriptable_object_event_system_example_diagram.png
