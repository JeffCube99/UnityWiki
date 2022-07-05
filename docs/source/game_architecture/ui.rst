##
UI
##

**"Where is the play button? What Play But-- Oh no we forgot to implement the UI!!!"**

.. _UI_Element_Based_System:

UI Architecture: Element Based System
#####################################

In an object based ui system, collections of UI elements are placed inside of game objects. For example
all ui elements in the main menu are children MainMenu GameObject, and all ui elements in the
options menu are children of the OptionsMenu GameObject. This makes it fairly easy to swap between menus by setting
all ui parent objects inactive then setting the parent object of interest active. Additionally you can set multiple ui objects
active if you want to have multiple ui objects active at the same time like a pause menu overlaying the in game UI.

..  dropdown:: **UIManager.cs (Element Based System)**

    ..  code-block:: c#

        using System.Collections;
        using System.Collections.Generic;
        using UnityEngine;
        using UnityEngine.Events;

        public class UIManager : MonoBehaviour
        {
            public List<GameObject> uiElements;

            private void SetAllUiElementsActive(bool isActive)
            {
                for (int i = 0; i < uiElements.Count; i++)
                {
                    uiElements[i].SetActive(isActive);
                }
            }

            public void HideAllUiElements()
            {
                SetAllUiElementsActive(false);
            }

            public void ShowAllUiElements()
            {
                SetAllUiElementsActive(true);
            }

            public void HideSingleUiElement(int elementIndex)
            {
                uiElements[elementIndex].SetActive(false);
            }

            public void ShowSingleUiElement(int elementIndex)
            {
                uiElements[elementIndex].SetActive(true);
            }

            public void ShowSingleUiElementOnly(int elementIndex)
            {
                HideAllUiElements();
                uiElements[elementIndex].SetActive(true);
            }

            /// <summary>
            /// This function takes in a string with ui element indices separated by commas.
            /// For example : "1,2,3,12"
            /// We do this so that this function can be exposed to UnityEvents since it only has one string parameter.
            /// </summary>
            /// <param name="elementList"></param>
            public void ShowMultipleUiElementsOnly(string elementList)
            {
                HideAllUiElements();
                foreach (var indexString in elementList.Split(','))
                {
                    int index = int.Parse(indexString);
                    if (index < uiElements.Count)
                        uiElements[int.Parse(indexString)].SetActive(true);
                }
            }

        }


Example
*******

Click to download :download:`UIManagementExample.unitypackage </_downloads/UIManagementExample.unitypackage>`.

UI Organization Through Prefab Variants
#######################################

When crafting the UI for your game, you may find yourself deciding on changing the way certain buttons
appear / behave. You may have prefabs for each of these button types but what if you wanted to change
the font style for all buttons? You would have to go into each of the button prefabs and update the font used.
But what if there was a better way?

Start using prefab variants. You could start with a base button class and create many child prefabs from that base
class. Then if you wanted to change the font, you could simply adjust the font in the base prefab and watch it spread
to all children prefabs.

The below example showcases a standard menu created from prefabs and prefab variants making it very easy to modify.

Example
*******

..  important::

    This example requires the following packages to be installed:

    *   TextMeshPro Essentials

..  warning::

    This example also includes the following packages:

    *   UIManagementExample.unitypackage (See :ref:`UI_Element_Based_System`)


Click to download :download:`UIPrefabVariantSystemExample.unitypackage </_downloads/UIPrefabVariantSystemExample.unitypackage>`.