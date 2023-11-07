###########
Game Center
###########

Links
#####

*   `Unity Game Center Sign In Documentation <https://docs.unity.com/ugs/en-us/manual/authentication/manual/platform-signin-apple-game-center>`_
*   `Enable / Configure Game Center On XCode <https://developer.apple.com/documentation/gamekit/enabling_and_configuring_game_center/>`_
*   `Resolve Bugs With Apple UnityPackage <https://forum.unity.com/threads/unity-apple-plugin-issue.1462814/>`_

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




