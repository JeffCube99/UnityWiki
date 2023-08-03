############
Beta Testing
############

`Google Play Console <https://play.google.com/console/about/>`_ gives the user access to tools to test your app with
specific groupd or open your tests to google play users.

Google Play Console
###################

Overview
********

*   `Google Play Console <https://play.google.com/console/about/>`_ gives the user access to tools to test your app with
    specific groupd or open your tests to google play users.
*   More information for android developers be found at https://support.google.com/googleplay/android-developer/answer/9845334?hl=en

Requirements
************

*   A Google Account

Set Up
******

#.  Create a `Gmail <https://mail.google.com/?>`_ or `Google Workspace <https://workspace.google.com/>`_ account
#.  Follow the sign up process for A Play Console Developer Account at https://play.google.com/console/

    ..  note::

        You can start out with an individual account and then in the future you can switch it to a company developer account:
        https://support.google.com/googleplay/android-developer/thread/203273835/change-account-type?hl=en#:~:text=Log%20into%20the%20Play%20Console,a%20link%20to%20change%20it

#.

Distributing App Through Google Play Console
********************************************

#.  Go to https://play.google.com/console/ and select your developer account
#.  Go to the **All apps** section and click the **Create app** button.
#.  Fill in the app details. Under the declarations section, read and understand all declarations and then check them off.
    Afterwards click the **Create app** button.
#.  On The Google Play Console, go to the **Testing** dropdown and select **Internal Testing**.
#.  From here scroll down and select the **Testers** Tab and below click on the **Create Email List** button.
#.  Name the email list and add emails of people who wish to test the game. Afterwards add a feedback URL
    or email address people can use to send feedback.
#.  Click the **Save** button on the lower right hand side of the screen.
#.  Next click on the the **Releases** tab. Underneath click **Create new release**
#.  Under the **App Integrity** section, click **Choose signing key**. For this exercise we will choose to use the
    Google-generated key.
#.  Before you can upload your app. You must sign it in release mode. To do so follow the steps below:

    #.  Go to **Edit > Project Settings** and Select the **Player** section on the left
    #.  Click the android tab and scroll down to the **Publishing Settings** section.
    #.  Click the **Keystore Manager** Button. This will open the keystore manager window. In here you can create a new
        key for your app. Inside this window click the Keystore Dropdown and select the **Create New** option and select
        a place to store it. Note that you do not want to save this key in a place accessible to the public like in
        a public github repository. (It is good practice to not even store the key inside a private github repository).
    #.  Enter the password for the keystore as well as the Alias and password for the key
    #.  Click the **Add Key** button. Then click yes when Unity asks to set it as your Project Keystore and Project Key.

        ..  note::

            For more information on the key making process see: https://docs.unity3d.com/Manual/android-keystore-create.html .

#.  Next create an app bundle file (.aab file) from your unity project. To do this, do the following:

    #.  Open your unity project
    #.  Go to **File > Build Settings**
    #.  Make sure the **Android** platform is selected
    #.  Check the box next to the **Build App Bundle** option and uncheck the box next to the **Development Build** option.
    #.  Press the **Build** button and set the name and location of the build.

        ..  note::

        The first time you build this way the build may take way longer than expected. If this is the case just cancel
        the build, (and optionally close and re open the project) and try re building it. It may go much faster next time.

    ..  note::

        From: `About Android App Bundles <https://developer.android.com/guide/app-bundle>`_

        *   An Android App Bundle is a publishing format that includes all your app’s compiled code and resources,
            and defers APK generation and signing to Google Play.
        *   Google Play uses your app bundle to generate and serve optimized APKs for each device configuration,
            so only the code and resources that are needed for a specific device are downloaded to run your app.
            You no longer have to build, sign, and manage multiple APKs to optimize support for different devices,
            and users get smaller, more-optimized downloads.

#.  Next, return to the Google Play Console window and upload your app bundle under the **App Bundles** section
#.  Add your information under the **Release Details** section.
#.  Click the blue **Next** button.
#.  Scroll up and find and click the section called **Preview and confirm the release**.
#.  On the preview page resolve any errors or warnings you encounter. See below for some of the errors and warnings I overcame:

    *   For the error "Your app cannot be published yet. Complete the steps listed on the Dashboard."

        #.  This error doesn't come up normally when you do internal testing. Check to see that your
            build contains an app bundle. This appeared for me when i accidentally went to the preview page
            without assigning an app bundle to the release.

    *   For the "There is no deobfuscation file associated with this App Bundle" warning:

        #.  Go to **Edit > Project Settings** and select the player section
        #.  Select the android tab and under the **Publishing Settings** dropdown under the Minify section check the
            options **Use R8** and **Release**
        #.  After building your .aab file, you should also see a mapping.txt file next to it.
        #.  Upload the new .aab file to Google Play. Scrolling down below the upload section, find the bundle, click
            the 3 dots next to it and click the option to pass in the mapping.txt file.

            ..  note::

                This is how some users reported solving the problem but for me Google Play Console failed with
                the uploading the .txt file even after multiple attempts


    * For the "This App Bundle contains native code, and you've not uploaded debug symbols" warning:

        #.  Go to **File > Build Settings**
        #.  Under the android settings, set the **Create symbols.zip** dropdown to Public
        #.  After building your .aab file you should also see a symbols.zip file next to it.
        #.  Upload the new .aab file to Google Play. Scrolling down below the upload section, find the bundle, click
            the 3 dots next to it and pass in the symbols.zip file.

            ..  note::

                If you encounter the error "Version code XXX has already been used"
                click the **Internal Testing** section on the left and click the **Discard Release** button. Afterwards click
                the **App Bundle Explorer** tab on the left, select the bundle you just discarded and click the **Delete app bundle** button

#.  Once all errors and warnings are resolved on the preview page, click the **Save** button.
#.  Testers will not automatically be notified via email. For them to recieve notifications about releases they
    need to be provided with an opt-in link. This link can be located on the Google Play Console by clicking on
    **Internal testing** on the left section, clicking the **Testers** tab on the page, and scrolling down until you see
    the **How testers join your test** and click the **Copy link** button.