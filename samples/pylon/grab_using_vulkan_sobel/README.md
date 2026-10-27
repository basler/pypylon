# Vulkan Sobel Sample

Grabs Mono8 images directly into Vulkan memory (zero copy), runs a Sobel edge
filter on the GPU, and shows the original and the result side by side.

Run continuously with the window (close it or press Esc to stop):

```bash
python grab_using_vulkan_sobel.py
```

Process 100 frames without opening a window:

```bash
python grab_using_vulkan_sobel.py --no-display --frames 100
```

Without a camera, use Basler Camera Emulation, e.g. `PYLON_CAMEMU=1`.

## What goes where

| File | Contents |
|---|---|
| `grab_using_vulkan_sobel.py` | Camera setup and the grab loop: grab, filter, display. Start reading here. |
| `buffer_factory.py` | `VulkanBufferFactory`: pylon grabs into Vulkan memory; `grab_result.BufferContext` is the image on the GPU. |
| `image_filter.py` | `ImageFilter`: base class for GPU filters. |
| `sobel_filter.py` | `SobelFilter`: shader, output image, and commands of the Sobel algorithm. Template for new filters. |
| `display.py` | `ImageDisplay`: shows the original and processed images side by side. |
| `vulkan_context.py` | `VulkanContext`, `GpuImage`, `ComputeShader`: Vulkan device, memory, and shader helpers. |

## Adding a filter

1. Copy `sobel_filter.py`, e.g. to `dewarping_filter.py`. Replace the
   embedded shader, and create all resources the algorithm needs in `__init__`
   (shaders, the output image, lookup tables, ...). Record its GPU commands in
   `record()` and release the resources in `destroy()`.
2. In `grab_using_vulkan_sobel.py`, create the filter in the `with` statement
   next to the Sobel filter and chain it in the grab loop:

   ```python
   result_image = sobel_filter.process(camera_image)
   result_image = dewarping_filter.process(result_image)
   ```

Each filter takes the previous output as its input. `ImageFilter.process()`
records the GPU commands once per input image and replays them for later
frames, because pylon reuses a fixed set of grab buffers. Every filter waits
for the GPU before returning, so its output is ready for the next filter or the
display.

## Requirements

Python 3.10 or newer, pypylon, the Khronos Python `vulkan` bindings, and a
Vulkan 1.1 compute device. The window additionally requires PySDL2 and a
compute queue that can present.

## NVIDIA Performance Measurement

## Change GPU performance settings.

For a quick test, set Prefer Maximum Performance in NVIDIA Settings:

 1. Open NVIDIA X Server Settings.
 2. Select PowerMizer.
 3. Set Preferred Mode to Prefer Maximum Performance.
 4. Rerun the sample, ideally on AC power.

Enable performance mode:
nvidia-settings --assign '[gpu:0]/GPUPowerMizerMode=1'

Enable Auto Mode:
nvidia-settings --assign '[gpu:0]/GPUPowerMizerMode=0'


## Measure the GPU performance and memory utilization:

nvidia-smi --query-gpu=temperature.gpu,clocks.gr,clocks.mem,utilization.gpu,power.draw --format=csv -l 1