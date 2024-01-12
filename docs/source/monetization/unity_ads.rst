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

#   Follow the instructions in the `Unity Editor LevelPlay integration <https://docs.unity.com/ads/en-us/manual/editor-levelplay-integration>`_.

    #.  Go to **Window > Package Manager**
    #.  Under the **Packages** Dropdown select **Unity Registry** and select the **Ads Mediation** package
    #.  Click the **Install** button.
    #.  Once the install is complete go to **Ads Mediation > Integration Manager**.
    #.  Click the **Update** button next to ironSource and press the **Import** button on the popup. You may have to
        do this multiple times until it is fully updated.
    #.  Install and Update the UnityAds adapter

#.  `Set Up Unity LevelPlay <https://developers.is.com/ironsource-mobile/general/move-to-unity-levelplay/>`_

    #.  Create an ironSource account at https://platform.ironsrc.com/partners/identity/signup
    #.  On your ironSource homepage click the **Add App** button.
    #.  Enter your app's information.
    #.  Enable add units (like Interstitial ads) that you want to display.
    #.  If your app is on multiple platforms create a new app for each platform.
    #.  Sign into https://cloud.unity.com/
    #.  Click on the **Products** tab on the left hand side of the screen.
    #.  Click on the **Unity Ads Monetization** product.
    #.  Under **Setup > API Management** Generate your Level Play Service Account API Key and Monetization Stats API Access. Also take
        note of your Organization Core ID found under **Setup > Organization Settings**.
    #.  On IronSource navigate to **Setup > SDK networks** and add the Unity Ads network.
    #.  When setting up unity ads enter information for the API Key (Monetization Stats API) and enter organization
        Core ID. Make sure to enable Unity bidder auto setup which requires the Level Play Service Account API key and secret key
        you generated.
    #.  For each app make sure to go to **Settings > SDK Networks** and under Unity Ads setup your add placements
        (you will need the App Store Game IDS found in the unity cloud monetization product under **Settings > Game IDs** and your Placement IDs which are found
        found in the unity cloud monetization product under **Placements**)

#.  `Initialize the SDK <https://docs.unity.com/ads/en-us/manual/InitializingTheUnitySDK>`_ in Unity

    #.  Create a script that will initialize the SDK early in the game's run time. Preferably when the game is launched.
    #.  The script is avaliable at https://docs.unity.com/ads/en-us/manual/InitializingTheUnitySDK Add the game IDs
        given to you earlier when signing up for the Unity Ads Monetization product on https://cloud.unity.com/

        ..  code-block:: c#

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

#.  `Integrate Ads On IOS <https://docs.unity.com/ads/en-us/manual/iOSDeveloperIntegrations>`_

    #.  Open your UnityProject's .xcworkspace file
    #.  Click the **Pods** xcode project file and select the Podfile
    #.  Inside the podfile add the line ``pod 'UnityAds'``. See below for an example

        ..  code-block:: c#

            source 'https://github.com/CocoaPods/Specs'
            source 'https://github.com/CocoaPods/Specs.git'
            platform :ios, '12.0'

            target 'UnityFramework' do
              pod 'IronSourceSDK', '7.7.0.0'
              pod 'UnityAds'
            end
            target 'Unity-iPhone' do
            end
            use_frameworks!
    #.  Afterwards open the terminal and navigate to the directory that holds the podfile. Then run the command
        ``pod install``

#.  Test Ads On Devices

    #.  Sign into https://cloud.unity.com/
    #.  Click on the **Products** tab on the left hand side of the screen.
    #.  Click on the **Unity Ads Monetization** product.
    #.  Click the **Testing** section
    #.  Under the test mode section, click the **Add Test Device** button and fill out the device information.
        Refer to https://docs.unity.com/monetization-dashboard/en-us/manual/TestDevices
        to determine the Advertising ID for your device.

Potential Errors
################

*   Xcode build Error

    .. error::

        'IronSource/IronSource.h' file not found

    To fix this try:

    *   If you have integrated unity ads go to **Ads Mediation > Integration Manager**. In the the ironSource
        row click the update button.
    *   Go to https://developers.is.com/ironsource-mobile/unity/unity-plugin/#step-5. and download
        the IronSource.framework files. There should be instructions on the site on how to add these files to your
        project. for me I downloaded and added IronSource.framework into /Assets/Plugins/iOS
    *   When opening the project in xcode use the .xcworkspace file in Xcode, not the .xcodeproj file. if you're working
        on a project that uses CocoaPods or has multiple related sub-projects, you'll typically be working with an
        .xcworkspace. If you're working on a standalone project, you'll be using an .xcodeproj.
    *   Try cleaning your project (Product -> Clean Build Folder) and then rebuilding it.
    *   Update MacOS and Xcode

*   Add Load Error

    ..  error::

        Error loading Ad Unit: Interstitial_iOS - INVALID_ARGUMENT - adMarkup is missing; objectId is missing

    ..  error::

        E/UnityAds: +[USRVApiSdk WebViewExposed_logError:callback:] (line:63) :: Header bidding load invocation failed: adMarkup is missing; objectId is missing

    To fix this try:

    *   In **Project Settings > Services > Ads** Make sure Ads are switched on.


*   Duplicate Class Build Error

    ..  error::

        Configure project :launcher WARNING: The option setting 'android.enableR8=true' is deprecated. It will be removed in version 5.0 of the Android Gradle plugin. You will no longer be able to disable R8
        Task :unityLibrary:preBuild UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:preBuild UP-TO-DATE Task :launcher:preBuild UP-TO-DATE Task :unityLibrary:IronSource.androidlib:preBuild UP-TO-DATE Task :unityLibrary:IronSource.plugin:preBuild UP-TO-DATE Task :unityLibrary:preReleaseBuild UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:preReleaseBuild UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:packageReleaseRenderscript NO-SOURCE Task :launcher:extractProguardFiles UP-TO-DATE Task :unityLibrary:IronSource.plugin:preReleaseBuild UP-TO-DATE Task :unityLibrary:IronSource.androidlib:preReleaseBuild UP-TO-DATE Task :launcher:preReleaseBuild UP-TO-DATE Task :unityLibrary:packageReleaseRenderscript NO-SOURCE Task :unityLibrary:IronSource.androidlib:packageReleaseRenderscript NO-SOURCE Task :unityLibrary:IronSource.plugin:packageReleaseRenderscript NO-SOURCE Task :unityLibrary:GooglePlayGamesManifest.androidlib:compileReleaseRenderscript NO-SOURCE Task :unityLibrary:IronSource.plugin:compileReleaseRenderscript NO-SOURCE Task :unityLibrary:compileReleaseRenderscript NO-SOURCE Task :launcher:compileReleaseRenderscript NO-SOURCE Task :unityLibrary:IronSource.androidlib:compileReleaseRenderscript NO-SOURCE Task :unityLibrary:generateReleaseResValues UP-TO-DATE Task :launcher:generateReleaseResValues UP-TO-DATE Task :launcher:generateReleaseResources UP-TO-DATE Task :unityLibrary:generateReleaseResources UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:generateReleaseResValues UP-TO-DATE Task :unityLibrary:IronSource.plugin:generateReleaseResValues UP-TO-DATE Task :unityLibrary:IronSource.androidlib:generateReleaseResValues UP-TO-DATE Task :unityLibrary:IronSource.androidlib:generateReleaseResources UP-TO-DATE Task :unityLibrary:IronSource.plugin:generateReleaseResources UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:generateReleaseResources UP-TO-DATE Task :launcher:createReleaseCompatibleScreenManifests UP-TO-DATE Task :unityLibrary:packageReleaseResources UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:packageReleaseResources UP-TO-DATE Task :unityLibrary:IronSource.androidlib:packageReleaseResources UP-TO-DATE Task :launcher:extractDeepLinksRelease UP-TO-DATE Task :unityLibrary:IronSource.plugin:packageReleaseResources UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:extractDeepLinksRelease UP-TO-DATE Task :unityLibrary:extractDeepLinksRelease UP-TO-DATE Task :unityLibrary:IronSource.androidlib:extractDeepLinksRelease UP-TO-DATE Task :unityLibrary:processReleaseManifest UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:processReleaseManifest UP-TO-DATE Task :unityLibrary:IronSource.plugin:extractDeepLinksRelease UP-TO-DATE Task :unityLibrary:IronSource.androidlib:processReleaseManifest UP-TO-DATE Task :unityLibrary:IronSource.plugin:processReleaseManifest UP-TO-DATE Task :unityLibrary:compileReleaseLibraryResources UP-TO-DATE Task :unityLibrary:IronSource.androidlib:compileReleaseLibraryResources UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:compileReleaseLibraryResources UP-TO-DATE Task :unityLibrary:IronSource.plugin:compileReleaseLibraryResources UP-TO-DATE Task :unityLibrary:mergeReleaseShaders UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:mergeReleaseShaders UP-TO-DATE Task :unityLibrary:IronSource.androidlib:mergeReleaseShaders UP-TO-DATE Task :unityLibrary:IronSource.plugin:mergeReleaseShaders UP-TO-DATE Task :unityLibrary:IronSource.androidlib:compileReleaseShaders NO-SOURCE Task :unityLibrary:compileReleaseShaders NO-SOURCE Task :unityLibrary:generateReleaseAssets UP-TO-DATE Task :unityLibrary:IronSource.androidlib:generateReleaseAssets UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:compileReleaseShaders NO-SOURCE Task :unityLibrary:GooglePlayGamesManifest.androidlib:generateReleaseAssets UP-TO-DATE Task :unityLibrary:IronSource.plugin:compileReleaseShaders NO-SOURCE Task :unityLibrary:IronSource.androidlib:packageReleaseAssets UP-TO-DATE Task :unityLibrary:IronSource.plugin:generateReleaseAssets UP-TO-DATE Task :unityLibrary:IronSource.androidlib:compileReleaseAidl NO-SOURCE Task :unityLibrary:GooglePlayGamesManifest.androidlib:packageReleaseAssets UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:compileReleaseAidl NO-SOURCE Task :unityLibrary:IronSource.plugin:packageReleaseAssets UP-TO-DATE Task :unityLibrary:IronSource.plugin:compileReleaseAidl NO-SOURCE Task :unityLibrary:GooglePlayGamesManifest.androidlib:parseReleaseLocalResources UP-TO-DATE Task :unityLibrary:IronSource.androidlib:parseReleaseLocalResources UP-TO-DATE Task :unityLibrary:IronSource.plugin:parseReleaseLocalResources UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:generateReleaseRFile UP-TO-DATE Task :unityLibrary:IronSource.androidlib:generateReleaseRFile UP-TO-DATE Task :unityLibrary:IronSource.plugin:generateReleaseRFile UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:generateReleaseBuildConfig UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:javaPreCompileRelease UP-TO-DATE Task :unityLibrary:IronSource.androidlib:generateReleaseBuildConfig UP-TO-DATE Task :unityLibrary:IronSource.androidlib:javaPreCompileRelease UP-TO-DATE Task :unityLibrary:IronSource.plugin:generateReleaseBuildConfig UP-TO-DATE Task :unityLibrary:IronSource.plugin:javaPreCompileRelease UP-TO-DATE Task :unityLibrary:IronSource.androidlib:compileReleaseJavaWithJavac UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:compileReleaseJavaWithJavac UP-TO-DATE Task :unityLibrary:IronSource.androidlib:bundleLibCompileToJarRelease UP-TO-DATE Task :unityLibrary:IronSource.androidlib:mergeReleaseGeneratedProguardFiles UP-TO-DATE Task :unityLibrary:IronSource.androidlib:exportReleaseConsumerProguardFiles UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:bundleLibCompileToJarRelease UP-TO-DATE Task :unityLibrary:IronSource.plugin:compileReleaseJavaWithJavac UP-TO-DATE Task :unityLibrary:IronSource.plugin:bundleLibCompileToJarRelease UP-TO-DATE Task :unityLibrary:IronSource.plugin:mergeReleaseGeneratedProguardFiles UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:mergeReleaseGeneratedProguardFiles UP-TO-DATE Task :unityLibrary:IronSource.plugin:exportReleaseConsumerProguardFiles UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:exportReleaseConsumerProguardFiles UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:processReleaseJavaRes NO-SOURCE Task :unityLibrary:GooglePlayGamesManifest.androidlib:bundleLibResRelease NO-SOURCE Task :unityLibrary:IronSource.androidlib:processReleaseJavaRes NO-SOURCE Task :unityLibrary:IronSource.plugin:processReleaseJavaRes NO-SOURCE Task :unityLibrary:IronSource.plugin:bundleLibResRelease NO-SOURCE Task :unityLibrary:GooglePlayGamesManifest.androidlib:bundleLibRuntimeToJarRelease UP-TO-DATE Task :unityLibrary:IronSource.androidlib:bundleLibResRelease NO-SOURCE Task :unityLibrary:IronSource.androidlib:bundleLibRuntimeToJarRelease UP-TO-DATE Task :unityLibrary:IronSource.plugin:bundleLibRuntimeToJarRelease UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:mergeReleaseJniLibFolders UP-TO-DATE Task :unityLibrary:IronSource.androidlib:mergeReleaseJniLibFolders UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:mergeReleaseNativeLibs UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:stripReleaseDebugSymbols NO-SOURCE Task :unityLibrary:IronSource.androidlib:mergeReleaseNativeLibs UP-TO-DATE Task :unityLibrary:GooglePlayGamesManifest.androidlib:copyReleaseJniLibsProjectOnly UP-TO-DATE Task :unityLibrary:IronSource.androidlib:stripReleaseDebugSymbols NO-SOURCE Task :unityLibrary:IronSource.plugin:mergeReleaseJniLibFolders UP-TO-DATE Task :unityLibrary:IronSource.androidlib:copyReleaseJniLibsProjectOnly UP-TO-DATE Task :unityLibrary:IronSource.plugin:mergeReleaseNativeLibs UP-TO-DATE Task :unityLibrary:IronSource.plugin:stripReleaseDebugSymbols NO-SOURCE Task :unityLibrary:IronSource.plugin:copyReleaseJniLibsProjectOnly UP-TO-DATE Task :unityLibrary:packageReleaseAssets Task :unityLibrary:compileReleaseAidl NO-SOURCE Task :unityLibrary:generateReleaseBuildConfig UP-TO-DATE Task :unityLibrary:parseReleaseLocalResources UP-TO-DATE Task :unityLibrary:generateReleaseRFile UP-TO-DATE Task :unityLibrary:javaPreCompileRelease UP-TO-DATE Task :launcher:processReleaseManifest Task :launcher:mergeReleaseShaders UP-TO-DATE Task :launcher:compileReleaseShaders NO-SOURCE Task :launcher:generateReleaseAssets UP-TO-DATE Task :launcher:mergeReleaseAssets Task :launcher:checkReleaseDuplicateClasses FAILED Task :launcher:mergeReleaseResources

    ..  error::

        Note: C:\UnityProjects\TunnelTwisterV3\Library\Bee\Android\Prj\IL2CPP\Gradle\unityLibrary\src\main\java\com\unity3d\player\UnityPlayerActivity.java uses or overrides a deprecated API. Note: Recompile with -Xlint:deprecation for details.
        FAILURE: Build failed with an exception.
        •	What went wrong: Execution failed for task ':launcher:checkReleaseDuplicateClasses'.
        1 exception was raised by workers: java.lang.RuntimeException: Duplicate class com.ironsource.unity.androidbridge.AndroidBridge found in modules IronSource-bridge.jar (IronSource-bridge.jar) and android-bridge.jar (android-bridge.jar) Duplicate class com.ironsource.unity.androidbridge.AndroidBridge$1 found in modules IronSource-bridge.jar (IronSource-bridge.jar) and android-bridge.jar (android-bridge.jar) Duplicate class com.ironsource.unity.androidbridge.AndroidBridge$2 found in modules IronSource-bridge.jar (IronSource-bridge.jar) and android-bridge.jar (android-bridge.jar) Duplicate class com.ironsource.unity.androidbridge.AndroidBridge$3 found in modules IronSource-bridge.jar (IronSource-bridge.jar) and android-bridge.jar (android-bridge.jar) Duplicate class com.ironsource.unity.androidbridge.AndroidBridge$4 found in modules IronSource-bridge.jar (IronSource-bridge.jar) and android-bridge.jar (android-bridge.jar) Duplicate class com.ironsource.unity.androidbridge.AndroidBridge$5 found in modules IronSource-bridge.jar (IronSource-bridge.jar) and android-bridge.jar (android-bridge.jar)

    The solution was found at https://forum.unity.com/threads/gradle-build-failed-duplicate-classes-ironsource.1506746/

    #.  Delete the IronSource folder from my Assets Folder
    #.  Go to the ironsource website (https://developers.is.com/ironsource-mobile/unity/unity-plugin/#step-1) and download the latest unity package.
    #.  In unity go to **Assets > Import Package > Custom Pacckage** And import the ironsource package