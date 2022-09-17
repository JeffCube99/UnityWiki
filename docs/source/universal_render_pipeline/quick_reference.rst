##########################################
Universal Render Pipeline: Quick Reference
##########################################

Purpose of URP
##############
**"Why should my project use URP?***

The Universal Render Pipeline helps developers quickly and easily create optimized graphics across a range of platforms from
mobile to high-end consoles and PCs.

*   In unity a Render Pipeline performs a series of operations that take the contents of a scene and displays them on a screen.
*   Unity has 3 prebuilt render pipelines:

    *   The Built-in Render Pipeline is Unity’s default render pipeline. It is a general-purpose render pipeline that has limited options for customization.
    *   The Universal Render Pipeline (URP) is a Scriptable Render Pipeline that is quick and easy to customize, and lets you create optimized graphics across a wide range of platforms.
    *   The High Definition Render Pipeline (HDRP) is a Scriptable Render Pipeline that lets you create cutting-edge, high-fidelity graphics on high-end platforms.

Documentation
#############

For more comprehensive documentation on the URP, visit: https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@14.0/manual/index.html

Installing URP
##############

For installation instructions visit: https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@14.0/manual/index.html

URP Settings
############

*   The URP uses a Scriptable Object asset called **Universal Render Pipeline Asset** to adjust the project's render settings. The
    advantage of this system is that you can quicly swap in and out settings assets to experiment with different render settings
    (e.g. swap shadows on / off).

    ..  note::

        When you create a project from the URP template, unity provides you with some default settings assets in the
        **Project** window under **Assets > Settings**.

*   You can find the URP settings page in the **Project Settings** window under **Graphics**. You can then assign a
    **Universal Render Pipeline Asset** to the **Scriptable Render Pipeline Settings** field.

    ..  important::

        The **Scriptable Render Pipeline Settings** field IS NOT USED if there is Render Pipeline Asset override
        specified inside the Quality Settings. To see if there is an override, inside the **Project Settings** window, go to
        **Quality** and check **Rendering > Render Pipeline Asset**.

*   **URP Global Settings**: In the **Project Settings** window under **Graphics > URP Global Settings**, you can
    assign a **Universal Render Pipeline Global Settings** Scriptable object asset. This asset
    lets you define settings including the names of rendering layers (for 3d renderers) as well as Shader Stripping
    that define which shader variants unity strips when you build the player.

    ..  note::

        *   Unity compiles shader source files into shader programs. Each compiled shader program has one or more variants:
            different versions of the shader program for different conditions. At runtime, Unity uses the variant that
            matches the current requirements. You configure variants using shader keywords (e.g. "COLOR_RED", "COLOR_GREEN").
        *   Stripping shaders can give you smaller build sizes and shorter build times (e.g. a project that never uses
            shadows for directional lights, you can uncheck **Cast Shadows** in the URP asset and shader stripping will
            strip these shader variants from the build.
