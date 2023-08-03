############################
Getting Started With Android
############################

**"I want to put a game on an Android phones. What is the first step?"**

..  contents::
    :local:

Quickstart
##########

*   If you want to run a game in the editor on a phone in general, see :ref:`Unity_Remote`.
*   If you want to build and run a game on an android device see :ref:`Unity_Android_Build` (Requires a MAC).

Testing Your Game On Devices
############################

.. _Unity_Android_Build:

*******************
Unity Android Build
*******************

..  note::

    Here are some links that helped me with this process:

    *   `How to EASILY Build to an Android Phone in Unity <https://www.youtube.com/watch?v=Nb62z3J4A_A>`_
    *   `Publishing for Android <https://learn.unity.com/tutorial/publishing-for-android#>`_

..  note::

    The following steps were done using:

    *   A machine running Windows 10.

#.  Add Android build support to your unity installation. You can add Android Build Support inside Unity Hub by navigating to
    the **Installs** tab, clicking the triple dots / cog icon next to your chosen installation, and selecting **Add Modules**.
    From there you can select and download Android build support.
#.  Open up your unity project and navigate to **Edit > Preferences**. Select the **External Tools** category on the left
    hand side. If you then scroll to the bottom you should see that All android JDK, SDK, NDK, and other elements
    are installed with unity. If this is not the case, retry the android build support installation step above.
#.  Go to **File > Build Settings**. Under the **Platform** section select **Android** and press the **Switch Platform**
    button on the lower right hand side of the window.
#.  On your Android smartphone, enable developer mode. This setting may vary from phone to phone so you should look
    up the process for your device online.
#.  Once developer mode is enabled you should then have access to a developer options panel. We will enable the options for:

    *   USB Debugging (to build to our phone)
    *   Stay Awake (Screen will not turn off while your phone is plugged in).
#.  Now plug your phone into your computer. On your phone, if there is a popup asking you to allow USB debugging, select
    the allow option.
#.  Go to **File > Build Settings** and under the Android settings locate the **Run Device** dropdown. Click the
    **Refresh** button next to the dropdown and after the refresh you should be able to select your device from the
    device drop down.
#.  On build settings locate the **Development Build** checkbox and check it. This will allow us to build to our phone
    without requiring a application key.
#.  Before building to your phone, visit **Edit > Project Settings** and navigate to the Player section on the left.
    From here you can set the Company Name, Product Name, and Version number. Below this you can click on the android
    tab to set icons for your device as well as other settings. Some important settings to consider are listed below:

    *   Package Name:

        *   Go to **Edit > Project Settings** under the Player section, select the android tab. Under the
            **Other Settings** dropdown under the **Identification** section, check the Override Default Package Name
            and set the name to "com.[Company Name].[Product Name]"

    *   Target API Level:

        *   The Google Play store has a target API Level requirement: https://developer.android.com/google/play/requirements/target-sdk .
        *   Go to **Edit > Project Settings** under the Player section, select the android tab. Under the
            **Other Settings** dropdown under the **Identification** section, set the Minimum API level to the Google Play
            store minimum, and the Target API Level to highest installed.

#.  Go to **File > Build Settings** and, with android select build and run and then choose a folder to build to and
    the name of the .apk file. Sometimes a window may pop up telling you may be missing support for an API level. If
    so clidk the **Update Android SDK** button. If the software of the device does not meet the API level then you will have to
    go back into your project settings and set the Minimum API level to the level of your device.

    ..  note::

        On the play store if you do not support the correct API version you will recieve an error when trying to run
        the game.

    ..  note::

        The next time you build on your device you can simply overwrite the preexisting apk file with the new one.

#.  Once the build is complete the game should start to run on your device.
