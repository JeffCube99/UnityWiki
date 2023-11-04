==========================================
Coroutines (AKA Running tasks on the side)
==========================================

How Coroutines Work
===================

Coroutines can be used to spread tasks across several frames. At a basic level coroutines are functions that execute
code in one frame until they hit a ``yield`` statement. Then then they pause execution until the next frame. In the
next frame they then resume execution starting from the ``yield`` statement.

When Does The Body Of A Coroutine Function Run?
===============================================

Coroutines typically run after the ``Update`` function returns. The execution inside
can be paused and resumed be altered based on the type of ``yield`` expression used:

*   ``yield``: Resume after all ``Update`` Functions are called.
*   ``yield WaitForSeconds``: Resume after all ``Update`` Functions after specified time delay.
*   ``yield WaitForFixedUpdate``: Resume after all ``FixedUpdate`` Functions are called. Can be invoked
    twice in the same frame if a yield was called prior to FixedUpdate.
*   ``yield WWW``: Resume after WWW download has completed.
*   ``yield StartCoroutine("X")``: Resume after coroutine "X" completes execution.

How Coroutines Stop
===================

Coroutines stop under the following conditions:

*   They finish executing the coroutine function (No infinite yield loops)
*   The user executes `StopCoroutine() <https://docs.unity3d.com/ScriptReference/MonoBehaviour.StopCoroutine.html>`_
    on a specific coroutine or halts all coroutines in the script using
    `StopAllCoroutines() <https://docs.unity3d.com/ScriptReference/MonoBehaviour.StopAllCoroutines.html>`_.
*   The game object the script is attached to is destroyed or sets SetActive to false.

    ..  note::

        If you disabled MonoBehaviour by setting
        `enabled <https://docs.unity3d.com/ScriptReference/Behaviour-enabled.html>`_ to false Unity will not stop
        coroutines.

Basic Coroutines
================

.. dropdown:: Print "Hello" to the Console Once

    ..  code-block:: c#

        public class PrintHelloOnce : MonoBehaviour
        {
            void Start()
            {
                StartCoroutine(PrintHelloWorld());
            }

            IEnumerator PrintHelloWorld()
            {
                Debug.Log("Hello World");
                // No more code to execute. The Coroutine PrintHelloWorld stops execution
            }
        }

.. dropdown:: Print "Hello" to the Console Every Frame

    ..  code-block:: c#

        public class PrintHelloEveryFrame : MonoBehaviour
        {
            void Start()
            {
                StartCoroutine(PrintHelloWorld());
            }

            IEnumerator PrintHelloWorld()
            {
                // We call yield inside an infinite loop.
                // This results in the body of the loop executing once each frame.
                while (true)
                {
                    Debug.Log("Hello World");
                    yield return null;
                }
            }
        }

.. dropdown:: Print "Hello" to the Console Every Frame Every Few Seconds

    ..  code-block:: c#

        public class PrintHelloEveryFewSeconds : MonoBehaviour
        {
            void Start()
            {
                StartCoroutine(PrintHelloWorld());
            }

            IEnumerator PrintHelloWorld()
            {
                // We call yield inside an infinite loop with WaitForSeconds(2.0f);
                // This results in the body of the loop executing in a frame every 2 seconds.
                while (true)
                {
                    Debug.Log("Hello World");
                    yield return new WaitForSeconds(2.0f);
                }
            }
        }

    ..  note::

        This effect can also be accomplished using the
        `InvokeRepeating() <https://docs.unity3d.com/ScriptReference/MonoBehaviour.InvokeRepeating.html>`_ function.

.. dropdown:: Print "Hello" to the Console After Every 2 Seconds

    ..  code-block:: c#

        public class PrintHelloEveryFewSeconds : MonoBehaviour
        {
            public float delay = 2f;

            void Start()
            {
                // We pass a variable delay into the coroutine
                StartCoroutine(PrintHelloWorld(delay));
            }

            IEnumerator PrintHelloWorld(float delay)
            {
                // We call yield inside an infinite loop with WaitForSeconds(delay);
                // This results in the body of the loop executing in a frame at an interval determined by "delay".
                while (true)
                {
                    Debug.Log("Hello World");
                    yield return new WaitForSeconds(delay);
                }
            }
        }

    ..  note::

        This effect can also be accomplished using the
        `InvokeRepeating() <https://docs.unity3d.com/ScriptReference/MonoBehaviour.InvokeRepeating.html>`_ function.

.. dropdown:: Print "Hello" to the Console Every Frame Until The User Stops It

    ..  code-block:: c#

        public class PrintHelloUntilUserStopsCoroutine : MonoBehaviour
        {
            // we save the coroutine to a variable so we have
            // a reference to it when using StartCoroutine() and StopCoroutine()
            private IEnumerator coroutine;

            void Start()
            {
                coroutine = PrintHelloWorld();
                StartCoroutine(coroutine);
            }

            private void Update()
            {
                // We stop the coroutine when the user presses the space bar
                if (Input.GetKeyDown(KeyCode.Space))
                {
                    StopCoroutine(coroutine);
                }
            }

            IEnumerator PrintHelloWorld()
            {
                // We call yield inside an infinite loop.
                // This results in the body of the loop executing once each frame.
                while (true)
                {
                    Debug.Log("Hello World");
                    yield return null;
                }
            }
        }

Working With Multiple Coroutines
================================

.. dropdown:: Run Coroutines In Parallel

    ..  code-block:: c#

        public class PrintHelloAndGoodbyeSimultaneously : MonoBehaviour
        {
            void Start()
            {
                RunCoroutinesSimultaneously();
            }

            public void RunCoroutinesSimultaneously()
            {
                StartCoroutine(PrintWordFor5Seconds("Hello"));
                StartCoroutine(PrintWordFor5Seconds("Goodbye"));
            }

            IEnumerator PrintWordFor5Seconds(string word)
            {
                float count = 0;
                while (count < 5)
                {
                    Debug.Log(word);
                    count++;
                    yield return new WaitForSeconds(1.0f);
                }
            }
        }

.. dropdown:: Run Coroutines One After The Other

    ..  code-block:: c#

        public class PrintReadySetGo : MonoBehaviour
        {
            void Start()
            {
                StartCoroutine(RunCoroutinesOneAfterTheOther());
            }

            IEnumerator RunCoroutinesOneAfterTheOther()
            {
                yield return StartCoroutine(PrintWordAndPauseForOneSecond("Ready"));
                yield return StartCoroutine(PrintWordAndPauseForOneSecond("Set"));
                yield return StartCoroutine(PrintWordAndPauseForOneSecond("Go"));
            }

            IEnumerator PrintWordAndPauseForOneSecond(string word)
            {
                Debug.Log(word);
                yield return new WaitForSeconds(1.0f);
            }
        }

.. dropdown:: Have Coroutines Run Other Coroutines

    ..  code-block:: c#

        public class BossEntersAndSaysHi : MonoBehaviour
        {
            void Start()
            {
                StartCoroutine(BossMakesAnEntrance());
            }

            IEnumerator BossMakesAnEntrance()
            {
                Debug.Log("Boss Begins To Enter The Room");
                yield return new WaitForSeconds(1.0f);
                yield return StartCoroutine(BossGreetsThePlayerAfterOneSecond());
                Debug.Log("Boss Finishes Entering");
            }

            IEnumerator BossGreetsThePlayerAfterOneSecond()
            {
                yield return new WaitForSeconds(1.0f);
                Debug.Log("Hello Champion");
            }
        }