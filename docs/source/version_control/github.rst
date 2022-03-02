======
GitHub
======

GitHub for Unity Package
========================

..  warning::

    From the reviews on the Asset Store, it is not reccommended that you use GitHub for Unity as it is prone to
    breaking and has a lack of development with later versions of Unity.
    Use to GitHub for Desktop instead.

Installation
------------

You can install GitHub for unity in the editor following these steps:

#.  Go to the `Unity Asset Store <assetstore.unity.com>`_ and search for GitHub.
#.  Click on GitHub for Unity and on its store page click the "Add to My Assets" button.
#.  In the unity editor. Go to **Window > Package Manager**.
#.  In the Packages dropdown select **My Assets**. Then search for GitHub.
#.  Select the GitHub for Unity package and click **Import**


GitHub Desktop
==============

Installation
------------

Install GitHub Desktop from https://desktop.github.com/ and follow the installation instructions


Add An Existing Project
-----------------------

Lets say we have an existing project located at ``C:\UnityProjects\ExampleProject``. To create a git repository
from this project follow these steps:

#.  Open and sign into GitHub Destkop
#.  Go to **File > New repository...**
#.  Given that our project is located at ``C:\UnityProjects\ExampleProject`` we set ``ExampleProject`` for the
    **Name** and ``C:\UnityProjects`` for the **Local path**.
#.  Under the **Git ignore** option select **Unity**
#.  If the existing project uses Git LFS, Github Desktop may prompt you to initialize Git LFS. If it does
    click on **Initialize Git LFS**
#.  After initializing the repository, you can publish it by clicking on the **Publish repository** button at the
    top left of the GitHub Destkop window.

Clone from an online repository
-------------------------------

#.  Go to **File > Options** and sign into your GitHub account
#.  Select **Current Repository dropdown > Add dropdown > Clone repository**
#.  Select an existing repository from github.
#.  Choose a location on your computer to clone the repository.

    ..  note::

        When choosing where to clone your repository you do not have to create a new directory with your project name
        it will automatically be created at the location you specify

Undo Some / All Uncommitted Changes
-----------------------------------

If you want to undo some or all of your changes

#.  Go to your repository on GitHub Desktop
#.  Click the Changes section
#.  Select the changes you wish to discard, right click them, and select the discard option.