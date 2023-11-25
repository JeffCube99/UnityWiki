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

                    Google provides you a dummy fingerprint value. You need to run the command ``keytool -keystore path-to-debug-or-production-keystore -list -v``
                    to get the SHA1 certificate fingerprint of the keystore you use to sign your app. To use the ``keytool``
                    command you need to install JDK by following the steps in `Oracle's installation guide <https://docs.oracle.com/en/java/javase/18/install/installation-jdk-microsoft-windows-platforms.html>`_

                Afterwards I clicked the **Create** button.

        #.  Once these steps were done I was able to select the OAuth client i just created in
            google play console and I clicked on the **Save Changes** button.
        #.  To continue with the service configuration process I had to add the play games services SDK
            to my APK to use the APIs. To do this I followed instructions found on
            `this Google Play Game Services Page <https://developers.google.com/games/services/v1/android/quickstart>`_.
            For my app I did the follwing

            #.  In the unity editor I went to **Edit > Project Settings > Player.
            #.  Under Publishing Settings, i checked the box next to **Custom Main Gradle Template**
            #.  This created a file under **Assets\Plugins\Android\mainTemplate.gradle. I then opened
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



