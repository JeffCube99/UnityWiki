########################
Asynchronous Programming
########################

Links
#####

    For more information see:

    *   https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/async-scenarios
    *   https://youtu.be/WY-mk-ZGAq8?si=4hqQlNIcgiLG0auF
    *   https://github.com/davidfowl/AspNetCoreDiagnosticScenarios/blob/master/AsyncGuidance.md#asynchronous-programming
    *   https://randompoison.github.io/posts/unity-async/

Overview
########

If you need to run code that takes an unpredictable amount of time to finish, use
asynchronous programming to run the operation in a separate thread and monitor the task
to check when it completes.

..  important::

    It seems that if you choose to add async functions to your scripts, the best practice
    is to only call them using other async functions. Unity allows users to add the async keyword
    to event functions like ``Awake`` ``Start`` and ``OnEnable``. So you can call your
    async methods from there.

When Does The Body Of An Asynchronous Function Run?
###################################################

*   An async method runs synchronously (the function that called the async method waits) until it reaches its first await expression.
    Then it is suspended until the awaited task is complete. In the meantime control returns to the caller of the method.
*   (As I understand it) In unity you can call ``await Task.Yield()`` to essentially suspend an async method for at minimum one frame.
    (As I understand it) This is made possible through Unity's `UnitySynchronizationContext <https://github.com/Unity-Technologies/UnityCsReference/blob/master/Runtime/Export/Scripting/UnitySynchronizationContext.cs>`_
    since by default async / await logic relies on the default `SynchronizationContext <https://learn.microsoft.com/en-us/archive/msdn-magazine/2011/february/msdn-magazine-parallel-computing-it-s-all-about-the-synchronizationcontext>`_
    which has no concept of frames in unity.

When Does an Asynchronous Function Stop?
########################################

*   Async functions only stop once they execute through all of their code (run to completion).
*   Async functions in scripts attached to objects are not tied to a GameObject and will continue to run even if the object
    they are attached to is destroyed. This also means that they will continue to run even if a new scene
    is loaded.

..  important::

    *   Unity `warns <https://docs.unity3d.com/Manual/overview-of-dot-net-in-unity.html>`_ us that
        async tasks are not automatically stopped when exiting play mode!!! So if you have an async
        function that loops infinitely / never quits you may be stuck with it running while in
        the editor.
    *   If this happens to you. To cancel all async tasks being run outside of play mode, simply
        enter play mode again. You can enter play mode in an empty scene so that you aren't accidentally
        calling async functions again in play mode.

How To Cancel Asynchronous Functions In Unity
#############################################

..  note::

    If you are using unity and are tyring to cancel an async method that is out of your control, simply enter
    play mode (preferably in an empty scene is best since there is no risk of re executing the functions that got
    out of control in the first place).

Because asynchronous functions can continue to execute even when loading in new scenes or exiting play mode,
It is important to have a way to terminate async functions in case things go wrong and in the worse case
they are stuck in an infinite loop. The convention for cancelling async functions appears to be introducing
try finally statements into the async function and raising an error when we want to exit early.
For raising these errors we use `CancellationTokens <https://learn.microsoft.com/en-us/dotnet/api/system.threading.cancellationtoken?view=net-7.0>`_

See examples below:

..  important::

    While the following examples showcase their functionality, I recommend that every async you use
    in unity has at least the ability to cancel when the object is destroyed.

..  dropdown:: Cancel Async Method When Object Is Destroyed

    ..  code-block:: c#

        using System;
        using System.Threading;
        using System.Threading.Tasks;
        using UnityEngine;

        public class CancelAsyncAfterObjectIsDestroyed : MonoBehaviour
        {
            private CancellationTokenSource cancellationTokenSource;

            // Start is called before the first frame update
            async void Start()
            {
                // Destroy game object after 5 seconds
                Destroy(gameObject, 10);
                cancellationTokenSource = new CancellationTokenSource();
                try
                {
                    await ExampleTask(cancellationTokenSource.Token);
                }
                catch (OperationCanceledException)
                {
                    Debug.Log("Operation was cancelled");
                }
            }

            private void OnDestroy()
            {
                CancelAndDisposeCancellationTokenSource();
            }

            private void CancelCancellationTokenSource()
            {
                if (cancellationTokenSource != null && !cancellationTokenSource.IsCancellationRequested)
                {
                    cancellationTokenSource.Cancel();
                }
            }

            private void CancelAndDisposeCancellationTokenSource()
            {
                CancelCancellationTokenSource();
                cancellationTokenSource?.Dispose();
            }

            private async Task ExampleTask(CancellationToken cancellationToken)
            {
                while (true)
                {
                    Debug.Log("Hello World");
                    await Task.Delay(TimeSpan.FromSeconds(1), cancellationToken);

                    // // You could alternatively choose this method if you wanted to print every frame
                    // if (cancellationToken.IsCancellationRequested)
                    // {
                    //     cancellationToken.ThrowIfCancellationRequested();
                    // }
                    // await Task.Yield();
                }
            }
        }


..  dropdown:: Cancel Async Method After Time Has Passed

    ..  code-block:: c#

        using System;
        using System.Threading;
        using System.Threading.Tasks;
        using UnityEngine;

        public class CancelAsyncAfterTimeHasPassed : MonoBehaviour
        {
            private CancellationTokenSource cancellationTokenSource;

            // Start is called before the first frame update
            async void Start()
            {
                cancellationTokenSource = new CancellationTokenSource();
                // Cancel after 5 seconds
                cancellationTokenSource.CancelAfter(TimeSpan.FromSeconds(5));
                try
                {
                    await ExampleTask(cancellationTokenSource.Token);
                }
                catch (OperationCanceledException)
                {
                    Debug.Log("Operation was cancelled");
                }
            }

            private void OnDestroy()
            {
                CancelAndDisposeCancellationTokenSource();
            }

            private void CancelCancellationTokenSource()
            {
                if (cancellationTokenSource != null && !cancellationTokenSource.IsCancellationRequested)
                {
                    cancellationTokenSource.Cancel();
                }
            }

            private void CancelAndDisposeCancellationTokenSource()
            {
                CancelCancellationTokenSource();
                cancellationTokenSource?.Dispose();
            }

            private async Task ExampleTask(CancellationToken cancellationToken)
            {
                while (true)
                {
                    Debug.Log("Hello World");
                    await Task.Delay(TimeSpan.FromSeconds(1), cancellationToken);

                    // // You could alternatively choose this method if you wanted to print every frame
                    // if (cancellationToken.IsCancellationRequested)
                    // {
                    //     cancellationToken.ThrowIfCancellationRequested();
                    // }
                    // await Task.Yield();
                }
            }
        }

..  dropdown:: Cancel Async Method When Key Is Pressed

    ..  code-block:: c#

        using System;
        using System.Threading;
        using System.Threading.Tasks;
        using UnityEngine;

        public class CancelAsyncOnKeyPress : MonoBehaviour
        {
            private CancellationTokenSource cancellationTokenSource;

            // Start is called before the first frame update
            async void Start()
            {
                cancellationTokenSource = new CancellationTokenSource();
                try
                {
                    await ExampleTask(cancellationTokenSource.Token);
                }
                catch (OperationCanceledException)
                {
                    Debug.Log("Operation was cancelled");
                }
            }

            private void Update()
            {
                // We stop the async operation when the user presses the space bar
                if (Input.GetKeyDown(KeyCode.Space))
                {
                    CancelCancellationTokenSource();
                }
            }

            private void OnDestroy()
            {
                CancelAndDisposeCancellationTokenSource();
            }

            private void CancelCancellationTokenSource()
            {
                if (cancellationTokenSource != null && !cancellationTokenSource.IsCancellationRequested)
                {
                    cancellationTokenSource.Cancel();
                }
            }

            private void CancelAndDisposeCancellationTokenSource()
            {
                CancelCancellationTokenSource();
                cancellationTokenSource?.Dispose();
            }

            private async Task ExampleTask(CancellationToken cancellationToken)
            {
                while (true)
                {
                    Debug.Log("Hello World");
                    await Task.Delay(TimeSpan.FromSeconds(1), cancellationToken);

                    // // You could alternatively choose this method if you wanted to print every frame
                    // if (cancellationToken.IsCancellationRequested)
                    // {
                    //     cancellationToken.ThrowIfCancellationRequested();
                    // }
                    // await Task.Yield();
                }
            }
        }



Examples
########

Basic Asynchronous Programming
******************************

.. dropdown:: Print "Hello" to the Console Once

    ..  code-block:: c#

        using System.Threading.Tasks;
        using UnityEngine;

        public class PrintHelloOnceAsync : MonoBehaviour
        {

            // Start is called before the first frame update
            async void Start()
            {
                await PrintHelloAsync();
            }

            private async Task PrintHelloAsync()
            {
                Debug.Log("Hello World");
                await Task.Yield();
            }

        }

.. dropdown:: Print "Hello" to the Console Every 2 Seconds

    ..  code-block:: c#

        using System;
        using System.Threading;
        using System.Threading.Tasks;
        using UnityEngine;

        public class PrintHelloEveryFewSecondsAsync : MonoBehaviour
        {
            private CancellationTokenSource cancellationTokenSource;
            public int millisecondDelay = 2000;

            // Start is called before the first frame update
            async void Start()
            {
                await PrintHelloAsync();
            }

            private void OnDestroy()
            {
                CancelAndDisposeCancellationTokenSource();
            }

            private void CancelCancellationTokenSource()
            {
                if (cancellationTokenSource != null && !cancellationTokenSource.IsCancellationRequested)
                {
                    cancellationTokenSource.Cancel();
                }
            }

            private void CancelAndDisposeCancellationTokenSource()
            {
                CancelCancellationTokenSource();
                cancellationTokenSource?.Dispose();
            }

            private async Task PrintHelloAsync()
            {
                try
                {
                    cancellationTokenSource = new CancellationTokenSource();
                    await PrintHelloRepeatedlyAsync(cancellationTokenSource.Token);
                }
                catch (OperationCanceledException ex)
                {
                    Debug.Log("Detected Cancellation");
                }
                finally
                {
                    cancellationTokenSource.Dispose();
                    cancellationTokenSource = null;
                }
            }

            private async Task PrintHelloRepeatedlyAsync(CancellationToken cancellationToken)
            {
                while (true)
                {
                    Debug.Log("Hello World");

                    if (cancellationToken.IsCancellationRequested)
                    {
                        cancellationToken.ThrowIfCancellationRequested();
                    }

                    await Task.Delay(millisecondDelay, cancellationToken);
                }
            }
        }


..  dropdown:: Print "Hello" to the Console Every Frame Until The User Stops It

    ..  code-block:: c#

        using System;
        using System.Threading;
        using System.Threading.Tasks;
        using UnityEngine;

        public class PrintHelloUntilUserStopsAsync : MonoBehaviour
        {
            private CancellationTokenSource cancellationTokenSource;

            // Start is called before the first frame update
            async void Start()
            {
                await PrintHelloAsync();
            }

            private void Update()
            {
                // We stop the async operation when the user presses the space bar
                if (Input.GetKeyDown(KeyCode.Space))
                {
                    CancelAsyncOperation();
                }
            }

            private void OnDestroy()
            {
                CancelAndDisposeCancellationTokenSource();
            }

            private void CancelCancellationTokenSource()
            {
                if (cancellationTokenSource != null && !cancellationTokenSource.IsCancellationRequested)
                {
                    cancellationTokenSource.Cancel();
                }
            }

            private void CancelAndDisposeCancellationTokenSource()
            {
                CancelCancellationTokenSource();
                cancellationTokenSource?.Dispose();
            }

            private async Task PrintHelloAsync()
            {
                try
                {
                    cancellationTokenSource = new CancellationTokenSource();
                    await PrintHelloRepeatedlyAsync(cancellationTokenSource.Token);
                }
                catch (OperationCanceledException ex)
                {
                    Debug.Log("Detected Cancellation");
                }
                finally
                {
                    cancellationTokenSource.Dispose();
                    cancellationTokenSource = null;
                }
            }

            private async Task PrintHelloRepeatedlyAsync(CancellationToken cancellationToken)
            {
                while (true)
                {
                    Debug.Log("Hello World");

                    if (cancellationToken.IsCancellationRequested)
                    {
                        cancellationToken.ThrowIfCancellationRequested();
                    }

                    await Task.Yield();
                }
            }
        }


Working With Multiple Async Functions
*************************************

.. dropdown:: Run Async Methods In Parallel

    ..  code-block:: c#

        using System;
        using System.Collections.Generic;
        using System.Threading;
        using System.Threading.Tasks;
        using UnityEngine;

        public class PrintHelloAndGoodbyeSimultaneouslyAsync : MonoBehaviour
        {
            private CancellationTokenSource cancellationTokenSource;

            // Start is called before the first frame update
            async void Start()
            {
                await PrintHelloAsync();
            }

            private void OnDestroy()
            {
                CancelAndDisposeCancellationTokenSource();
            }

            private void CancelCancellationTokenSource()
            {
                if (cancellationTokenSource != null && !cancellationTokenSource.IsCancellationRequested)
                {
                    cancellationTokenSource.Cancel();
                }
            }

            private void CancelAndDisposeCancellationTokenSource()
            {
                CancelCancellationTokenSource();
                cancellationTokenSource?.Dispose();
            }

            private async Task PrintHelloAsync()
            {
                try
                {
                    cancellationTokenSource = new CancellationTokenSource();
                    List<Task> taskList = new List<Task>();
                    taskList.Add(PrintWordRepeatedlyAsync("Hello", cancellationTokenSource.Token));
                    taskList.Add(PrintWordRepeatedlyAsync("Goodbye", cancellationTokenSource.Token));
                    await Task.WhenAll(taskList);
                }
                catch (OperationCanceledException ex)
                {
                    Debug.Log("Detected Cancellation");
                }
                finally
                {
                    cancellationTokenSource.Dispose();
                    cancellationTokenSource = null;
                }
            }

            private async Task PrintWordRepeatedlyAsync(string word, CancellationToken cancellationToken)
            {
                while (true)
                {
                    Debug.Log(word);

                    if (cancellationToken.IsCancellationRequested)
                    {
                        Debug.Log("Throw Cancellation Request");
                        cancellationToken.ThrowIfCancellationRequested();
                    }

                    await Task.Yield();
                }
            }
        }


.. dropdown:: Run Async Methods One After The Other

    ..  code-block:: c#

        using System;
        using System.Threading;
        using System.Threading.Tasks;
        using UnityEngine;

        public class PrintReadySetGoAsync : MonoBehaviour
        {
            private CancellationTokenSource cancellationTokenSource;

            // Start is called before the first frame update
            async void Start()
            {
                await PrintHelloAsync();
            }

            private void OnDestroy()
            {
                CancelAndDisposeCancellationTokenSource();
            }

            private void CancelCancellationTokenSource()
            {
                if (cancellationTokenSource != null && !cancellationTokenSource.IsCancellationRequested)
                {
                    cancellationTokenSource.Cancel();
                }
            }

            private void CancelAndDisposeCancellationTokenSource()
            {
                CancelCancellationTokenSource();
                cancellationTokenSource?.Dispose();
            }

            private async Task PrintHelloAsync()
            {
                try
                {
                    cancellationTokenSource = new CancellationTokenSource();
                    await PrintWordAndPauseForOneSecondAsync("Ready", cancellationTokenSource.Token);
                    await PrintWordAndPauseForOneSecondAsync("Set", cancellationTokenSource.Token);
                    await PrintWordAndPauseForOneSecondAsync("Go", cancellationTokenSource.Token);
                }
                catch (OperationCanceledException ex)
                {
                    Debug.Log("Detected Cancellation");
                }
                finally
                {
                    cancellationTokenSource.Dispose();
                    cancellationTokenSource = null;
                }
            }

            private async Task PrintWordAndPauseForOneSecondAsync(string word, CancellationToken cancellationToken)
            {
                Debug.Log(word);
                await Task.Delay(1000, cancellationToken);
            }
        }

.. dropdown:: Have Async Functions Run Other Async Functions

    ..  code-block:: c#

        using System;
        using System.Threading;
        using System.Threading.Tasks;
        using UnityEngine;

        public class BossEntersAndSaysHiAsync : MonoBehaviour
        {
            private CancellationTokenSource cancellationTokenSource;

            // Start is called before the first frame update
            async void Start()
            {
                await BossMakesAnEntrance();
            }

              private void OnDestroy()
            {
                CancelAndDisposeCancellationTokenSource();
            }

            private void CancelCancellationTokenSource()
            {
                if (cancellationTokenSource != null && !cancellationTokenSource.IsCancellationRequested)
                {
                    cancellationTokenSource.Cancel();
                }
            }

            private void CancelAndDisposeCancellationTokenSource()
            {
                CancelCancellationTokenSource();
                cancellationTokenSource?.Dispose();
            }

            private async Task BossMakesAnEntrance()
            {
                try
                {
                    cancellationTokenSource = new CancellationTokenSource();
                    await BossTalksAsync("Boss: How is the grind?", cancellationTokenSource.Token);
                }
                catch (OperationCanceledException ex)
                {
                    Debug.Log("Detected Cancellation");
                }
                finally
                {
                    cancellationTokenSource.Dispose();
                    cancellationTokenSource = null;
                }
            }

            private async Task BossTalksAsync(string words, CancellationToken cancellationToken)
            {
                Debug.Log(words);
                await Task.Delay(4000, cancellationToken);
                await EmployeeReplyAsync("Employee: Nothing Much", "Employee: Doing Work", cancellationToken);
            }

            private async Task EmployeeReplyAsync(string words0, string words1, CancellationToken cancellationToken)
            {
                Debug.Log(words0);
                await Task.Delay(4000, cancellationToken);
                Debug.Log(words1);
                await Task.Delay(4000, cancellationToken);
            }
        }

Tasks
#####

Returning Values From Tasks
***************************

You can specify the return type of the task using the ``Task<return_type>`` syntax. When we await on a task with
a return type, when the task finishes it returns a value of that type.

.. dropdown:: Returning a value from a task.

    ..  code-block:: c#

        using System;
        using System.Threading;
        using System.Threading.Tasks;
        using UnityEngine;

        public class ReturningValuesFromTasks : MonoBehaviour
        {
            private CancellationTokenSource cancellationTokenSource;

            private async void Start()
            {
                cancellationTokenSource = new CancellationTokenSource();
                try
                {
                    int result = await ExampleTask(cancellationTokenSource.Token);
                    Debug.Log($"Result from async operation is {result}");
                }
                catch (OperationCanceledException)
                {
                    Debug.Log($"Operation was cancelled");
                }
            }

            private void OnDestroy()
            {
                CancelAndDisposeCancellationTokenSource();
            }

            private void CancelCancellationTokenSource()
            {
                if (cancellationTokenSource != null && !cancellationTokenSource.IsCancellationRequested)
                {
                    cancellationTokenSource.Cancel();
                }
            }

            private void CancelAndDisposeCancellationTokenSource()
            {
                CancelCancellationTokenSource();
                cancellationTokenSource?.Dispose();
            }


            private async Task<int> ExampleTask(CancellationToken cancellationToken)
            {
                await Task.Delay(TimeSpan.FromSeconds(5), cancellationToken);
                return 0;
            }
        }


Complete, Cancel, Or Fault a Task outside the Task
**************************************************

To control a task outside the task function, like for example stopping a task when a condition is reached, you can use
a TaskCompletionSource. Note that ``TaskCanceledException`` is invoked when awaiting a cancelled task. This is slightly
different from the ``OperationCanceledException`` which is thrown explicitly when working with cancellation tokens.
Also note that the exceptions passed to the ``TrySetException`` will be thrown when awaiting the task that has an
exception set.

.. dropdown:: Completing, Cancelling, Or Faulting a Task From Outside the Task

    ..  code-block:: c#

        using System;
        using System.Threading;
        using System.Threading.Tasks;
        using UnityEngine;

        public class ControlTaskFromOutsideTask : MonoBehaviour
        {
            private CancellationTokenSource cancellationTokenSource;
            private TaskCompletionSource<int> taskCompletionSource;

            private async void Start()
            {
                cancellationTokenSource = new CancellationTokenSource();
                taskCompletionSource = new TaskCompletionSource<int>();

                // Register a callback to cancel the TaskCompletionSource when the token is canceled
                cancellationTokenSource.Token.Register(() => taskCompletionSource.TrySetCanceled(cancellationTokenSource.Token));

                try
                {
                    int result = await taskCompletionSource.Task;
                    Debug.Log($"Result from task completion source task is {result}");
                }
                catch (TaskCanceledException)
                {
                    Debug.Log($"Task was canceled.");
                }
                catch (Exception ex)
                {
                    Debug.Log($"Task failed with exception: {ex.Message}");
                }
            }

            private void OnDestroy()
            {
                CancelAndDisposeCancellationTokenSource();
            }

            private void CancelCancellationTokenSource()
            {
                if (cancellationTokenSource != null && !cancellationTokenSource.IsCancellationRequested)
                {
                    cancellationTokenSource.Cancel();
                }
            }

            private void CancelAndDisposeCancellationTokenSource()
            {
                CancelCancellationTokenSource();
                cancellationTokenSource?.Dispose();
            }

            public void CompleteTask()
            {
                taskCompletionSource.TrySetResult(42);
            }

            public void CancelTask()
            {
                taskCompletionSource.TrySetCanceled();
            }

            public void ErrorTask()
            {
                try
                {
                    throw new InvalidOperationException("Throwing Exception On Purpose");
                }
                catch (Exception e)
                {
                    taskCompletionSource.TrySetException(e);
                }
            }
        }
