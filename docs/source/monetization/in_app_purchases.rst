################
In-App Purchases
################

Links
#####

*   `Unity Ads Documentation <https://docs.unity.com/ads/en-us/manual/UnityAdsHome>`_

Unity In-App Purchases Setup Log #1
###################################

#.  `Link your Unity Project to a Unity Dashboard Project <https://docs.unity.com/ugs/en-us/manual/overview/manual/managing-unity-projects#ConfiguringProjectsForUGS>`_.

    ..  note::

        We had already done this when setting up unity authentication.

#.  Sign your project up for for Unity In-App Purchases product in https://cloud.unity.com/

    #.  Sign into https://cloud.unity.com/
    #.  Click on the **Products** tab on the left hand side of the screen.
    #.  Click on the **In-App Purchases** product.
    #.  Click on the **Lauch** button. This will take you to the `Unity IAP Documentation <https://docs.unity.com/ugs/en-us/packages/com.unity.purchasing/4.9/manual>`_
    #.  From here I got the information I needed to proceed with implementing In App Purchases. I will document the next
        steps I took below.

#.  `Activate In-App Purchasing <https://docs.unity.com/ugs/en-us/packages/com.unity.purchasing/4.9/manual/Overview>`_ in Unity

    #.  In unity go to **Window > General > Services**
    #.  Click on the **In-App Purchasing** section. This should open In-App Purchasing Settings in the Project Settings
        window.
    #.  Click the **Off** Button to toggle In-App purchasing on. This will install the IAP package from the package
        manager.

#.  `Initialize Unity Gaming Services first then In-App Purchasing second <https://docs.unity.com/ugs/en-us/packages/com.unity.purchasing/4.9/manual/InitializationOverview>`_

    #.  Below is example code for initializing Unity Gaming Services

        ..  code-block:: c#

            using System;
            using Unity.Services.Core;
            using Unity.Services.Core.Environments;
            using UnityEngine;

            public class InitializeUnityServices : MonoBehaviour
            {
                public string environment = "production";

                async void Start()
                {
                    try
                    {
                        var options = new InitializationOptions()
                            .SetEnvironmentName(environment);

                        await UnityServices.InitializeAsync(options);
                    }
                    catch (Exception exception)
                    {
                        // An error occurred during services initialization.
                    }
                }
            }

    #.  Below is example code for initializing In App Purchases

        ..  code-block:: c#

            using UnityEngine;
            using UnityEngine.Purchasing;
            using UnityEngine.Purchasing.Extension;

            public class MyIAPManager : IDetailedStoreListener {

                private IStoreController controller;
                private IExtensionProvider extensions;

                public MyIAPManager () {
                    var builder = ConfigurationBuilder.Instance(StandardPurchasingModule.Instance());
                    builder.AddProduct("100_gold_coins", ProductType.Consumable, new IDs
                    {
                        {"100_gold_coins_google", GooglePlay.Name},
                        {"100_gold_coins_mac", MacAppStore.Name}
                    });

                    UnityPurchasing.Initialize (this, builder);
                }

                /// <summary>
                /// Called when Unity IAP is ready to make purchases.
                /// </summary>
                public void OnInitialized (IStoreController controller, IExtensionProvider extensions)
                {
                    this.controller = controller;
                    this.extensions = extensions;
                }

                /// <summary>
                /// Called when Unity IAP encounters an unrecoverable initialization error.
                ///
                /// Note that this will not be called if Internet is unavailable; Unity IAP
                /// will attempt initialization until it becomes available.
                /// </summary>
                public void OnInitializeFailed (InitializationFailureReason error)
                {
                }

                /// <summary>
                /// Called when a purchase completes.
                ///
                /// May be called at any time after OnInitialized().
                /// </summary>
                public PurchaseProcessingResult ProcessPurchase (PurchaseEventArgs e)
                {
                    return PurchaseProcessingResult.Complete;
                }

                /// <summary>
                /// Called when a purchase fails.
                /// IStoreListener.OnPurchaseFailed is deprecated,
                /// use IDetailedStoreListener.OnPurchaseFailed instead.
                /// </summary>
                public void OnPurchaseFailed (Product i, PurchaseFailureReason p)
                {
                }

                /// <summary>
                /// Called when a purchase fails.
                /// </summary>
                public void OnPurchaseFailed (Product i, PurchaseFailureDescription p)
                {
                }
            }

#.  `Define Products <https://docs.unity.com/ugs/en-us/packages/com.unity.purchasing/4.9/manual/DefiningProductsOverview>`_ that users can purchase.

    #.  In the above example script there was a section of code that defined products that users can purchase in your game.

        ..  code-block::

            var builder = ConfigurationBuilder.Instance(StandardPurchasingModule.Instance());
            builder.AddProduct("100_gold_coins", ProductType.Consumable, new IDs
            {
                {"100_gold_coins_google", GooglePlay.Name},
                {"100_gold_coins_mac", MacAppStore.Name}
            });

            UnityPurchasing.Initialize (this, builder);

    #.  Look to the `documentation <https://docs.unity.com/ugs/en-us/packages/com.unity.purchasing/4.9/manual/DefiningProductsOverview>`_
        to determine how to construct the products you plan to put in your game.

#.  `Enable users to purchase items <https://docs.unity.com/ugs/en-us/packages/com.unity.purchasing/4.9/manual/UnityIAPInitiatingPurchases>`_

    #.  The below script references the ``InitiatePurchase`` method of the ``IStoreController`` defined in the
        ``MyIAPManager`` class in the example above.

    ..  code-block:: c#

        // Example method called when the user presses a 'buy' button
        // to start the purchase process.
        public void OnPurchaseClicked(string productId) {
            controller.InitiatePurchase(productId);
        }

#.  `Process Purchase Requests <https://docs.unity.com/ugs/en-us/packages/com.unity.purchasing/4.9/manual/UnityIAPProcessingPurchases>`_

    #.  Use the ``ProcessPurchase`` function of your ``IStoreListener`` (in the ``MyIAPManager`` above) to respond to purchase requests. Look at
        the documentation to see what to return from this function as it depends on whether the user is purchasing
        consumables or not.
    #.  Note that when restoring purchases, the ``ProcessPurchase`` function will be called for each product the user
        owns.

#.  `Restore Transactions <https://docs.unity.com/ugs/en-us/packages/com.unity.purchasing/4.9/manual/UnityIAPRestoringTransactions>`_

    #.  Gogle Play automatically restores any products the user owns during the first initialization following reinstallation.
    #.  The ``ProcessPurchase`` method of your ``IStoreListener`` (in the ``MyIAPManager`` example script above) will be called for each owned item.

#.  `Testing Purchases <https://docs.unity.com/ugs/en-us/packages/com.unity.purchasing/4.9/manual/HowToTest>`_

    #.  In the ``MyIAPManager`` example script above, when initializing the ``StandardPurchasingModule``, set
        ``StandardPurchasingModule.Instance().useFakeStoreUIMode`` to ``FakeStoreUIMode.DeveloperUser``. In game
        a window will pop up that asks you how to initialize the store as well as choose how to respond to each
        purchase request that is initiated.

#.  `Set Up In-App Purchases on iOS <https://docs.unity.com/ugs/en-us/packages/com.unity.purchasing/4.9/manual/UnityIAPAppleConfiguration>`_

    #.  Go to https://appstoreconnect.apple.com/ and sign in
    #.  Select your app and click on the **App Store** Tab
    #.  On the left hand side of the screen look under Features and select **In-App Purchases**
    #.  On the In-App Purchases screen click the Plus button to create an In-App purchase. For each purchase
        you will have to enter a type, reference name, and product ID. Note that the product ID is the same
        ID used in Unity.
    #.  After entering all the information click the **Create** button.
    #.  On your new in app purchase product page scroll down to **Availability** and click the **Set Up Avaliability**
        button. By default Apple makes your product available to all possible countries.
    #.  Next, scroll down to the **Price Schedule** section and click the **Add Pricing** button.
    #.  Select your base country and price for the base country.
    #.  After clicking the **next** button you will be able to set prices across all other countries.
    #.  Look at the rest of the in app purchase page for other in app purchase options.

#.  `Test In-App Purchases on iOS <https://docs.unity.com/ugs/en-us/packages/com.unity.purchasing/4.9/manual/UnityIAPAppleConfiguration>`_

    #.  Go to https://appstoreconnect.apple.com/ and sign in
    #.  Go to the **Users and Access** section and select the **Sandbox** tab.
    #.  Click a button to **Add Test Account** and enter in the testers information.

        ..  note::

            From `Apple's sandbox documentation <https://developer.apple.com/help/app-store-connect/test-in-app-purchases/create-sandbox-apple-ids/>`_

            Use an email address that hasn’t been used as an Apple ID or to purchase iTunes or App Store content.
            Consider creating a dedicated email address for each sandbox tester.

            If your email service provider supports email subaddressing with a plus sign (+), you can use subaddresses
            of a sandbox-specific address for a sandbox tester. For example, if your base sandbox email is billjames2@icloud.com,
            you can use billjames2+UK@icloud.com, billjames2+US@icloud.com, and billjames2+JP@icloud.com as email addresses
            for additional testers. All communications sent to the subaddresses are also sent to the base address.



