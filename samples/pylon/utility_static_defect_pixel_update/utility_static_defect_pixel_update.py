#!/usr/bin/env python3
"""\
Detect and update user static defect pixels e.g. on ace 2 cameras.

See also:
https://docs.baslerweb.com/knowledge/static-defect-pixel-correction-in-ace-2-additional-information

This utility grabs a series of frames, averages them over time to suppress
temporal noise, and detects hot pixels (bright outliers in a dark image) or
cold pixels (dark outliers in a bright image). The detected coordinates are
merged into the camera's user static-defect list and written back.

Run it in one of two modes:
  - hot:  point the camera at a dark scene (lens capped) to find hot pixels.
  - cold: point the camera at a bright, homogeneous scene to find cold pixels.

Without hardware, configure Basler Camera Emulation so a virtual device is
visible to pylon.FirstFound:
https://docs.baslerweb.com/camera-emulation

Note: This sample requires proper hardware setup to function correctly.
"""

import argparse
import sys

import numpy as np
from pypylon import pylon

NUMBER_OF_IMAGES_FOR_MEAN = 100
DEFAULT_EXPOSURE_TIME_US = 30000.0
DEFAULT_THRESHOLD_DARK_DN = 130.0
DEFAULT_THRESHOLD_HOT_DN = 15.0
TOP_OUTLIERS_TO_PRINT = 20
GRAB_TIMEOUT_MS = 5000

HOT_PIXEL_GAIN_DB = 18.0
COLD_PIXEL_GAIN_DB = 0.0
HOT_MODE_MAX_MEAN_PERCENT = 20.0
COLD_MODE_MIN_MEAN_PERCENT = 75.0


class MeasurementConfiguration(pylon.ConfigurationEventHandler):
    """Apply measurement-safe camera settings when the camera opens."""

    def __init__(self, mode, exposure_time_us):
        super().__init__()
        self.mode = mode
        self.exposure_time_us = exposure_time_us

    def OnOpened(self, camera):
        # Disable automatic adjustments and image-altering features so the
        # temporal average reflects the raw sensor response. TrySetValue is a
        # no-op on cameras that do not expose a given parameter.
        camera.ExposureAuto.TrySetValue("Off")
        camera.GainAuto.TrySetValue("Off")
        camera.OffsetX.TrySetToMinimum()
        camera.OffsetY.TrySetToMinimum()
        camera.Width.TrySetToMaximum()
        camera.Height.TrySetToMaximum()
        camera.TestImageSelector.TrySetValue("Off")
        camera.PixelFormat.TrySetValue("Mono8")
        camera.ReverseX.TrySetValue(False)
        camera.ReverseY.TrySetValue(False)
        camera.BinningHorizontal.TrySetValue(1)
        camera.BinningVertical.TrySetValue(1)
        camera.LUTEnable.TrySetValue(False)
        if not camera.GammaEnable.TrySetValue(False):
            camera.Gamma.TrySetValue(1.0, pylon.FloatValueCorrection_ClipToRange)
        camera.BslFlatFieldCorrection.TrySetValue("Off")
        camera.BslVignettingCorrection.TrySetValue("Off")
        camera.BslShadingCorrection.TrySetValue("Off")
        camera.BslColorCorrection.TrySetValue("Off")

        gain_db = HOT_PIXEL_GAIN_DB if self.mode == "hot" else COLD_PIXEL_GAIN_DB
        camera.Gain.TrySetValue(gain_db)
        camera.ExposureTime.TrySetValue(self.exposure_time_us)


def acquire_mean_image(camera, number_of_images=NUMBER_OF_IMAGES_FOR_MEAN):
    """Grab number_of_images frames and return their per-pixel mean as float64."""
    print(f"Acquiring {number_of_images} images for temporal averaging...")
    accumulator = None
    grabbed = 0

    camera.StartGrabbingMax(number_of_images, pylon.GrabStrategy_LatestImageOnly)
    while camera.IsGrabbing():
        with camera.RetrieveResult(GRAB_TIMEOUT_MS, pylon.TimeoutHandling_ThrowException) as grab_result:
            if not grab_result.GrabSucceeded():
                continue
            frame = grab_result.Array.astype(np.float64)
            accumulator = frame if accumulator is None else accumulator + frame
            grabbed += 1

    if grabbed == 0:
        raise RuntimeError("No images were grabbed successfully.")

    return accumulator / grabbed


def get_pixel_dynamic_range(camera, mean_image):
    """Return the (min, max) pixel dynamic range in DN, with sensible fallbacks."""
    observed_max = float(mean_image.max())
    if observed_max <= 255.0:
        fallback_max = 255.0
    elif observed_max <= 4095.0:
        fallback_max = 4095.0
    else:
        fallback_max = 65535.0

    pixel_min = float(camera.PixelDynamicRangeMin.GetValueOrDefault(0))
    pixel_max = float(camera.PixelDynamicRangeMax.GetValueOrDefault(int(fallback_max)))
    if pixel_max <= pixel_min:
        return 0.0, fallback_max

    return pixel_min, pixel_max


def pixel_value_percent_of_range(value, pixel_min, pixel_max):
    """Return value as a percentage of the [pixel_min, pixel_max] range."""
    return ((value - pixel_min) / (pixel_max - pixel_min)) * 100.0


def evaluate_brightness(mode, mean_gray_value, pixel_min, pixel_max):
    """Return (is_valid, mean_percent, warning) for the acquired average brightness."""
    mean_percent = pixel_value_percent_of_range(mean_gray_value, pixel_min, pixel_max)

    if mode == "hot" and mean_percent > HOT_MODE_MAX_MEAN_PERCENT:
        return False, mean_percent, f"image too bright for hot-pixel detection ({mean_percent:.1f}%). Darken the scene."
    if mode == "cold" and mean_percent < COLD_MODE_MIN_MEAN_PERCENT:
        return False, mean_percent, f"image too dark for cold-pixel detection ({mean_percent:.1f}%). Brighten the scene."

    return True, mean_percent, None


def detect_hot_pixels(mean_image, threshold_offset_dn):
    """Return hot-pixel outliers as (x, y, value, relevance) tuples plus the threshold."""
    background_mean = float(mean_image.mean())
    hot_threshold = background_mean + threshold_offset_dn
    rows, cols = np.where(mean_image > hot_threshold)
    outliers = [
        (
            int(cols[i]),
            int(rows[i]),
            float(mean_image[rows[i], cols[i]]),
            float(mean_image[rows[i], cols[i]]) - hot_threshold,
        )
        for i in range(len(rows))
    ]
    outliers.sort(key=lambda item: item[3], reverse=True)
    return outliers, background_mean, hot_threshold


def detect_cold_pixels(mean_image, threshold_dn):
    """Return cold-pixel outliers as (x, y, value, relevance) tuples plus the threshold."""
    rows, cols = np.where(mean_image < threshold_dn)
    outliers = [
        (
            int(cols[i]),
            int(rows[i]),
            float(mean_image[rows[i], cols[i]]),
            threshold_dn - float(mean_image[rows[i], cols[i]]),
        )
        for i in range(len(rows))
    ]
    outliers.sort(key=lambda item: item[3], reverse=True)
    return outliers, threshold_dn


def outliers_to_coordinates(outliers):
    """Reduce (x, y, value, relevance) outliers to a list of (x, y) coordinates."""
    return [(x, y) for x, y, _value, _relevance in outliers]


def merge_coordinate_lists(existing_pixels, detected_pixels):
    """Merge existing and detected (x, y) pixels into a sorted, duplicate-free list."""
    merged = set()
    for pixel in existing_pixels:
        merged.add((int(pixel[0]), int(pixel[1])))
    for x, y in detected_pixels:
        merged.add((int(x), int(y)))
    return sorted(merged, key=lambda item: (item[1], item[0]))


def print_outlier_report(outliers):
    """Print the number of detected outliers and the strongest ones."""
    print(f"\nDetected outliers: {len(outliers)}")
    if not outliers:
        print("  No defect pixels detected.")
        return

    print(f"  Top {min(len(outliers), TOP_OUTLIERS_TO_PRINT)} outliers (x, y, value_dn, relevance_dn):")
    for x, y, value, relevance in outliers[:TOP_OUTLIERS_TO_PRINT]:
        print(f"    ({x:5d}, {y:5d})   value={value:8.2f}   relevance={relevance:8.2f}")


def update_user_defect_list(camera, detected_pixels):
    """Merge detected pixels into the camera's user static-defect list and write it back."""

    capacity = camera.BslStaticDefectPixelCorrectionMaxDefects.GetValueOrDefault( 0 )
    if capacity <= 0:
        raise RuntimeError("The camera does not support static defect pixel correction or has zero capacity.")
    if capacity < len(detected_pixels) :
        raise RuntimeError("Too many defects detected - adopt test settings or reduce the number of detected defects.")

    get_ok, existing_pixels = pylon.StaticDefectPixelCorrection.GetDefectPixelList(
        camera.NodeMap,
        [],
        pylon.StaticDefectPixelCorrection.ListType_User,
    )
    if not get_ok:
        raise RuntimeError("Reading the user static-defect list failed.")

    target_pixels = merge_coordinate_lists(existing_pixels, detected_pixels)

    normalize_ok, normalized_pixels = pylon.StaticDefectPixelCorrection.NormalizePixelList(
        camera.NodeMap,
        target_pixels,
    )
    if not normalize_ok:
        raise RuntimeError("Normalizing the static-defect list failed.")

    set_ok, written_pixels = pylon.StaticDefectPixelCorrection.SetDefectPixelList(
        camera.NodeMap,
        normalized_pixels,
        pylon.StaticDefectPixelCorrection.ListType_User,
    )
    if not set_ok:
        raise RuntimeError("Writing the user static-defect list failed.")

    return len(written_pixels)


def parse_arguments(argv=None):
    """Parse the command-line arguments for the utility."""
    parser = argparse.ArgumentParser(description="Detect and update user static defect pixels.")
    parser.add_argument("mode", choices=("hot", "cold"), help="detection mode")
    parser.add_argument(
        "-e", "--exposure-time-us", type=float, default=DEFAULT_EXPOSURE_TIME_US,
        help="exposure time in microseconds",
    )
    parser.add_argument(
        "-td", "--threshold-dark-dn", type=float, default=DEFAULT_THRESHOLD_DARK_DN,
        help="cold-pixel threshold in DN",
    )
    parser.add_argument(
        "-th", "--threshold-hot-dn", type=float, default=DEFAULT_THRESHOLD_HOT_DN,
        help="hot-pixel threshold offset above the background mean in DN",
    )
    parser.add_argument(
        "-n","--dry-run", action="store_true",
        help="detect defect pixels but do not update the camera list",
    )
    parser.add_argument(
        "-f", "--force", action="store_true",
        help="continue even if the acquisition brightness is out of range",
    )
    return parser.parse_args(argv)


exit_code = 0
try:
    args = parse_arguments()
    print(f"Mode: {args.mode}")
    print(f"Exposure time: {args.exposure_time_us} us")

    with pylon.InstantCamera() as camera:
        # Register the configuration before Open() so OnOpened can apply it.
        configuration = MeasurementConfiguration(args.mode, args.exposure_time_us)
        camera.RegisterConfiguration(
            configuration,
            pylon.RegistrationMode_Append,
            pylon.Cleanup_None,
        )
        camera.Attach(pylon.FirstFound)
        camera.Open()
        print("Using device:", camera.DeviceInfo.ModelName)

        mean_image = acquire_mean_image(camera)
        mean_gray_value = float(mean_image.mean())
        pixel_min, pixel_max = get_pixel_dynamic_range(camera, mean_image)

        is_valid, mean_percent, warning = evaluate_brightness(
            args.mode, mean_gray_value, pixel_min, pixel_max
        )
        print("\nAcquisition statistics:")
        print(f"  Pixel dynamic range (DN): {pixel_min:.0f} .. {pixel_max:.0f}")
        print(f"  Average gray value (DN): {mean_gray_value:.2f}  ({mean_percent:.1f}% of range)")
        if warning:
            print(f"  WARNING: {warning}", file=sys.stderr)
        if not is_valid and not args.force:
            raise RuntimeError(
                "Acquisition brightness out of range. Re-run with corrected illumination "
                "or pass -f/--force to continue."
            )

        if args.mode == "hot":
            outliers, _background_mean, _threshold = detect_hot_pixels(mean_image, args.threshold_hot_dn)
        else:
            outliers, _threshold = detect_cold_pixels(mean_image, args.threshold_dark_dn)
        print_outlier_report(outliers)

        detected_pixels = outliers_to_coordinates(outliers)
        if args.dry_run:
            print("\nDry run: camera user static-defect list not updated.")
        else:
            written_count = update_user_defect_list(camera, detected_pixels)
            print(f"\nEntries written to user static-defect list: {written_count}")

except Exception as e:
    print("An exception occurred:", e)
    import traceback
    traceback.print_exc()
    exit_code = 1

sys.exit(exit_code)

