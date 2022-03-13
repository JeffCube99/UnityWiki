####################################
Managing Collections of Game Objects
####################################

..  contents::
    :local:

Object Pooling
##############

**"Creating new objects slows down the game. Lets reuse existing objects instead!"**

***************************
What Is Object Pooling For?
***************************

Using Unity's `Instantiate <https://docs.unity3d.com/ScriptReference/Object.Instantiate.html>`_ function can slow
down your game if you constantly creating objects including bullets, pickups, enemies, and obstacles. An alternative to
this is to have a ObjectPooler, a script that instantiates game objects up to a certain point and then reuses existing
objects when the game requires more objects spawned. Additionally, instead of destroying game objects when we are done
with them, we use `SetActive(false) <https://docs.unity3d.com/ScriptReference/GameObject.SetActive.html>`_.
This allows the ObjectPooler to call SetActive(true) to reuse the game objects again.

.. _Object_Pooling_Scriptable_Objects:

***********************************************
Object Pooling Architecture: Scriptable Objects
***********************************************

..  image:: /_images/scriptable_object_pooling_system_diagram.svg

..  dropdown:: **ObjectPool.cs**

    ..  code-block:: c#

        using System.Collections.Generic;
        using UnityEngine;

        [CreateAssetMenu(fileName = "NewObjectPool", menuName = "ScriptableObjects/ObjectPool")]
        public class ObjectPool : ScriptableObject
        {
            [SerializeField] private GameObject prefab;
            [SerializeField] private int maxObjects;

            private Queue<PooledObjectReference> spawnedItems;

            private PooledObjectReference SpawnObject()
            {
                GameObject newObject = Instantiate(prefab);
                ComponentOfPooledObject[] components = newObject.GetComponentsInChildren<ComponentOfPooledObject>();
                return new PooledObjectReference(newObject, components);
            }

            // Returns a PooledObjectReference from the ObjectPool
            // If the pool queue is empty or if it is less than full we spawn a new object, add its reference to the queue, and return its reference
            // If the pool queue is full we get the oldest reference from the queue:
            //      If the reference object still exists we add the reference back into the queue and return the reference
            //      If the reference object no longer exists, we spawn a new object, add its reference to the queue, and return its reference.
            private PooledObjectReference GetObjectReferenceFromPool()
            {
                if (spawnedItems == null)
                {
                    spawnedItems = new Queue<PooledObjectReference>();
                }

                if (spawnedItems.Count < maxObjects)
                {
                    PooledObjectReference newReference = SpawnObject();
                    spawnedItems.Enqueue(newReference);
                    return newReference;
                }
                else
                {
                    PooledObjectReference oldReference = spawnedItems.Dequeue();
                    if (oldReference.gameObject == null)
                    {
                        // If the object reference is null, the object has likely been destroyed. Therefore spawn a new object
                        PooledObjectReference newReference = SpawnObject();
                        spawnedItems.Enqueue(newReference);
                        return newReference;
                    }
                    else
                    {
                        spawnedItems.Enqueue(oldReference);
                        return oldReference;
                    }
                }
            }

            // Returns a game object from the object pool with its position and rotation set in world space
            public GameObject Instantiate(Vector3 position, Quaternion rotation)
            {
                return Instantiate(position, rotation, null);
            }

            // Returns a game object from the object pool parented to partent and with its position and rotation set relative to the parent.
            public GameObject Instantiate(Vector3 localPosition, Quaternion localRotation, Transform parent)
            {
                PooledObjectReference reference = GetObjectReferenceFromPool();
                GameObject pooledObject = reference.gameObject;
                // Deactivate the object prior to altering its transform
                pooledObject.SetActive(false);
                pooledObject.transform.parent = parent;
                pooledObject.transform.localPosition = localPosition;
                pooledObject.transform.localRotation = localRotation;
                pooledObject.SetActive(true);
                // Invoke OnSpawn events in the game object's components
                reference.InvokeOnSpawn();
                return pooledObject;
            }

        }

        // In addition to the object reference we also store references to
        // PooledObjectReference components to improve performance by eliminating
        // repeated calls to pooledObject.GetComponentsInChildren<ComponentOfPooledObject>
        public class PooledObjectReference
        {
            public GameObject gameObject;
            public ComponentOfPooledObject[] components;

            public PooledObjectReference(GameObject gameObjectInstance, ComponentOfPooledObject[] componentInstances)
            {
                gameObject = gameObjectInstance;
                components = componentInstances;
            }

            // Invokes the OnSpawn method contained within each pooledObjectComponent
            public void InvokeOnSpawn()
            {
                foreach (ComponentOfPooledObject component in components)
                {
                    component.OnSpawn();
                }
            }
        }

..  dropdown:: **ComponentOfPooledObject.cs**

    ..  code-block:: c#

        using UnityEngine;

        // A base class for any script that is attached to a pooled game object and needs to execute
        // some logic when the object is spawned by the pool. OnSpawn will execute even if this
        // is a component of a child object of the pooled object
        public abstract class ComponentOfPooledObject : MonoBehaviour
        {
            // Function called whenever the pooled object is spawned from the object pool
            public abstract void OnSpawn();
        }

..  dropdown:: **ImplementOnSpawn.cs + Spawner.cs**

    ..  code-block:: c#

        using UnityEngine;

        public class ImplementOnSpawn : ComponentOfPooledObject
        {
            public override void OnSpawn()
            {
                Debug.Log("Object Has Spawned From Object Pool");
            }
        }

    ..  code-block:: c#

        using UnityEngine;

        public class Spawner : MonoBehaviour
        {
            // We serialize the objectPool field so we can see it in the editor which allows
            // us to drag and drop the object pool reference in the editor
            [SerializeField] private ObjectPool objectPool;

            private void Start()
            {
                InvokeRepeating("SpawnObject", 1, 0.25f);
            }

            private void SpawnObject()
            {
                objectPool.Instantiate(Random.insideUnitSphere, Random.rotation);
            }
        }



Example
*******

Click to download :download:`ScriptableObjectPoolingExample.unitypackage </_downloads/ScriptableObjectPoolingExample.unitypackage>`.

..  image:: /_images/scriptable_object_pooling_system_example_diagram.svg

Runtime Sets
############

**"Fire All Weapons! . . . Ok but what and where are the weapons?"**

*************************
What Are Rutime Sets For?
*************************

There are scenarios in your game when you need to keep track of objects in the scene:

*   In a real time strategy game you may need access to a set for all your tanks, boats, or airplanes so that the
    player can select them with  a single keystroke.
*   In a game where you fight hordes of enemies the you may need access to the set of enemies in the level and the
    set of powerups in the world.
*   In a game where you manages a store you may need access to a set of all products and a sub set of produce products.

You can use runtime sets to track these things and give you the information when your game needs it.

********************************************
Runtime Set Architecture: Scriptable Objects
********************************************

..  note::

    For more information on Scriptable Object Runtime Sets, see `Unite Austin 2017 - Game Architecture with Scriptable Objects <https://youtu.be/raQ3iHhE_Kk?t=2311>`_

..  image:: /_images/scriptable_object_runtime_set_diagram.svg

..  dropdown:: **RuntimeSet.cs + AddItemToRuntimeSet.cs**

    ..  code-block:: c#

        using System.Collections.Generic;
        using UnityEngine;

        public abstract class RuntimeSet<T> : ScriptableObject
        {
            public List<T> items = new List<T>();

            public void Add(T thing)
            {
                if (!items.Contains(thing))
                    items.Add(thing);
            }

            public void Remove(T thing)
            {
                if (items.Contains(thing))
                    items.Remove(thing);
            }
        }


    ..  code-block:: c#

        using UnityEngine;

        public abstract class AddItemToRuntimeSet<T> : MonoBehaviour
        {
            [SerializeField] private RuntimeSet<T> runtimeSet;

            // Child classes get to decide how to extract the item from the game
            // object the component is attached to.
            protected abstract T GetItemFromGameObject(GameObject gameObject);

            private void OnEnable()
            {
                T item = GetItemFromGameObject(gameObject);
                if (item == null)
                {
                    ThrowExceptionForMissingItem(gameObject);
                }
                else
                {
                    runtimeSet.Add(item);
                }
            }

            private void OnDisable()
            {
                T item = GetItemFromGameObject(gameObject);
                if (item == null)
                {
                    ThrowExceptionForMissingItem(gameObject);
                }
                else
                {
                    runtimeSet.Remove(item);
                }
            }

            private void ThrowExceptionForMissingItem(GameObject gameObject)
            {
                Debug.LogError($"The game object '{gameObject}' does not contain elements required for the runtime set {runtimeSet.GetType().Name}");
            }
        }

..  dropdown:: **RuntimeSet.cs + AddItemToRuntimeSet.cs**

    ..  code-block:: c#

        using UnityEngine;

        // The CreateAssetMenu attribute allows us to create scriptable object assets in the editor
        // In the Editor: Right Click > Create > ScriptableObjects > RuntimeSets > GameObjectRuntimeSet
        [CreateAssetMenu(fileName = "NewGameObjectRuntimeSet", menuName = "ScriptableObjects/RuntimeSets/GameObjectRuntimeSet")]
        public class GameObjectRuntimeSet : RuntimeSet<GameObject>
        {

        }

    ..  code-block:: c#

        using UnityEngine;

        public class AddGameObjectToRuntimeSet : AddItemToRuntimeSet<GameObject>
        {
            protected override GameObject GetItemFromGameObject(GameObject gameObject)
            {
                return gameObject;
            }
        }

..  dropdown:: **Counter.cs**

    ..  code-block:: c#

        using UnityEngine;

        public class Counter : MonoBehaviour
        {
            public GameObjectRuntimeSet runtimeSet;

            void Start()
            {
                Debug.Log($"RuntimeSet '{runtimeSet.name}' contains {runtimeSet.items.Count} elements");
            }
        }

Example
*******

Click to download :download:`ScriptableObjectRuntimeSetExample.unitypackage </_downloads/ScriptableObjectRuntimeSetExample.unitypackage>`.

..  image:: /_images/scriptable_object_runtime_set_example_diagram.svg