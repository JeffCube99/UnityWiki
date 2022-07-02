====================
Information Transfer
====================

..  contents::
    :local:

Overview
========

This section covers some ways information can be transferred in a unity project.
Some examples include transferring information between game objects, scenes, and play sessions.


Transfer Information Between Game Objects
=========================================

**Example:** We have 2 scripts (``PlayerController`` and ``PlayerUI``) on 2 different game objects.
Both scripts call functions that require the player's health. How can both
of these game objects get access to the same player health variable?

Referencing the Other Game Object
---------------------------------

We can have the ``PlayerController`` class store the player health variable. Then we have the ``PlayerUI`` class have
a variable that references the ``PlayerController`` class and use that reference to get the player health from
``PlayerController``.

..  warning::

    This method can reduce the modularity of your game and make testing more difficult.
    In this example, since ``PlayerUI`` depends on a ``PlayerController`` existing in the scene,
    if you wanted to test the behavior of ``PlayerUI`` B in a new scene you must also add a ``PlayerController`` to
    the scene. This can become cumbersome when your game architecture has a web of references.

..  dropdown:: A class ``PlayerController`` that contains and uses a ``playerHealth`` variable.

    ..  code-block:: c#

        using UnityEngine;

        public class PlayerController : MonoBehaviour
        {
            public int playerHealth;
            void Start()
            {
                Debug.Log($"PlayerController Logging Player Health: {playerHealth}");
            }
        }

..  dropdown:: A class ``PlayerUI`` that has a reference to ``PlayerController`` to access the ``playerHealth`` variable.

    ..  code-block:: c#

        using UnityEngine;

        public class PlayerUI : MonoBehaviour
        {
            public PlayerController playerController;

            void Start()
            {
                // Acces player health from playerController
                Debug.Log($"PlayerUI Logging Player Health: {playerController.playerHealth}");
            }
        }

    Below is an image showing how we give a ``PlayerController`` reference to ``PlayerUI`` in the editor.

    ..  image:: /_images/game_object_reference.png

Using Scriptable Objects
------------------------

We can have a scriptable object ``Health`` contain the player health variable. From this we create a ``PlayerHealth``
asset that we use to store the player's health. Then we can give ``PlayerController`` and ``PlayerUI`` a reference to
``PlayerHealth`` thus giving both classes access to the player's health.

For more on scriptable objects as data containers, see: `Unite Austin 2017 - Game Architecture with Scriptable Objects <https://youtu.be/raQ3iHhE_Kk?list=PLuldlT8dkudpCEkYQJb_H26BcbE7ozisX&t=926>`_

..  dropdown:: A scriptable object (Heath) that contains a health variable.

    ..  code-block:: c#

        using UnityEngine;

        // The CreateAssetMenu attribute allows us to create scriptable object assets in the editor
        // In the Editor: Right Click > Create > ScriptableObjects > Health
        [CreateAssetMenu(fileName = "NewHealth", menuName = "ScriptableObjects/Health")]
        public class Health : ScriptableObject
        {
            public int health;
        }

    Below is an image showing how we create a scriptable object asset ``PlayerHealth`` from the Health script in the editor.

    ..  image:: /_images/scriptable_object_asset_creation_1.png

    ..  image:: /_images/scriptable_object_asset_1.png

..  dropdown:: A class ``PlayerController`` that references the scriptable object asset of type``Health``.

    ..  code-block:: c#

        using UnityEngine;

        public class PlayerController : MonoBehaviour
        {
            public Health playerHealth;
            void Start()
            {
                Debug.Log($"PlayerController Logging Player Health: {playerHealth.health}");
            }
        }

    Below is an image showing how we give a ``PlayerController`` reference to the ``PlayerHealth`` asset in the editor.

    ..  image:: /_images/game_object_reference_1.png

..  dropdown:: A class ``PlayerUI`` that references the scriptable object asset of type``Health``.

    ..  code-block:: c#

        using UnityEngine;

        public class PlayerUI : MonoBehaviour
        {
            public Health playerHealth;

            void Start()
            {
                Debug.Log($"PlayerUI Logging Player Health: {playerHealth.health}");
            }
        }

Transfer Information Between Scenes
===================================


**Example:** A player has 3 lives and he loses 1 life in scene #1. When we load scene #2, how can the game
remember how many lives the player has?

Using A Static Class
--------------------

A static class can persist between scene changes. This means any information stored within the static class will also
persist between scene changes and can be accessed by scripts in the new scene.

..  warning::

    Data in a static class can be accessed from anywhere. This can introduce bugs when multiple developers attempt to
    modify static variables. The project can end up having multiple classes reading and writing to static variables
    without taking into account each other's logic. Additionally it hard to identify where changes to static
    variables are coming from when they can be accessed by anyone.

..  dropdown:: A static class that tracks player lives.

    ..  code-block:: c#

        // Static classes cannot inherit from MonoBehaviour
        public static class PlayerInformation
        {
            // Variables inside static classes must use the static keyword.
            public static int lives;
        }

..  dropdown:: A class that can set the value of player lives.

    ..  code-block:: c#

        using UnityEngine;

        public class SetPlayerInformation : MonoBehaviour
        {
            public void SetPlayerLives(int lives)
            {
                PlayerInformation.lives = lives;
            }
        }

..  dropdown:: A class that can retrieve the value of player lives.

    ..  code-block:: c#

        using UnityEngine;

        public class DisplayPlayerInformation : MonoBehaviour
        {
            void Start()
            {
                // Access the lives variable within the static PlayerInformation class
                Debug.Log($"Lives: {PlayerInformation.lives}");
            }
        }



Using Scriptable Objects
------------------------

A scriptable object can contain information and is stored as an asset in your project.
This means that it persists through scene changes and you can give scripts references to the scriptable object
to read and write information from it.

*   `Link to video example <https://www.youtube.com/watch?v=SmnjRCa_iO4>`_

..  warning::

    Changes you make to scriptable objects in play mode will persist while in the editor. If you are not careful
    you could accidentally build a game with scriptable objects containing values you did not want.
    For example, if you have a scriptable object tracking how many lives the player has and during your
    play testing that amount is set to 10 before you exit play mode, the scriptable object will now have that value set
    to 10. If you then build the game, when starting the game up the player will start with 10 lives. You can fix
    this issue any number of ways. For example you can have a game manager that makes sure to reset the lives
    to 3 at the start of each level.

..  dropdown:: A scriptable object class and asset that contains the player's lives.

    ..  code-block:: c#

        using UnityEngine;

        // The CreateAssetMenu attribute allows us to create scriptable object assets in the editor
        // In the Editor: Right Click > Create > PlayerInformation
        [CreateAssetMenu(fileName = "New PlayerInformation", menuName = "PlayerInformation")]
        public class PlayerInformation_ScriptableObject : ScriptableObject
        {
            public int lives;
        }

    Below is an image showing how we create a scriptable object asset from the PlayerInformation_ScriptableObject script
    in the editor.

    ..  image:: /_images/scriptable_object_asset_creation.png

    ..  image:: /_images/scriptable_object_asset.png


..  dropdown:: A class that can set the value of player lives in the scriptable object asset.

    ..  code-block:: c#

        using UnityEngine;

        public class SetPlayerInformation_ScriptableObject : MonoBehaviour
        {
            // This is a reference to the player info scriptable object asset
            public PlayerInformation_ScriptableObject playerInformation;

            // We change the value of lives within the player info scriptable object asset
            public void SetPlayerLives(int lives)
            {
                playerInformation.lives = lives;
            }
        }

    Below is an image showing how we give the above script reference to the scriptable object asset.

    ..  image:: /_images/scriptable_object_set_asset_reference.png


..  dropdown:: A class that can retrieve the value of player lives from the scriptable object asset.

    ..  code-block:: c#

        using UnityEngine;

        public class DisplayPlayerInformation_ScriptableObject : MonoBehaviour
        {
            // This is a reference to the player info scriptable object asset
            public PlayerInformation_ScriptableObject playerInformaiton;

            void Start()
            {
                // We retrieve the value of lives within the player info scriptable object asset
                Debug.Log($"Lives: {playerInformaiton.lives}");
            }
        }

    Below is an image showing how we give the above script reference to the scriptable object asset.

    ..  image:: /_images/scriptable_object_set_asset_reference2.png


Using DontDestroyOnLoad
-----------------------

By default, all game objects from the previous scene are destroyed when we open a new scene. If we call
`DontDestroyOnLoad() <https://docs.unity3d.com/ScriptReference/Object.DontDestroyOnLoad.html>`_ on a game object,
that object will continue to exist into the next scene. This means that
any information the game object has will be carried into the new scene. Objects in the new scene can then
access that game object to retrieve the information.

.. dropdown:: A class that tracks player lives and persists between scenes.

    ..  code-block:: c#

        using UnityEngine;

        public class PlayerInformation : MonoBehaviour
        {
            // We create a static instance so that the class be easily accessed from other scripts.
            // We use a private setter so other scripts cannot modify the value of Instance.
            public static PlayerInformation Instance { get; private set; }
            public int lives;

            private void Awake()
            {
                // We only want one PlayerInformation instance to exist. If a PlayerInformation is initialized (Awake),
                // it will destroy itself if it detects that another PlayerInformation instance already exists. Otherwise
                //  it sets itself as the instance.
                if (Instance != null)
                {
                    Destroy(gameObject);
                    return;
                }
                Instance = this;

                // Keeps the game object from being destroyed. when a new scene loads.
                DontDestroyOnLoad(gameObject);
            }
        }

.. dropdown:: A class that retrieves the information from the PlayerInformation class in the new scene.

    ..  code-block:: c#

        public class PlayerInfoReader : MonoBehaviour
        {
            private void Start()
            {
                // We check to see if an instance of PlayerInformation exists.
                if (PlayerInformation.Instance != null)
                {
                    Debug.Log(PlayerInformation.Instance.lives);
                }
            }
        }


Transfer Information Between Sessions
=====================================

**Example:** A player has unlocked levels 1-3 in your game. The player then closes the game. When the player
re-opens the game, how can the game remember the levels the player has unlocked?

Using JSON Serialization
------------------------

Unity can convert unity objects into JSON text through
`JSON Serialization <https://docs.unity3d.com/Manual/JSONSerialization.html>`_ and save that text using
`File.WriteAllText() <https://docs.microsoft.com/en-us/dotnet/api/system.io.file.writealltext?view=net-6.0>`_ to a standard location at
`Application.persistentDataPath <https://docs.unity3d.com/ScriptReference/Application-persistentDataPath.html>`_.

..  warning::

    JSON Serialization does not support data types like ``Dictionary<>``. For a comprehensive list of supported
    types, see `JSON Serialization <https://docs.unity3d.com/Manual/JSONSerialization.html>`_


.. dropdown:: A class that saves and loads information from a JSON save file.

    ..  code-block:: c#

        using UnityEngine;
        using System.IO;  // Needed for us to use `Path` and `File` classes

        public class LevelManager : MonoBehaviour
        {
            public int levelsUnlocked;

            private static string SAVE_FILE_PATH;

            private void Awake()
            {
                // Define the location of the save file.
                SAVE_FILE_PATH = Path.Combine(Application.persistentDataPath, "savefile.json");
            }

            // We use LevelData to store the number of levels the player has unlocked.
            // `[System.Serializable]` is needed for any class used with JSON Serializer API
            [System.Serializable]
            class LevelData
            {
                public int levelsUnlocked;
            }

            public void SaveProgress()
            {
                // Store information in a new LevelData class
                LevelData data = new LevelData();
                data.levelsUnlocked = levelsUnlocked;

                // Convert LevelData class into a json string
                string jsonData = JsonUtility.ToJson(data);

                // Write the string to the file at SAVE_FILE_PATH
                File.WriteAllText(SAVE_FILE_PATH, jsonData);
            }

            public void LoadProgress()
            {
                // We only load information if the save file exists
                if (File.Exists(SAVE_FILE_PATH))
                {
                    // Load the json string from the savefile
                    string jsonData = File.ReadAllText(SAVE_FILE_PATH);

                    // Convert the json string back into a LevelData class
                    LevelData data = JsonUtility.FromJson<LevelData>(jsonData);

                    // Retrieve the levelsUnlocked from the loaded LevelData class
                    levelsUnlocked = data.levelsUnlocked;
                }
            }
        }

Using Binary Serialization
--------------------------

In unity you can save data to custom binary files. These files are harder to read than json files and make them
slightly more secure.

.. dropdown:: A class that saves and loads information from a BINARY save file.

    ..  code-block:: c#

        using UnityEngine;
        using System.IO; // Needed for us to use `Path` and `File` classes
        using System.Runtime.Serialization.Formatters.Binary; // Needed for us to use the `BinaryFormatter` class

        public class LevelManager : MonoBehaviour
        {
            public int levelsUnlocked;

            private static string SAVE_FILE_PATH;

            private void Awake()
            {
                // Define the location of the save file.
                SAVE_FILE_PATH = Path.Combine(Application.persistentDataPath, "savefile.bin");
            }

            // We use LevelData to store the number of levels the player has unlocked.
            // `[System.Serializable]` is needed for any class saved to a binary file
            [System.Serializable]
            class LevelData
            {
                public int levelsUnlocked;
            }

            public void SaveProgress()
            {
                // Store information in a new LevelData class
                LevelData data = new LevelData();
                data.levelsUnlocked = levelsUnlocked;

                // Use a binary formatter combined with a file stream to save the data to a file at SAVE_FILE_PATH
                BinaryFormatter formatter = new BinaryFormatter();
                FileStream stream = new FileStream(SAVE_FILE_PATH, FileMode.Create);
                formatter.Serialize(stream, data);

                // Close the stream after we are finished using it
                stream.Close();
            }

            public void LoadProgress()
            {
                // We only load information if the save file exists
                if (File.Exists(SAVE_FILE_PATH))
                {
                    // Load the data from the savefile using the binary formatter and filestream.
                    BinaryFormatter formatter = new BinaryFormatter();
                    FileStream stream = new FileStream(SAVE_FILE_PATH, FileMode.Open);
                    LevelData data = formatter.Deserialize(stream) as LevelData;

                    // Close the stream after we are finished using it
                    stream.Close();

                    // Retrieve the levelsUnlocked from the loaded LevelData class
                    levelsUnlocked = data.levelsUnlocked;
                }
                else
                {
                    Debug.LogError("Save file not found in " + SAVE_FILE_PATH);
                    return;
                }
            }
        }


Scriptable Object Save System Example
-------------------------------------

..  note::

    Some of the code in this example was lifted from `Save SCRIPTABLE OBJECTS - Unity Tutorial <https://www.youtube.com/watch?v=Bv-Qie4ISWg>`_

This save system is useful if your game stores its information inside scriptable objects. Scriptable
objects can use this system to store their data in binary files. You can coordinate the saving of
data throughout the game with a use of a central scriptable object that has references to all other scriptable
objects that contain data. Additionally its supports multiple save files.

Implementation:

*   **ISaveLoad.cs**

    *   An interface for scriptable objects that allows them to work within the save system.
    *   The interface makes the scriptable object responsible for saving and loading its own data.

*   **SaveSystemUtilities.cs**

    *   Utility functions that allow for the saving and loading of data to binary files.
    *   Contains functions that help identify the saves that do and do not exist as well as functions to generate new
        save names if the need arises

*   **SaveSystem.cs**

    *   A scriptable object you can use in game to coordinate saving and loading game data.
    *   The save system contains reference to scriptable objects that implement the ISaveLoad inteface

..  dropdown:: **ISaveLoad.cs**

    ..  code-block:: c#

        public interface ISaveLoad
        {
            // Returns the name the class gives to the data. This name should be unique to the class
            // instance and should not be held by other classes implementing this inteface to avoid save collisions.
            string GetDataName();

            // Classes that implement this function should save their data in file with a path
            // that incorporates the save name. If an error is encountered during the save process
            // this function should return a string about the error. Otherwise it returns a null / empty string.
            string Save(string saveName);

            // Classes that implement this function should load their data from file with a path
            // that incorporates the save name. If an error is encountered during the load process
            // this function should return a string about the error. Otherwise it returns a null / empty string.
            string Load(string saveName);

            // Resets the class to a default state. Used when the player starts a new game.
            // If an error is encountered during the reset process
            // this function should return a string about the error. Otherwise it returns a null / empty string.
            string Reset();
        }


..  dropdown:: **SaveSystemUtilities.cs**

    ..  code-block:: c#

        using System.Collections;
        using System.Collections.Generic;
        using UnityEngine;
        using System.IO;
        using System.Runtime.Serialization.Formatters.Binary;

        /// <summary>
        /// These utilities are built for a save system where:
        ///     *   Each save game has a particular name. That name is used as a parent directory
        ///         that houses all files for that save game.
        ///     *   One can have multiple save games.
        /// </summary>
        public static class SaveSystemUtilities
        {
            const string SAVE_FILE_EXTENSION = ".bin";
            const string PARENT_SAVE_DIRECTORY_NAME = "saves";
            const string DEFAULT_SAVE_NAME = "NewGame";

            // Returns the parent directory that contains all save directories
            private static string GetSaveSystemParentDirectory()
            {
                return Path.Combine(Application.persistentDataPath, PARENT_SAVE_DIRECTORY_NAME);
            }

            // Returns a path for a save directory with a given save name
            private static string GetSaveDirectoryPath(string saveName)
            {
                return Path.Combine(GetSaveSystemParentDirectory(), saveName);
            }

            // Returns a filepath that incorporates the name of the data and save name.
            private static string GetSaveDataFilePath(string dataName, string saveName)
            {
                return Path.Combine(GetSaveDirectoryPath(saveName), dataName + SAVE_FILE_EXTENSION);
            }

            private static void CreateSaveDirectories(string saveName)
            {
                string saveSystemDirectoryPath = GetSaveSystemParentDirectory();
                string saveDirectoryPath = GetSaveDirectoryPath(saveName);
                if (!Directory.Exists(saveSystemDirectoryPath))
                {
                    Directory.CreateDirectory(saveSystemDirectoryPath);
                }
                if (!Directory.Exists(saveDirectoryPath))
                {
                    Directory.CreateDirectory(saveDirectoryPath);
                }
            }

            // Save your data to a file with a path that incorporates the name of the data and save file name.
            public static void Save<T>(T data, string dataName, string saveName)
            {
                // If the directories we save files to have not been created, create them.
                CreateSaveDirectories(saveName);

                BinaryFormatter binaryFormatter = new BinaryFormatter();
                string saveDataFilePath = GetSaveDataFilePath(dataName, saveName);
                FileStream fileStream = new FileStream(saveDataFilePath, FileMode.Create);
                binaryFormatter.Serialize(fileStream, data);
                fileStream.Close();
            }

            // Attempts to load the data for the specified data under the save file.
            // If the data is found it returns it, otherwise it returns the default value of the type.
            public static T Load<T>(string dataName, string saveName)
            {
                T data = default;
                if (SaveDataExists(dataName, saveName))
                {
                    string saveDataFilePath = GetSaveDataFilePath(dataName, saveName);
                    BinaryFormatter binaryFormatter = new BinaryFormatter();
                    FileStream fileStream = new FileStream(saveDataFilePath, FileMode.Open);
                    data = (T)binaryFormatter.Deserialize(fileStream);
                }

                return data;
            }

            // Returns true if the save (directory) exists
            public static bool SaveExists(string saveName)
            {
                string saveDirectoryPath = GetSaveDirectoryPath(saveName);
                return Directory.Exists(saveDirectoryPath);
            }

            // Returns true if the save file exists for data under a save file name
            public static bool SaveDataExists(string dataName, string saveName)
            {
                string saveDataFilePath = GetSaveDataFilePath(dataName, saveName);
                return File.Exists(saveDataFilePath);
            }

            // Deletes a save (directory) if it exists
            public static void DeleteSave(string saveName)
            {
                if (SaveExists(saveName))
                {
                    // Delete the save directory and its subdirectories.
                    Directory.Delete(GetSaveDirectoryPath(saveName), true);
                }
            }

            // Returns a list of all save names that exist
            public static List<string> GetAllSaveNames()
            {
                List<string> saveNames = new List<string>();
                DirectoryInfo directoryInfo = new DirectoryInfo(GetSaveSystemParentDirectory());
                DirectoryInfo[] directories = directoryInfo.GetDirectories();
                foreach (DirectoryInfo directory in directories)
                {
                    saveNames.Add(directory.Name);
                }
                return saveNames;
            }

            // Generates a save name that has not been used yet.
            public static string GenerateNewSaveName()
            {
                string saveName;
                int count = 0;

                do
                {
                    saveName = DEFAULT_SAVE_NAME + count;
                    count += 1;
                }
                while (SaveExists(saveName));

                return saveName;
            }
        }


..  dropdown:: **SaveSystem.cs**

    ..  code-block:: c#

        using System.Collections;
        using System.Collections.Generic;
        using UnityEngine;
        using UnityEngine.Events;

        /// <summary>
        /// The Save System helps to coordinate the saving and loading of game data
        /// into scriptable objects that implement the ISaveLoad interface.
        /// </summary>
        [CreateAssetMenu(fileName = "SaveSystem", menuName = "ScriptableObjects/SaveLoadGame/SaveSystem")]
        public class SaveSystem : ScriptableObject
        {
            // The current save name. This is kept in memory for convenience.
            public string currentSaveName;
            // List of scriptable objects (that implement the ISaveLoad interface) that  save / load data
            public List<ScriptableObject> gameDataObjects;

            // UnityEvents that are triggered in the case of errors
            public UnityEvent<string> OnSaveError;
            public UnityEvent<string> OnLoadError;
            public UnityEvent<string> OnStartGameError;

            // Returns a list of objects that have implemented the ISaveLoad intefrace.
            // Any object that has not implemented the interface will not be included.
            private List<ISaveLoad> GetSaveLoadObjects()
            {
                List<ISaveLoad> saveLoadObjects = new List<ISaveLoad>();
                foreach (ScriptableObject gameDataObject in gameDataObjects)
                {
                    if (gameDataObject is ISaveLoad)
                    {
                        ISaveLoad saveloadObject = (ISaveLoad)gameDataObject;
                        saveLoadObjects.Add(saveloadObject);
                    }
                }
                return saveLoadObjects;
            }

            // Checks to see that objects that are saving and loading each save to
            // a unique file name.
            private bool SaveCollisionsDetected(string saveName)
            {
                List<ISaveLoad> saveLoadObjects = GetSaveLoadObjects();
                List<string> dataNames = new List<string>();
                foreach (ISaveLoad saveLoadObject in saveLoadObjects)
                {
                    string dataName = saveLoadObject.GetDataName();
                    if (dataNames.Contains(dataName))
                    {
                        OnSaveError.Invoke($"Save Collision Detected. Multiple Objects attempting to save using the same data name: {dataName}");
                        return true;
                    }
                    else
                    {
                        dataNames.Add(dataName);
                    }
                }
                return false;
            }

            // Goes through each game data object and invokes its save method
            public void SaveGame(string saveName)
            {
                // Do noting if the save name is not set / valid
                if (string.IsNullOrEmpty(saveName))
                {
                    OnSaveError.Invoke($"The current save name {saveName} is not a valid name");
                    return;
                }


                // Do a check to make sure there are no save collisions.
                if (SaveCollisionsDetected(saveName))
                {
                    return;
                }

                // Set the current save name to the game we are saving
                currentSaveName = saveName;

                // Trigger each object's save method
                List<ISaveLoad> saveLoadObjects = GetSaveLoadObjects();
                foreach (ISaveLoad saveLoadObject in saveLoadObjects)
                {
                    string errorMessage = saveLoadObject.Save(saveName);

                    // stop saving data if an error is detected
                    if (!string.IsNullOrEmpty(errorMessage))
                    {
                        OnSaveError.Invoke(errorMessage);
                        return;
                    }
                }
            }

            // Save each game data object using the current save file name we are using
            public void SaveGame()
            {
                SaveGame(currentSaveName);
            }

            // Goes through each game data object and invokes its load method
            public void LoadGame(string saveName)
            {
                if (SaveSystemUtilities.SaveExists(saveName))
                {
                    // Set the current save name to the game we are loading
                    currentSaveName = saveName;

                    // Trigger each object's load method
                    List<ISaveLoad> saveLoadObjects = GetSaveLoadObjects();
                    foreach (ISaveLoad saveLoadObject in saveLoadObjects)
                    {
                        string errorMessage = saveLoadObject.Load(saveName);

                        // stop loading data if an error is detected
                        if (!string.IsNullOrEmpty(errorMessage))
                        {
                            OnSaveError.Invoke(errorMessage);
                            return;
                        }
                    }
                }
                else
                {
                    OnLoadError.Invoke($"The save file {saveName} does not exist");
                }
            }

            // Goes through each game data object and invokes its reset method
            public void SetupNewGame(string saveName)
            {
                // Set the current save name to the game we are starting
                currentSaveName = saveName;

                // Do noting if the save name is not set / valid
                if (string.IsNullOrEmpty(saveName))
                {
                    OnStartGameError.Invoke($"The current save name {saveName} is not a valid name");
                    return;
                }

                // Trigger each object's reset method
                List<ISaveLoad> saveLoadObjects = GetSaveLoadObjects();
                foreach (ISaveLoad saveLoadObject in saveLoadObjects)
                {
                    string errorMessage = saveLoadObject.Reset();

                    // stop resetting data if an error is detected
                    if (!string.IsNullOrEmpty(errorMessage))
                    {
                        OnStartGameError.Invoke(errorMessage);
                        return;
                    }
                }

                // Save the game
                SaveGame();
            }

            public void DeleteGame(string saveName)
            {
                if (SaveSystemUtilities.SaveExists(saveName))
                {
                    SaveSystemUtilities.DeleteSave(saveName);
                }
            }

        }

Example
*******

Click to download :download:`ScriptableObjectSaveSystemExample.unitypackage </_downloads/ScriptableObjectSaveSystemExample.unitypackage>`.
