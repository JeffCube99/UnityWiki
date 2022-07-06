#########
User Data
#########

**"Looks like a player got a high score! ... And look here comes another bug report."**

..  contents::
    :local:

.. _User_Bug_Reports:

User Bug Reports
################

************************
Sourcing Player Feedback
************************

Common ways to get feedback on your game are:

*   Asking people you give the game to send feedback to you directly.
*   Look at comments under your game page.
*   Look at reviews of your game or comments under your game page.

However what if you wanted to include a report feature directly into the game? This way you could
be notified of many issues found by players, without having to scan through comments to see if anyone
brings up potential issues.

**************************
Use Unity Cloud Dignostics
**************************

Visit `Unity Cloud Diagnostics <https://unity.com/products/cloud-diagnostics>`_ to quickly get started integrating
user bug reporting into your porject. It is free to all unity creators although free users are limited to
a small amount of reports per day.

The steps to integrating this into your project may vary depending on when you read this but in general it goes as
follows:

#.  Visit `Unity Cloud Diagnostics <https://unity.com/products/cloud-diagnostics>`_ and click the **Get started** button.
    If you don't see that then visit the
    `Getting Started Cloud Diagnostics <https://docs.unity.com/cloud-diagnostics/GettingStarted/GettingStartedwithCloudDiagnostics.html>`_
    page directly.
#.  On the left side bar, navigate your way to the `User Reporting <https://docs.unity.com/cloud-diagnostics/UserReporting/SettingupUserReporting.html>`_
    section and follow the steps for setting up user reporting in your unity project.
#.  At some point you will install an SDK that contains a prefab you can drag into your scene. The prefab
    has a button that will allow a user to submit a bug report.

..  important::

    With the SDK you are able to submit reports straight from the unity editor! It may take a few minutes for the reports
    to register on `Unity Dashboard <https://dashboard.unity3d.com>`_ so be patient. With the reports working in the
    editor you should be able to then build your games on whatever platform you use and submit reports in the working builds.