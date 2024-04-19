#####################################
Unity Universal Render Pipeline (URP)
#####################################

Links
#####

*   https://docs.unity3d.com/Packages/com.unity.render-pipelines.universal@16.0/manual/rendering-in-universalrp.html

Overview
########

What is a Render Pipeline?
**************************

A render pipeline is a sequence of steps that a graphics system follows to render a (3D) scene to a 2D screen.

What is Unity's Render Pipeline (URP)?
**************************************

Unity's Universal Render Pipeline (URP) is a prebuilt scriptable render pipeline made by Unity. In a URP project,
unity uses URP to render all cameras in your project. For each camera, URP executes the following sequence of steps:

#.  **Call the `beginContextRendering <https://docs.unity3d.com/ScriptReference/Rendering.RenderPipelineManager-beginContextRendering.html>`_
    event.** This allows the user to execute code before rendering each frame.
#.  For each camera in the scene:

    #.  **Call the `beginCameraRendering <https://docs.unity3d.com/ScriptReference/Rendering.RenderPipelineManager-beginCameraRendering.html>`_
        event.** This allows the user to execute code before rendering each camera loop. The event allows you to know what camera
        is about to be rendered.
    #.  **Setup culling parameters.** Configures parameters that determine how the culling system culls lights and shadows.
        The user can override this part of the render pipeline with a custom renderer.
    #.  **Perform culling.** Uses the culling parameters to compute a list of visible renderers (e.g. mesh renderer, sprite renderer, etc.)
        , shadow casters, and Lights that are visible to the camera. Culling parameters and Camera layer distances affect culling
        and rendering performance.
    #.  **Build Rendering Data.** Catches information based on teh culling output, quality settings from the URP Asset, Camera,
        and the current running platform to build the RenderingData struct. The Rendering data struct tells the renderer the amount
        of rendering work and quality required for the camera and the currently chosen platform.
    #.  **Setup renderer.** Builds a list of render passes, and queues them for execution according to the rendering data.
        The user can override this part of the render pipeline with a custom renderer.
    #.  **Execute the renderer.** Executes each render pass in the queue. the Renderer outputs the camera image to the
        framebuffer. The
    #.  Call the `endCameraRendering <https://docs.unity3d.com/ScriptReference/Rendering.RenderPipelineManager-endCameraRendering.html>`_
        event. This allows the user to execute code before after each camera loop. The event allows you to know what camera
        has finished rendering.

#.  Call the `endContextRendering <https://docs.unity3d.com/ScriptReference/Rendering.RenderPipelineManager-endContextRendering.html>`_
    event. This allows the user to execute code after rendering each frame.

Universal Render Pipeline Steps
###############################

Overview
********

*   Inside URP or in any custom RenderPipeline class unity calls the
    `RenderPipeline.Render <https://docs.unity3d.com/ScriptReference/Rendering.RenderPipeline.Render.html>`_ method automatically.
*   You can override the built in Render method to write custom rendering code.
*   This method is called once per frame and once per frame for each manual call to Camera.Render.
*   During the RenderPipeline.Render() function, the developer typically initializes a CommandBuffer, followed by adding
    a clear render target command. The commands are scheduled to be executed when calling the ScriptableRenderContext.ExecuteCommandBuffer() method
    from the ScriptableRenderContext input to the RenderPipeline.Render() function. By the end of the function
    the developer calls the ScriptableRenderContext.Submit() method to submit all scheduled commands they set up
    to the rendering loop for execution.
*   If you are using URP, you can use the
    `beginContextRendering <https://docs.unity3d.com/ScriptReference/Rendering.RenderPipelineManager-beginContextRendering.html>`_,
    `endContextRendering <https://docs.unity3d.com/ScriptReference/Rendering.RenderPipelineManager-endContextRendering.html>`_,
    `beginCameraRendering <https://docs.unity3d.com/ScriptReference/Rendering.RenderPipelineManager-beginCameraRendering.html>`_, or
    `endCameraRendering <https://docs.unity3d.com/ScriptReference/Rendering.RenderPipelineManager-endCameraRendering.html>`_
    to call your custom code at defined points using this method.
*   If you are creating your own custom RenderPipeline class, you can call the delegates yourself using
    `RenderPipeline.BeginContextRendering <https://docs.unity3d.com/ScriptReference/Rendering.RenderPipeline.BeginContextRendering.html>`_,
    `RenderPipeline.BeginCameraRendering <https://docs.unity3d.com/ScriptReference/Rendering.RenderPipeline.BeginCameraRendering.html>`_,
    `RenderPipeline.EndCameraRendering <https://docs.unity3d.com/ScriptReference/Rendering.RenderPipeline.EndCameraRendering.html>`_, and
    `RenderPipeline.EndContextRendering <https://docs.unity3d.com/ScriptReference/Rendering.RenderPipeline.EndContextRendering.html>`_,

Setup Culling Parameters
************************

*   Culling parameters are used to determine which objects should be rendered based on their visibility to the camera.
*   Culling parameters can improve performance by avoiding unnecessary rendering of objects that are not visible.
*   You can view the culling parameters for a given camera by using the `Camera.TryGetCullingParameters <https://docs.unity3d.com/ScriptReference/Camera.TryGetCullingParameters.html>`_
    method. This produces a `ScriptableCullingParameters <https://docs.unity3d.com/ScriptReference/Rendering.ScriptableCullingParameters.html>`_
    struct. The values of the struct are copied from the Camera's parameters.
*   Examples of culling parameters include:

    *   **cullingMask**: Determines which layers of game objects are visible to the camera
    *   **cullingMatrix**: A matrix that transforms an object from world space to the camera's clip space. This is used
        to determine if an object lies within the camera's field of view.
    *   **cullingOptions**: A flags enum that is used to configure a culling operation. These include:

        *   **OcclusionCull**: When this flag is set unity performs occlusion culling as part of the culling operation.
        *   **NeedsLighting**: when this flag is set, Unity culls Lights as part of the culling operation.

Perform Culling
***************

*   The `ScriptableRenderContext.Cull <https://docs.unity3d.com/ScriptReference/Rendering.ScriptableRenderContext.Cull.html>`_
    operation performs culling based on an input `ScriptableCullingParameters <https://docs.unity3d.com/ScriptReference/Rendering.ScriptableCullingParameters.html>`_
    struct.
*   Culling in this way returns a `CullingResults <https://docs.unity3d.com/ScriptReference/Rendering.CullingResults.html>`_
    struct that includes information about visible objects, lights, and reflection probes. Unity uses this data to render objects and process
    lights.
*   Examples of CullingResults includes:

    *   **visibleLights**: Array of visible lights.
    *   **visibleReflectionProbes**: Array of visible reflection probes.
    *   **visibleOffscreenVertexLights**: Array of off screen lights that still affect visible vertices.

Build Rendering Data
********************

*   For the universal render pipeline, unity defines its own custom RenderingData structure that flattens several
    rendering settings used to render a camera stack. It pulls from the pipeline asset, camera, and light
    settings as well as the culling results, and existing command buffer.

Setup Renderer
**************

*   At this stage, unity uses its custom UniversalRenderer class's Setup() method, with its inputs being the
    ScriptableRenderContext and the renderingData generated from the previous step.
*   This function enqueues a myriad of passes. Each pass has a configure function that takes in
    the CommandBuffer and render texture descriptor. The passes call Configure in the order they are enqueued
    and afterwards any commands added to the command buffer are scheduled to be executed by calling the
    ScriptableRenderContext.ExecuteCommandBuffer() method.

Execute The Renderer
********************

*   URP calls ScriptableRenderContext.Submit() to execute the commands that it previously sent to the ScriptableRenderContext context.
*   Included with these commands are commands to output the camera image to the frame buffer using commands like `Graphics.Blit <https://docs.unity3d.com/ScriptReference/Graphics.Blit.html>`_
    Blit that can copy data from a source such as the render texture of the final rendered image to a destination like
    the frame buffer belonging to a target camera.


How A Triangle Is Rendered In Unity URP
#######################################

