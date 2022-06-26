======
States
======

..  contents::
    :local:

Overview
========

In games sometimes you need to track the state of things. For Example:

*   The Direction you are traveling: North, South, East, West
*   The player's health: 1-3
*   The action your player is performing: Idle, Walk, Run, Attack
*   Items in a chest: Food, Weapons, Money
*   Game State: InGame, InMenu, Victory, GameOver
*   Weapon Types: Stabbing, Blugeoning, Magical

This section covers several ways on how to manage game state logic.

State Example: Rock Paper Scissors
==================================

The examples in this section demonstrate the following behaviors:

*   There exists game objects in the scene with a state of Rock, Paper, and Scissors
*   When these game objects collide the loser is destroyed (rock collides with scissors -> scissors is destroyed)

The examples in this section also explore the following questions:

*   If we we add a new state to the scene ("Dynamite") that can destroy Rock, Paper, Scissors and Dynamite,
    how difficult is it to implement it given the existing game structure?

Using Enum States
-----------------

..  tip::

    *   Enums are good for a fixed number of elements. If you anticipate adding additional elements in the future
        be prepared to make extensive edits to your code, especially if many scrips reference the enum.

Base Implementation
^^^^^^^^^^^^^^^^^^^

*   **Elemental**

    *   Defines an enum ``Element`` with items "Rock", "Paper", and "Scissors"
    *   Has a ``Element`` attribute
    *   Has a method that detects if it can destroy another element
    *   OnTriggerEnter destroys the other game object if the other contains an element it can destroy.

..  dropdown:: The ``Elemental`` class.

    ..  code-block:: c#

        using UnityEngine;
        using System;

        public class Elemental : MonoBehaviour
        {
            public enum Element
            {
                Rock,
                Paper,
                Scissors
            }

            public Element element;

            public bool CanDestoryElement(Element otherElement)
            {
                switch (otherElement)
                {
                    case Element.Rock:
                        return element == Element.Paper;
                    case Element.Paper:
                        return element == Element.Scissors;
                    case Element.Scissors:
                        return element == Element.Rock;
                    default:
                        throw new ArgumentOutOfRangeException(nameof(otherElement), otherElement, null);
                }
            }

            private void OnTriggerEnter(Collider other)
            {
                Elemental otherElemental = other.gameObject.GetComponent<Elemental>();
                if (otherElemental != null)
                {
                    if (CanDestoryElement(otherElemental.element))
                    {
                        Destroy(other.gameObject);
                    }
                }
            }
        }

..  dropdown:: Game objects with ``Elemental`` components in the scene.

    ..  image:: /_images/game_state_rps_enum.png

Adding Dynamite Implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*   Had to add a new enum to the ``Element`` enum.
*   Had to update the logic of CanDestoryElement. Had to add a switch case for Dynamite and had to account for the
    Dynamite under other cases.


..  dropdown:: The ``Elemental`` class with Dynamite.

    ..  code-block:: c#
        :emphasize-lines: 11, 21, 23, 25, 26, 27

        using UnityEngine;
        using System;

        public class Elemental : MonoBehaviour
        {
            public enum Element
            {
                Rock,
                Paper,
                Scissors,
                Dynamite,
            }

            public Element element;

            public bool CanDestoryElement(Element otherElement)
            {
                switch (otherElement)
                {
                    case Element.Rock:
                        return element == Element.Paper || element == Element.Dynamite;
                    case Element.Paper:
                        return element == Element.Scissors || element == Element.Dynamite;
                    case Element.Scissors:
                        return element == Element.Rock || element == Element.Dynamite;
                    case Element.Dynamite:
                        return element == Element.Dynamite;
                    default:
                        throw new ArgumentOutOfRangeException(nameof(otherElement), otherElement, null);
                }
            }

            private void OnTriggerEnter(Collider other)
            {
                Elemental otherElemental = other.gameObject.GetComponent<Elemental>();
                if (otherElemental != null)
                {
                    if (CanDestoryElement(otherElemental.element))
                    {
                        Destroy(other.gameObject);
                    }
                }
            }
        }

Using Scriptable Object States
------------------------------

*   This example code was created from  `Unite Austin 2017 - Game Architecture with Scriptable Objects <https://youtu.be/raQ3iHhE_Kk?t=2732>`_

Base Implementation
^^^^^^^^^^^^^^^^^^^

*   **Element**

    *   A Scriptable Object
    *   Contains a list (``CanDestory``) of elements that it can destroy

*   **Elemental**

    *   Has a ``Element`` attribute
    *   OnTriggerEnter destroys the other game object if it contains an element that is present
        in the Element's ``CanDestory`` List

*   **In the Unity Editor**

    #.  Next create 3 scriptable object assets from ``Element`` and name them Rock, Paper, and Scissors
    #.  Inside the Rock asset, we add Scissors to the ``CanDestory`` List. This repeats similarly for Paper and Scissors.


..  dropdown:: The ``Element`` scriptable object.

    ..  code-block:: c#

        using System.Collections.Generic;
        using UnityEngine;

        // The CreateAssetMenu attribute allows us to create scriptable object assets in the editor
        // In the Editor: Right Click > Create > ScriptableObjects > GameEvent
        [CreateAssetMenu(fileName = "New Element", menuName = "ScriptableObjects/Element")]
        public class Element : ScriptableObject
        {
            [Tooltip("The elements this element can destroy")]
            public List<Element> CanDestroy = new List<Element>();
        }


..  dropdown:: The ``Elemental`` class.

    ..  code-block:: c#

        using UnityEngine;

        public class Elemental : MonoBehaviour
        {
            public Element element;

            private void OnTriggerEnter(Collider other)
            {
                Elemental otherElemental = other.gameObject.GetComponent<Elemental>();
                if (otherElemental != null)
                {
                    if (element.CanDestroy.Contains(otherElemental.element))
                    {
                        Destroy(other.gameObject);
                    }
                }
            }
        }


..  dropdown:: ``Element`` Scriptable Object Assets + Game objects with ``Elemental`` components.

    ..  image:: /_images/game_state_rps_so_0.png

    ..  image:: /_images/game_state_rps_so_1.png


Adding Dynamite Implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*   We create a new scriptable object assets from ``Element`` and name it Dynamite
*   Inside the Dynamite asset, we add Rock, Paper, and Scissors to the ``CanDestory`` List.

..  dropdown:: Dynamite asset + Dynamite Game Object

    ..  image:: /_images/game_state_rps_so_2.png


Scriptable Object Variables
===========================

Lets say you have a scene with the name ``level_0`` and you use the string ``level_0`` in some of your scripts.
Maybe at some point you change the level name or you want the level to be replaced by a scene with the name ``level_1``.
In this scenario you would have to track down each use of the ``level_0`` string and replace it with ``level_1``. Instead
of repeating this process every time the scene name is altered, you could make a reference to a scriptable object
storing the strings value. Now if the string needs to be altered all you would have to do is change the string inside
the scriptable object.

Implementation
--------------

*   **FloatVariable**

    *   A scriptable object that Contains the property ``value`` with the type float

*   **FloatReference**

    *   Contains a property ``floatVariable`` of type ``FloatVariable`` as well as property of ``constantValue`` of type ``float``
    *   The user can opt to use the value of the constant or float variable by specifying the boolean property ``useConstant``
    *   scripts retrieve a float from FloatReference using the ``value`` property.

*   Other scriptable objects of different types can be built off of the same framework of the 2 above classes.

..  dropdown:: The ``FloatVariable`` scriptable object and ``Float Reference`` class:

    ..  code-block:: c#

        using UnityEngine;
        using System;

        [CreateAssetMenu(fileName = "New FloatVariable", menuName = "ScriptableObjects/Variables/FloatVariable")]
        [Serializable]
        public class FloatVariable : ScriptableObject
        {
            public float value;
        }

    ..  code-block:: c#

        using System;

        [Serializable]
        public class FloatReference
        {
            public bool useConstant;
            public float constantValue;
            public FloatVariable floatVariable;

            public float value
            {
                get
                {
                    if (useConstant)
                    {
                        return constantValue;
                    }
                    else
                    {
                        return floatVariable.value;
                    }
                }
            }
        }

..  dropdown:: The ``StringVariable`` scriptable object and ``StringReference`` class:

    ..  code-block:: c#

        using UnityEngine;
        using System;

        [CreateAssetMenu(fileName = "New StringVariable", menuName = "ScriptableObjects/Variables/StringVariable")]
        [Serializable]
        public class StringVariable : ScriptableObject
        {
            public string value;
        }

    ..  code-block:: c#

        using System;

        [Serializable]
        public class StringReference
        {
            public bool useConstant;
            public string constantValue;
            public StringVariable stringVariable;

            public string value
            {
                get
                {
                    if (useConstant)
                    {
                        return constantValue;
                    }
                    else
                    {
                        return stringVariable.value;
                    }
                }
            }
        }

..  dropdown:: An example script that uses scriptable object variables:

    ..  code-block:: c#

        using UnityEngine;

        public class TestScript : MonoBehaviour
        {
            public FloatVariable health;
            public FloatReference healthReference;
            public StringVariable name;
            public StringReference nameReference;

            private void Start()
            {
                InteractWithFloatVariable();
                InteractWithStringVariable();
            }

            private void InteractWithFloatVariable()
            {
                Debug.Log($"Health equals {health.value}");
                health.value += 1;
                Debug.Log($"Adding 1 to health");
                Debug.Log($"New Health equals {health.value}");

                Debug.Log($"Health reference equals {healthReference.value}");
            }

            private void InteractWithStringVariable()
            {
                Debug.Log($"Name equals {name.value}");
                name.value += "bob";
                Debug.Log($"Adding 'bob' to Name");
                Debug.Log($"New Name equals {name.value}");

                Debug.Log($"Name reference equals {nameReference.value}");
            }
        }

Example
-------

Click to download :download:`ScriptableObjectVariablesExample.unitypackage </_downloads/ScriptableObjectVariablesExample.unitypackage>`.