#########
Unity Ads
#########

Links
#####

*   `Unity Ads Documentation <https://docs.unity.com/ads/en-us/manual/UnityAdsHome>`_

Unity Ads Setup Log #1
######################

#.  `Link your Unity Project to a Unity Dashboard Project <https://docs.unity.com/ugs/en-us/manual/overview/manual/managing-unity-projects#ConfiguringProjectsForUGS>`_.

    ..  note::

        We had already done this when setting up unity authentication.

#.  Sign your project up for for Unity Ads Monetization product in https://cloud.unity.com/

    #.  Sign into https://cloud.unity.com/
    #.  Click on the **Products** tab on the left hand side of the screen.
    #.  Click on the **Unity Ads Monetization** product.
    #.  Click on the **Get Started** button or **Enable Ads** button and fill out your company's information.
    #.  Under the stp for Meditation partner I chose the following default options

        *   I plan to use Mediation
        *   Mediation Partner: Unity LevelPlay

    #.  Under the Project Info step for ad settings I selected the default option which was to start fresh.
    #.  Under the setup step I selected the default option of bidding
    #.  Under the store ID i indicated that My app is not live in an app store yet.
    #.  With all of my information filled out I then was presented IDS for different platforms along with a set of instructions
        I will document in the next steps

#   Follow the instructions in the `Unity Ads Mediation Integration Guide <https://docs.unity.com/ads/en-us/manual/ImplementingUnityAdsInMediation>`_.

    #.  Go to **Window > Package Manager**
    #.  Under the **Packages** Dropdown select **Unity Registry** and select the **Ads Mediation** package
    #.  Click the **Install** button.
    #.  Once the install is complete go to **Ads Mediation > Integration Manager**.
    #.  Click the **Update** button next to ironSource and press the **Import** button on the popup. You may have to
        do this multiple times until it is fully updated.

#.  `Initialize the SDK <https://docs.unity.com/ads/en-us/manual/InitializingTheUnitySDK>`_ in Unity

    #.  Create a script that will initialize the SDK early in the game's run time. Preferably when the game is launched.
    #.  The script is avaliable at https://docs.unity.com/ads/en-us/manual/InitializingTheUnitySDK Add the game IDs
        given to you earlier when signing up for the Unity Ads Monetization product on https://cloud.unity.com/

        ..  code-block::

            using UnityEngine;
            using UnityEngine.Advertisements;

            public class AdsInitializer : MonoBehaviour, IUnityAdsInitializationListener
            {
                [SerializeField] string _androidGameId;
                [SerializeField] string _iOSGameId;
                [SerializeField] bool _testMode = true;
                private string _gameId;

                void Awake()
                {
                    InitializeAds();
                }

                public void InitializeAds()
                {
                #if UNITY_IOS
                        _gameId = _iOSGameId;
                #elif UNITY_ANDROID
                        _gameId = _androidGameId;
                #elif UNITY_EDITOR
                        _gameId = _androidGameId; //Only for testing the functionality in the Editor
                #endif
                    if (!Advertisement.isInitialized && Advertisement.isSupported)
                    {
                        Advertisement.Initialize(_gameId, _testMode, this);
                    }
                }


                public void OnInitializationComplete()
                {
                    Debug.Log("Unity Ads initialization complete.");
                }

                public void OnInitializationFailed(UnityAdsInitializationError error, string message)
                {
                    Debug.Log($"Unity Ads Initialization Failed: {error.ToString()} - {message}");
                }
            }

#.  Refer to the documentation for `Implementing interstitial (full screen) Ads <https://docs.unity.com/ads/en-us/manual/ImplementingBasicAdsUnity>`_ in Unity
