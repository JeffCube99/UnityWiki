#################
Google Play Games
#################

Links
#####

*   `Unity Google Play Games Sign In Documentation <https://docs.unity.com/ugs/en-us/manual/authentication/manual/platform-signin-google-play-games>`_


Google Play Games Login Setup Log #1
####################################

..  note::

    This setup was done with:

    *   Unity Version 2021.3.32f1

#.  Follow the `Unity Get Started Documentation <https://docs.unity.com/ugs/en-us/manual/authentication/manual/get-started>`_:

    #.  Sign up for `Unity Gaming Services <https://unity.com/solutions/gaming-services>`_. Make sure you lauch the
        Authentication Service for your app. Sign up for the Apple Game Center identity provider and MAKE SURE
        THE STATUS ON THE PROVIDER IS ENABLED!
    #.  Link your project to the service within the editor by going to **Edit > Project Settings**, clicking the **Services**
        row. I made a project within the Unity Gaming Services website so i just linked the existing project.
    #.  Install the SDK by going to **Window > Package Manager**. Select the **Unity Registry** dropdown and select
        the **Authentication** package. Make sure it's version is greater than or equal to 2.4.0. Otherwise you
        will need to upgrade your unity version to get access to a higher package version.
    #.  In your unity project, make sure when the app starts to run you initialize the Unity Services SDK.
        by calling ``await UnityServices.InitializeAsync();``. See the `UGS Manual <https://docs.unity.com/ugs/manual/overview/manual/getting-started#InitializingUGS>`_ for the full code snippet.

#.  Follow the `Unity Google Play Games Sign In Documentation <https://docs.unity.com/ugs/en-us/manual/authentication/manual/platform-signin-google-play-games>`_

    #.  Download the `Google Play Games Plugin for Unity <https://github.com/playgameservices/play-games-plugin-for-unity/tree/master/current-build>`_.
    #.  To import the package, in the unity editor go to **Assets > Import Package > Custom Package** and select the package file. After
        installation, the package will prompt you to enable or disable **Android Auto Resolution**. I opted to enable this.
    #.  Sign into `Google Play Console <https://play.google.com/console/u/0/signup>`_, and follow the instructions for how
        `to configure your game for Google Play Games login <https://developers.google.com/games/services/console/enabling>`_.
        For me this involved the following:

        #.  In the google play console homepage i scrolled down to the Apps section and
            selected my app.
        #.  On the left hand side of the screen scroll down to the **Grow** section. Under it
            select **Play Games Services > Setup and Management > Configuration**
        #.  On the Play Games Services setup page I selected the option to **Create new Play Game Services project**.
            I did not have an existing cloud project at the time so i clicked the **Create a new cloud project** button. This
            gave me instructions on how to do so. for me this was the following:

            #.  Navigate to `Google Cloud Console <https://console.cloud.google.com/projectcreate>`_
            #.  Create a new project with a name and organization (if you have one)
            #.  Go back to Google Play Console, refresh the cloud projects list by clicking the **Refresh cloud projects**
                button, and select your new google cloud project.

        #.  After selecting my newly created cloud project I clicked the **Use** button.
        #.  Scrolling down on the Play Games Services Configuration page, I went to the Properties
            section and clicked on **Edit Properties**. For testing you only need to enter the display name but
            you can fill out other properties if you like
        #.  Afterwads on the Play Games Services Configuration page I was presented
            with a checklist of action items to complete.
        #.  To continue I clicked on the Create OAuth consent screen step. and followed the instructions:

            #.  On the google cloud page for my app I selected the APIs & Services tab on the left side of the page and selected
                the OAuth consent screen.
            #.  On the page i selected External user type and clicked the **Create** button.
                Afterwards i followed the prompts and filled in the relevant information fields.
            #.  On the scopes portion of the registration, I made sure to include games, games_lite, and
                drive.appdata
            #.  On the Test users section, I added users that were current testers.

        #.  To continue with the service configuration process I scrolled down to the credentials section
            and clicked the **Add credential** button. For my credentials i selected the Android type. I then
            cliccked the **Create OAuth client** button which gave me instructions on how to do so the instructions
            page also gave me the details i needed to complete the form.

            #.  On my app's Google Cloud Platform page on the APIs & Services page i clicked on the
                **Credentials** row and clicked the **Create Credentials** button and selected the OAuth client ID
                option.
            #.  I then filled in the app information that was presented to me in the instructions page on google play
                console.

                ..  note::

                    If you use the Play App Signing service, confirm the fingerprint presented is the one actually in use
                    by going to https://play.google.com/console and scrolling down to the Setup **App Signing** section. If you do not use
                    this service you need to run the command ``keytool -keystore path-to-debug-or-production-keystore -list -v``
                    to get the SHA1 certificate fingerprint of the keystore you use to sign your app. To use the ``keytool``
                    command you need to install JDK by following the steps in `Oracle's installation guide <https://docs.oracle.com/en/java/javase/18/install/installation-jdk-microsoft-windows-platforms.html>`_

                Afterwards I clicked the **Create** button.

        #.  Once these steps were done I was able to select the OAuth client i just created in
            google play console and I clicked on the **Save Changes** button.
        #.  To continue with the service configuration process I had to add the play games services SDK
            to my APK to use the APIs. To do this I followed instructions found on
            `this (OLD) Google Play Game Services Page <https://developers.google.com/games/services/v1/android/quickstart>`_.
            For my app I did the follwing

                ..  important::::

                    Looking back the google play plugin works with the latest version of the play games service.
                    we should have not used the old Play Game Services help page, but the latest version of the play games services
                    help page found here: https://developers.google.com/games/services/android/quickstart. If you use this replace
                    the following instructions with the ones you find there.

            #.  In the unity editor I went to **Edit > Project Settings > Player**.
            #.  Under Publishing Settings, i checked the box next to **Custom Main Gradle Template**
            #.  This created a file under **Assets\Plugins\Android\mainTemplate.gradle**. I then opened
                this file and edited it to add the following lines of code to the top of the file

                ..  code-block::

                      buildscript {
                        repositories {
                          google()
                          mavenCentral()
                        }
                      }

                      allprojects {
                        repositories {
                          google()
                          mavenCentral()
                        }
                      }

            #.  Under the dependencies section of mainTemplate.gradle I added the following lines

                ..  code-block::

                    implementation 'com.google.android.gms:play-services-games:23.1.0'


        #.  After the last step, I navigated back to my apps Google Play Console page. I then went to
            **Play Games Services > Setup and management > Leaderboards**
        #.  From here I clicked the **Create Leaderboard** button and filled out the relevant information for
            each leaderboard I wanted to create. At the end of the form i clicked **Save as draft**
        #.  After configuring the leaderboards, On the left hand side of Google Play Console I went to **Play Games Services > Setup and management > Testers**
            to add the emails of all my testers. Because i halready had testers on the internal track, under the **Release Tracks**
            section, I just added my internal testers.
        #.  At this point the app now has access to use google play services.
            You do not need to publish. For more information about this visit `this information page <https://developers.google.com/games/services/console/testpub>`_

    #.  With google play console setup online we return to setting up the `Play Games Services <https://github.com/playgameservices/play-games-plugin-for-unity#configure-your-game>`_
        plugin.

        #.  On Google Play Console page. I then went to **Play Games Services > Setup and management > Leaderboards**.
            There I clicked the **Get resources** button and selected the **Android (XML)** tab. I copied the XML to the clipboard.
        #.  In unity I went to **Window > Google Play Games > Setup > Android Setup** and pasted the XML under the resources
            definition section. Then I clicked the **Setup** Button.

    #.  We opted not to setup a Web App Client ID since it is not required to submit high scores and access
        Google Play Games.

Potential Errors
################

*   Android Build Error

    .. error::

        Duplicate dependencies of com.google.android.gms:play-services-games-v2 and com.google.android.gms:play-services-games:23.1.0 clash
        with each other

    To fix this try:

    *   Go to the gradle template file **Assets\Plugins\Android\mainTemplate.gradle** and under dependencies
        include the following line

    ..  code-block::

        dependencies {
            ...
            implementation "com.google.android.gms:play-services-games-v2:+"
            ...
        }

*   Android Java Exception

    ..  error::

        AndroidJavaException: java.lang.ClassNotFoundException: com.google.android.gms.games.PlayGames java.lang.ClassNotFoundException: com.google.android.gms.games.PlayGames at java.lang.Class.classForName(Native Method) at java.lang.Class.forName(Class.java:454) at com.unity3d.player.UnityPlayer.nativeRender(Native Method) at com.unity3d.player.UnityPlayer.access$500(Unknown Source:1) at com.unity3d.player.UnityPlayer$e$1.handleMessage(Unknown Source:115) at android.os.Handler.dispatchMessage(Handler.java:102) at android.os.Looper.loopOnce(Looper.java:201) at android.os.Looper.loop(Looper.java:288) at com.unity3d.player.UnityPlayer$e.run(Unknown Source:21) Caused by: java.lang.ClassNotFoundException: com.google.android.gms.games.PlayGames at java.lang.Class.classForName(Native Method)  at java.lang.Class.forName(Class.java:454)  at com.unity3d.player.UnityPlayer.nativeRender(Native Method)  at com.unity3d.player.UnityPlayer.access$500(Unknown Source:1)  at com.unity3d.player.UnityPlayer$e$1.handleMessage(Unknown Source:115)  at android.os.Handler.dispatchMessage(Handler.java:102)  at android.os.Looper.loopOnce(Looper.java:201)  at android.os.Looper.loop(Looper.java:288)  at com.unity3d.player.UnityPlayer$e.run(Unknown Source:21)  at UnityEngine.AndroidJNISafe.CheckException () [0x00000] in <00000000000000000000000000000000>:0 at UnityEngine.AndroidJNISafe.FindClass (System.String name) [0x00000] in <00000000000000000000000000000000>:0 at UnityEngine.AndroidJavaClass._AndroidJ

    To fix this try:

    #.  Go to **Edit>Project Settings>Player**
    #.  Under the android dropdown go to **Publishing Settings** And check the box for Custom Proguard File.
        This should add a proguard file to **Assets\Plugins\proguard-user.txt**
    #.  Go to **Assets\GooglePlayGames\com.google.play.games\Proguard\games.txt** and copy the text into **Assets\Plugins\proguard-user.txt**



*   App Not Correctly Configured to Use Google Play games services

    ..  error::

        **** APP NOT CORRECTLY CONFIGURED TO USE GOOGLE PLAY GAME SERVICES
        **** DEVELOPER_ERROR
        **** This is usually caused by one of these reasons:
        **** (1) Your package name and certificate fingerprint do not match
        ****     the client ID you registered in Developer Console.
        **** (2) Your App ID was incorrectly entered.
        **** (3) Your game settings have not been published and you are
        ****     trying to log in with an account that is not listed as
        ****     a test account.
        **** (4) A server auth code was requested, but an incorrect client
        ****     id was provided. The client id for server auth codes should
        ****     be the client id for the game server (not the android app).
        ****
        **** To help you debug, here is the information about this app
        **** Package name         : com.JeffCubeGames.TunnelTwister
        **** Cert SHA1 fingerprint: 6B:A6:6E:AB:C0:EB:85:C7:F7:94:99:A6:BA:D4:AF:49:5E:7D:05:87
        **** App ID from manifest : 55047623714
        ****
        **** Check that the above information matches your setup in
        **** Developer Console. Also, check that you're logging in with the
        **** right account (it should be listed in the Testers section if
        **** your project is not yet published).
        ****
        **** For more information, refer to the troubleshooting guide:
        ****   http://developers.google.com/games/services/android/troubleshooting
        ****

    To fix this I did the following:

    #.  Check package name and certificate fingerprint:

        #.  In unity go to **File > Build Settings > Player Settings**
        #.  Go to the Android tab and scroll down to **Other Settings > Identification** There you should find the package
            name.
        #.  To compare with the package name you registered in Developer console, sign into https://play.google.com/console,
            select your application. Under the application name you will see the package name. click the **App Integrity** section on the left hand side
        #.  Next while still in **Player Settings** Scroll to **Publishing Settings**. Under the **Keystore** section
            you will see the path to the keystore file unity uses to sign the android application.
        #.  If you used the google play app signing service, to view your certificate fingerprint, sign into https://play.google.com/console,
            select your application. Click the **App Integrity** section on the left hand side. Next to the Play App Signing
            section click the **Settings** button. Scroll down to see the SHA1 certificate fingerprint in use.
        #.  Next to compare your certificate fingerprint to the one used by google cloud services, go to https://console.cloud.google.com/.
            Under **APIs & Services** section click **Credentials**. Select the credentials you use for your app and there you will find the
            SHA-1 certificate fingerprint. Note that if there is a difference between the fingerprint on the cloud service and the
            one displayed by play console, you should copy the one from play console into the google cloud credentials.