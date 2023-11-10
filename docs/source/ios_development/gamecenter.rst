###########
Game Center
###########

Links
#####

*   `Unity Game Center Sign In Documentation <https://docs.unity.com/ugs/en-us/manual/authentication/manual/platform-signin-apple-game-center>`_
*   `Enable / Configure Game Center On XCode <https://developer.apple.com/documentation/gamekit/enabling_and_configuring_game_center/>`_
*   `Resolve Bugs With Apple UnityPackage <https://forum.unity.com/threads/unity-apple-plugin-issue.1462814/>`_
*   `Apple Game Center - Informal Doc <https://docs.google.com/document/d/18IfxMcaYCoCHgFrMmM4gfGCHcKKnYx9iCr6DFBU-nLg/edit#heading=h.nh5j6ob4nbj3>`_

How To Setup Game Center Login
##############################

..  note::

    This setup was done with:

    *   Unity Version 2021.3.32f1
    *   Authentication Package Version 2.7.2

#.  Follow the `Unity Get Started Documentation <https://docs.unity.com/ugs/en-us/manual/authentication/manual/get-started>`_:

    #.  Sign up for `Unity Gaming Services <https://unity.com/solutions/gaming-services>`_
    #.  Link your project to the service within the editor by going to **Edit > Project Settings**, clicking the **Services**
        row. I made a project within the Unity Gaming Services website so i just linked the existing project.
    #.  Install the SDK by going to **Window > Package Manager**. Select the **Unity Registry** dropdown and select
        the **Authentication** package. Make sure it's version is greater than or equal to 2.4.0. Otherwise you
        will need to upgrade your unity version to get access to a higher package version.
    #.  In your unity project, make sure when the app starts to run you initialize the Unity Services SDK.
        by calling ``await UnityServices.InitializeAsync();``. See the `UGS Manual <https://docs.unity.com/ugs/manual/overview/manual/getting-started#InitializingUGS>`_ for the full code snippet.

#.  Follow the Unity `Apple Game Center Documentation <https://docs.unity.com/ugs/en-us/manual/authentication/manual/platform-signin-apple-game-center>`_

    #.  Install the `Apple Core & Game Kit Unity Plugins <https://github.com/apple/unityplugins>`_
    #.  If you want to include these packages in your version control system, I suggest moving the
        generated .tgz files within the Unity Project's **Packages** directory. Then when you add the packages
        using the package manager's **Add Package From Tarball** method, it will store the relative
        paths to those files.
    #.  Note I made the apple core package a custom package so that I could modify some of the c# files to make game center work.
        To make a package custom in unity simply navigate to your Unity Project directory, go to
        **Library / Package Cache**, identify the package of interest (has a similar name), and drag it into
        the **Packages** folder. For more information see `How can I modify built-in packages? <https://support.unity.com/hc/en-us/articles/9113460764052-How-can-I-modify-built-in-packages->`_
    #.  Next add Apple Game Center as an ID provider for Unity by going to `Unity Gaming Services <https://unity.com/solutions/gaming-services>`_.
        There select your project, scroll down to services and select **Player Authentication**. Click the **Launch**
        button and add **Apple Game Center** as a provider. Make sure to add the bundle identifier of your app
        (you should see it on Xcode under the **General** tab in the **Identity** section).
    #.  Next include the ``AppleGameCenterExampleScript`` provided on `Apple Game Center Documentation <https://docs.unity.com/ugs/en-us/manual/authentication/manual/platform-signin-apple-game-center>`_ page
        and make sure to add and call the ``SignInWithAppleGameCenterAsync`` function when your app loads.

#.  Follow `Apple's Guide to Enabling Game Center <https://developer.apple.com/documentation/gamekit/enabling_and_configuring_game_center/>`_

    #.  Go to the Signing and Capabilities tab in Xcode, Click the **+ Capability** button and double click GameCenter

#.  For some reason Apple will not recognize Game Center with your app unless you add 1 leaderboard to it.
    (See `this forum post <https://stackoverflow.com/questions/34055758/ios9-this-game-is-not-recognized-by-game-center>`_ for more information)

    #.  See this guide to `Configure leaderboards in App Store Connect <https://developer.apple.com/help/app-store-connect/configure-game-center/configure-leaderboards/>`_
    #.  For me, on `App Store Connect <https://appstoreconnect.apple.com/login>`_:

        *   I selected my app
        *   I selected the **Services** tab
        *   I clicked the **Game Center** Row
        *   I scrolled down to **Leaderboards** and I clicked the blue plus button to add a new leaderboard.

#.  When I tried to build the app to IOS, I encountered the following build errors:

    ..  error::

        Building for 'iOS', but linking in dylib (/Users/jeffreyspitz/UnityProjects/TunnelTwisterV3/Builds/iOSBuild/Frameworks/com.apple.unityplugin.core/Plugins/tvOS/AppleCoreNative.framework/AppleCoreNative) built for 'tvOS'

    My solution for this this is to do the following:

    #.  Make both the apple core package a and apple gamekit package custom (If you have not done so already). To start
        in your unity project files to **Library / Package Cache**, identify the package of interest (has a similar name), and drag it into
        the **Packages** folder. For more information see `How can I modify built-in packages? <https://support.unity.com/hc/en-us/articles/9113460764052-How-can-I-modify-built-in-packages->`_
    #.  Inside the UnityEditor in the project window navigate to **Packages > Apple.Core > Plugins > tvOS**. Select
        The **AppleCoreNative** plugin file and under its import settings in the inspector select Editor. This way we don't
        have it building to ios.
    #.  Netxt we repeat the same process for the GameKit package.
        Inside the UnityEditor in the project window navigate to **Packages > Apple.GameKit > Plugins > tvOS**. Select
        The **AppleCoreNative** plugin file and under its import settings in the inspector select Editor. This way we don't
        have it building to ios.

#.  When I tried to run the app to IOS, I also encountered the following error:

    ..  error::

        dyld[20195]: missing symbol called

    And this error occured when encountering the function GKLocalPlayer_GetLocal (when calling GKLocalPlayer.Local.FetchItems() from the
    gamekit package. It turns out there was a `forum post <https://forum.unity.com/threads/gklocalplayer-local-fetchitems-error-on-unity.1395694/>`_
    with other people facing the same issue. There was a `Google Doc <https://docs.google.com/document/d/18IfxMcaYCoCHgFrMmM4gfGCHcKKnYx9iCr6DFBU-nLg/edit#heading=h.nh5j6ob4nbj3>`_ posted on Oct 17 2023 by a member of Unity Technologies
    about a workaround for the issue. After looking at the document I did the following to fix the bug:

    #.  I cloned the apple unity plugins repo inside my Packages folder in my unity project.
    #.  I did not edit the unity plugins repo and simply built all packages using the standard ``python3 build.py`` command.
    #.  I added the tarball files of core and gamekit through the package manager window and then I repeated the step
        above where i made the packages custom and targeted the tvOS plugins to the editor.
    #.  I completed the step below where I added a code fix to AppleFrameworkUtility.cs script's "GetPluginLibraryPathForBuildTarget" method
    #.  I Modified the GKLocalPlayer script as outlined in the Google Doc.
    #.  I checked to make sure GameCenter was enabled as part of signing and capabilities in XCode.

#.  If after you build your app to your iphone and you encounter errors like package files not being found when trying
    to connect to game center try out the following:

    *   I found this post on the forums helpful: `Unity Apple plugin Issue <https://forum.unity.com/threads/unity-apple-plugin-issue.1462814/>`_.
    *   Essentially go to AppleFrameworkUtility.cs script's "GetPluginLibraryPathForBuildTarget" method and
        add the following lines of code. (`Github reference <https://github.com/makeplayhappy/appleunityplugins/blob/find_framework_fix/plug-ins/Apple.Core/Apple.Core_Unity/Assets/Apple.Core/Editor/AppleFrameworkUtility.cs>`_)

    ..  code-block:: c#

        // try without the .framework, Unity.2022 AssetDatabase.FindAssets fails with ".frameworks"
        if( libraryName.EndsWith(".framework") )
        {
            string libraryNameWithoutFramework = libraryName.Substring( 0, libraryName.LastIndexOf(".framework") );
            results = AssetDatabase.FindAssets(libraryNameWithoutFramework);
            foreach (string currGUID in results)
            {
                string libraryPath = AssetDatabase.GUIDToAssetPath(currGUID);
                string[] folders = libraryPath.Split('/');
                if (Array.IndexOf(folders, platformString) > -1)
                {
                    return libraryPath;
                }
            }

        }




