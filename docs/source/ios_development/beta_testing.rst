############
Beta Testing
############

The `Apple App Store Guidelines <https://developer.apple.com/app-store/review/guidelines/#beta-testing>`_ explicitly
state that "Demos, betas, and trial versions of your app don't belong on the App Store". Instead they refer
developers looking to test their apps to Apple's `TestFlight <https://developer.apple.com/testflight/>`_ Service.

TestFlight
##########

Overview
********

*   Apple provides the TestFlight service to make it easy for developers to invite users to test their Apps
*   More information can be found at https://developer.apple.com/testflight/

Requirements
************

*   A Mac computer
*   A Apple Developer account
*   A Xcode project connected to your apple developer account (See :ref:`Unity_iOS_Build`)

Set Up
******

#.  Create an Apple Developer account. Visit https://developer.apple.com/ for more information. Note that this process
    can take up to 5-7 business days.
#.  Go to https://developer.apple.com/account/
#.  On the webpage under the section **Program resources**, you should see a section called **App Store Connect**. Under
    this click the link for **Apps**. This should take you to https://appstoreconnect.apple.com/apps
#.  Click the button for adding a new app.
#.  Enter the relevant app information:

    *   Under the Bundle ID section, if you havent already registered an ID for your app see the article :ref:`Register_Bundle_ID`.
    *   Under the SKU section just enter any unique identifier you wish. You can use the name of your game for example

#.  Once you are done entering the app information click on the **Create** button.

#.  With your app created on App Store Connect. It is time to upload a build. Below we summarize the process for uploading
    an app using Xcode. but for more information see the links below

    *   https://developer.apple.com/help/app-store-connect/manage-builds/upload-builds/
    *   https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases

#.  In Xcode, go to **Product > Scheme > ChooseScheme** and select your app
#.  Next select **Product > Archive**. You may be prompted to sign up for Xcode cloud for their automatic services including
    archiving but we will defer from using this for now.
#.  After the archiving process is complete, the organizer window will automatically open with the archives section selected.
    From here you will be able to see your archive there.
#.  To confirm that your app is ready for TestFlight, select your archive in the archive window and click the **Validate App**
    button.

    *   During this process an App Store Connect distribution window will open. We select the options for
        uploading the app's symbols and managing version / build numbers before clicking **Next**
    *   During this process we opt in for automatically managing signing for app store connect distribution.
        Once the signing setup is complete we review the information and click **Validate**

#.  Validation is complete when you are presented with a screen titled **App "XXX" successfully validated**. From here
    you can click the **Done** button.
#.  Next select the Distribute button and select the **App Store Connect** option (for the app store and test flight service) followed by the **Upload** option. We
    next choose the options to upload app symbols and mange version / build numbers. We then allow for automatic signing
    management. Once this process is complete we click the **Upload** button.
#.  Once the upload is complete you you can see the build being processed by going to https://appstoreconnect.apple.com/ ,
    selecting your app, and clicking on the **TestFlight** tab.

Distributing App Through TestFlight
***********************************

For more information on TestFlight see https://developer.apple.com/help/app-store-connect/test-a-beta-version/overview-of-testflight

#.  Go to https://appstoreconnect.apple.com/ and click on you app
#.  Go to the TestFlight tab and check that your app status is **Ready to Submit**.

    ..  note::

        If you have not uploaded a build yet, see the setup instructions in the previous section.

#.  Under the general information section on the left hand side, select test information and fill out the sections
    including the feedback email.
#.  Back on the TestFlight Page under the **Build** section, click and open the build you wish to test. Under the test
    information page, include a description of what you want users to test / pay attention to as well as any other information
    they should know.
#.  Navigate back to your app's TestFlight page. If you have not already done so, create a group to invite testers. If you are just starting out you can create a
    Internal group. Go to the Internal Group section on the left hand side of the webpage and click the blue "+" button
    to create a new internal group. In this example, when we create a group we will opt out of automatic distribution.
#.  Now with the group selected, go to the **Testers** section and click the blue "+" button to add testers to the group.
#.  After adding your testers, go to the **Builds** section and click the blue "+" button to add a build. Then from the dropdowns
    you can select the appropriate version number and options for your builds should appear that you can then add.

    ..  note::

        Once users have been added to the group a build has been assigned, the users in the group will be sent an email
        with instructions on how to download TestFlight and how to begin testing the app.

#.  Users can leave feedback inside the testflight app. You can view this feedback on the app's TestFlight page under
    the section Feedback where you have access to user screenshots.
