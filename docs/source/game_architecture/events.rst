######
Events
######


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

..  image:: /_images/action_event_system_diagram.svg

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

..  image:: /_images/action_event_system_example_diagram.svg

.. _UnityEvents:

Event Architecture: Unity Events
################################

..  image:: /_images/unity_event_system_diagram.svg

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

..  image:: /_images/unity_event_system_example_diagram.svg

.. _Event_Architecture_Scriptable_Objects:

Event Architecture: Scriptable Objects
######################################

..  note::

    This section includes the use of Unity Events. See :ref:`UnityEvents` for more information.

..  note::

    For a video demo see  `ScriptableObject Events In Unity (C# Tutorial) | Unity Scriptable Objects <https://youtu.be/gXD2z_kkAXs>`_

..  image:: /_images/scriptable_object_event_system_diagram.svg


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

..  image:: /_images/scriptable_object_event_system_example_diagram.svg


.. _Event_Architecture_Scriptable_Objects_V2:

Event Architecture: Scriptable Objects V2
#########################################

We can refactor the above implementation for scriptable objects events so that:

*   Listeners are able to recieve any type of information
*   The game event listener component we add to game objects can listen in on multiple events

Because the data passed is an object, it is the responsibility of the scripts receiving the data
to cast the information to the correct type.

You can find the updated code and example below:


..  dropdown:: **GameEvent.cs + GameEventListener.cs (Single Object Argument Scriptable Object Event System)**

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
                RaiseListeners(null);
            }

            protected void RaiseListeners(object data)
            {
                // We go through the listeners in reverse in case some destroy themselves after the event is raised.
                for (int i = eventListeners.Count - 1; i >= 0; i--)
                {
                    eventListeners[i].OnEventRaised(data);
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

        // We make this class Serializable so that its properties are displayed in the inspector
        // when added to the GameEventListenerComponent's listeners list.
        [System.Serializable]
        public class GameEventListener
        {
            [Tooltip("Event to register with.")]
            public GameEvent Event;

            [Tooltip("Response to invoke when event is raised.")]
            public UnityEvent<object> Response;

            // We invoke the UnityEvent when we the GameEvent is raised
            public void OnEventRaised(object data)
            {
                Response.Invoke(data);
            }
        }

..  dropdown:: **IntGameEvent.cs (Adds a Raise function that accepts an int)**

    ..  code-block:: c#

        using UnityEngine;

        // GameEvent
        // IntGameEventListeners subscribe to the IntGameEvent asset
        // Other Scripts call the IntGameEvent's Raise(int) method

        // The CreateAssetMenu attribute allows us to create scriptable object assets in the editor
        // In the Editor: Right Click > Create > ScriptableObjects > IntGameEvent
        [CreateAssetMenu(fileName = "New IntGameEvent", menuName = "ScriptableObjects/IntGameEvent")]
        public class IntGameEvent : GameEvent
        {
            public void Raise(int data)
            {
                RaiseListeners(data);
            }
        }

..  dropdown:: **GameEventListenerComponent.cs (Attachable to Game Objects. Can listen into multiple Game Events)**

    ..  code-block:: c#

        using System.Collections;
        using System.Collections.Generic;
        using UnityEngine;

        public class GameEventListenerComponent : MonoBehaviour
        {
            public List<GameEventListener> listeners;

            private void OnEnable()
            {
                foreach (GameEventListener listener in listeners)
                {
                    listener.Event.RegisterListener(listener);
                }
            }

            private void OnDisable()
            {
                foreach (GameEventListener listener in listeners)
                {
                    listener.Event.UnregisterListener(listener);
                }
            }
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

            public void LogEventWithIntArgument(object data)
            {
                int number = (int)data;
                Debug.Log($"eventWithIntArgument has been invoked with value {number}");
            }
        }

Example
*******

Click to download :download:`ScriptableObjectEventSystemV2Example.unitypackage </_downloads/ScriptableObjectEventSystemV2Example.unitypackage>`.

.. _Event_Architecture_Scriptable_Objects_V3:

Event Architecture: Scriptable Objects V3
#########################################

This is mainly a refactoring of the V2 implementation for scriptable object events
(:ref:`Event_Architecture_Scriptable_Objects_V2`). In summary this was done to make the link between events
and the functions they called more explicit in the editor and code. See below for an in depth explanation:

*   In V2 game event listeners existed in their own separate monobehaviors. This made following links between game events
    and functions listening to those game events difficult. For example: On a player prefab you could have a
    PlayerController component and a Listener component. You can have the listener component contain a ``OnPlayerHurt`` game
    event and have it call PlayerController's ``TakeDamage()`` function when that hurt event was raised.
    This setup works just fine. However if you wanted to create a new prefab for a different kind of player object, you may
    start by adding a PlayerController component to it and then forget that you should also add a listener for a hurt event
    that calls the component's ``TakeDamage()`` function since there is no specific reference to a listener in the PlayerController component.
*   In V3 we have done away with the Game Event Listener component to discourage users from making links
    between events and functions that can be easy to miss. Scripts must now take game events in as arguments
    and register them directly with the methods they want to have called. The only downside of this approach is that scripts
    that to subscribe to these game events must be mindful of how they register and unregister function to events. Failure
    to register results in no functions called, and failure to unregister so that they aren't
    accidentally registered and called when they do not expect them to be.
    (Previously the listener component automatically registerd and unregistered on the ``OnEnable``
    ``OnDisable`` event functions.)
*   Game events no longer send data in a general object form. In V2 this was used in order to have the listener component
    accept any time of game event with any single argument input. Now that we have done away with the listener component,
    We thought it was better to keep the type of data passed into the raise method explicit to avoid confusion
*   Since we want to directly establish a link between the script functions and game events, we have decided to use
    ``UnityEvents`` and ``UnityActions`` since they allow us to pass functions as arguments and can directly
    register with events using the UnityEvent's ``AddListener()`` method.


You can find the updated code and example below:


..  dropdown:: **GameEvent.cs**

    ..  code-block:: c#

        using UnityEngine;
        using UnityEngine.Events;

        // GameEvent
        // Scripts can register functions with the the GameEvent asset
        // Scripts can call the GameEvent's Raise() method

        // The CreateAssetMenu attribute allows us to create scriptable object assets in the editor
        // In the Editor: Right Click > Create > ScriptableObjects > Events > GameEvent
        [CreateAssetMenu(fileName = "New GameEvent", menuName = "ScriptableObjects/Events/GameEvent")]
        public class GameEvent : ScriptableObject
        {
            // We use a unity event as it already has the infrastructure in place to register and call functions
            // With this event contained inside a scriptable object we will always be able to have it
            // accept listeners and be invoked.
            private UnityEvent gameEvent;

            public void Raise()
            {
                gameEvent.Invoke();
            }

            public void RegisterListener(UnityAction listener)
            {
                gameEvent.AddListener(listener);
            }

            public void UnregisterListener(UnityAction listener)
            {
                gameEvent.RemoveListener(listener);
            }
        }

..  dropdown:: **GameEventWithOneObject.cs + IntGameEvent.cs**

    ..  code-block:: c#

        using UnityEngine;
        using UnityEngine.Events;


        // This class allows us to define multiple child GameEvents that take arguments with explicit types
        public class GameEventWithOneArgument<T> : ScriptableObject
        {
            // We use a unity event as it already has the infrastructure in place to register and call functions
            // With this event contained inside a scriptable object we will always be able to have it
            // accept listeners and be invoked.
            private UnityEvent<T> gameEventWithOneArgument;

            public void Raise(T data)
            {
                gameEventWithOneArgument.Invoke(data);
            }

            public void RegisterListener(UnityAction<T> listener)
            {
                gameEventWithOneArgument.AddListener(listener);
            }

            public void UnregisterListener(UnityAction<T> listener)
            {
                gameEventWithOneArgument.RemoveListener(listener);
            }
        }

    ..  code-block:: c#

        using UnityEngine;

        // IntGameEvent
        // Scripts can register functions with the the IntGameEvent asset
        // Scripts can call the IntGameEvent's Raise() method

        // The CreateAssetMenu attribute allows us to create scriptable object assets in the editor
        // In the Editor: Right Click > Create > ScriptableObjects > Events > IntGameEvent
        [CreateAssetMenu(fileName = "New IntGameEvent", menuName = "ScriptableObjects/Events/IntGameEvent")]
        public class IntGameEvent : GameEventWithOneArgument<int>
        {

        }

..  dropdown:: **Publisher.cs + Subscriber.cs**

    ..  code-block:: c#

        using UnityEngine;

        public class Publisher : MonoBehaviour
        {
            public GameEvent onButtonPressGameEvent;
            public IntGameEvent onButtonPressIntEvent;

            void Update()
            {
                // When any key is pressed, raise both GameEvent assets
                if (Input.anyKeyDown)
                {
                    onButtonPressGameEvent.Raise();
                    onButtonPressIntEvent.Raise(42);
                }
            }
        }

    ..  code-block:: c#

        using UnityEngine;

        public class Subscriber : MonoBehaviour
        {
            public GameEvent onButtonPressGameEvent;
            public IntGameEvent onButtonPressIntEvent;

            // We want to register our functions when this game object is enabled
            private void OnEnable()
            {
                onButtonPressGameEvent.RegisterListener(LogEventWithNoArguments);
                onButtonPressIntEvent.RegisterListener(LogEventWithIntArgument);
            }

            // We want to stop registering our functions when this game object is disabled
            private void OnDisable()
            {
                onButtonPressGameEvent.UnregisterListener(LogEventWithNoArguments);
                onButtonPressIntEvent.UnregisterListener(LogEventWithIntArgument);
            }

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

Click to download :download:`ScriptableObjectEventSystemV3Example.unitypackage </_downloads/ScriptableObjectEventSystemV3Example.unitypackage>`.

