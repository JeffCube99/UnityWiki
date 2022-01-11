=================
Unity Collaborate
=================

..  sectnum::

..  contents::
    :local:

Get Started With an Existing Project
====================================

#.  Open Unity Hub
#.  Sign into your unity account
#.  Under the Projects tab you should see the shared project in grey. To download
    it select the unity version and click the cloud download button icon.

..  note::

    If you do not see a shared project sometimes you first have to hit the refresh
    button located below the last project in the list. If the button does not exist
    that means it has already refreshed. To refresh it again simply close and open
    unity hub. If you still cannot find the project that may mean that the owner
    of the project has yet to share it with you. It is possible that even if the
    owner of the project added you to the Unity group they did not specifically add you to
    the project within the group. Follow this
    `forum thread <https://forum.unity.com/threads/can-not-download-collab-project.526953/>`_ for more details

Collaborate in the Unity Editor
===============================

Collaborate Window
------------------

Inside the Unity Editor select Window -> Collaborate to open the collaboration window.

Sync with Changes from a Teammate
---------------------------------

Whenever a teammate updates some of their files, a "Sync" button will appear in the collaborate
window. Click on that button to update your project with their changes.

Push Your Changes
-----------------

Inside the collaborate window you can look over all of your changes. Select the ones you want to
apply, and then write a commit message in the text box below. Finally click the "Publish" button
to push your changes to the rest of the team.

Debugging Merge Conflicts
-------------------------

Sometimes you may accidentally modify the same files as your teammates. When this happen and you
click the "Sync" button in the collaborate window, unity will present an error message saying that
conflicts were detected. To debug these conflicts do the following:

*  If you have not set any Diff/Merge tools:

    #.  Go to Edit -> Preferences
    #.  Under the "External Tools" tab you should see an comment saying something like

        ..  code-block:: text

            No supported VCS diff tools were found ...

    #.  I chose to install SourceGear DiffMerge which was the first diff tools that was reccommended by Unity.
        You can download it from the `DiffMerge donwload page <https://sourcegear.com/diffmerge/downloads.php>`_.
    #.  After downloading the installer, launch it and follow the steps in the installation window. By default
        the executable will be installed in ``ProgramFiles/SourceGear/Common/sgdm.exe``
    #.  Next we go back to Unity and go to Edit -> Preferences
    #.  Under the "External tools" tab go to the "Revision Control Diff/Merge" dropdown and select "SourceGear DiffMerge".

        ..  note::

            If the "SourceGear DiffMerge" option does not exist, refresh the unity editor
            by closing and re-opening it.

*   If you have Diff/Merge tools installed:

    #.  Open the Collaborate Window (Window -> Collaborate)
    #.  Next to the files with differences click the eye icon. The differences should appear using your
        Diff/Merge tool of choice. Here you can view the differences but you will not be able to resolve the merge
        conflicts here as it is a read only view.
    #.  If you click on the merge icon (arrow with two tails) You will open your Diff/Merge tool with the ability to
        resolve the merge conflict and edit the file directly.
    #.  Often when are dealing with prefabs the conflicts will be very difficult to resolve
        through text editing alone. therefore you have 2 other options.

        *   **Use My Changes**: The "arrow pointing up into a line" icon is used to accept your own changes.
        *   **Use Remote Changes**: The "arrow pointing down into a line" icon is used to accept the remote's changes.



