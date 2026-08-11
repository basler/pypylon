"""\
This unit test checks the mapped pypylon API introduced by `src/pylon/ImageFormatConverter.i`.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon, genicam
import unittest
import warnings
import numpy as np


IGNORED_NAMES_ON_PYLON = (
    "CImageFormatConverter",
    "CImageFormatConverterImpl",
    "CImageFormatConverterParams_Params",
    "Basler_ImageFormatConverterParams",
    "IOutputPixelFormatEnum",
)

EXPECTED_IMAGE_FORMAT_CONVERTER_MEMBERS = (
    "Convert",
    "ConvertToArray",
    "ImageHasDestinationFormat",
    "SetOutputPixelFormat",
    "GetOutputPixelFormat",
    "OutputPixelFormat",
    "GetBufferSizeForConversion",
    "GetNodeMap",
    "Initialize",
    "IsInitialized",
    "IsSupportedInputFormat",
    "IsSupportedOutputFormat",
    "Uninitialize",
)

EXPECTED_FEATURE_NAMES = (
    "AdditionalLeftShift",
    "Gamma",
    "InconvertibleEdgeHandling",
    "MaxNumThreads",
    "MonoConversionMethod",
    "OutputBitAlignment",
    "OutputOrientation",
    "OutputPaddingX",
)


class ImageFormatConverterTestSuite(PylonEmuTestCase):

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def setUp(self):
        self._grab_results = []

    def tearDown(self):
        for grab_result in self._grab_results:
            try:
                # Grab results from camera devices typically occupy a buffer pool slot or several MB of memory,
                # so it is good practice to always release them explicitly when they are no longer needed.
                grab_result.Release()
            except Exception:
                pass

    def _grab_one_mono8(self):
        """Grab a single Mono8 frame from the emulator and return the grab result."""
        with pylon.InstantCamera(
            pylon.TlFactory.GetInstance().CreateFirstDevice(self.device_filter[0])
        ) as camera:
            grab_result = camera.GrabOne(5000)
        self.assertTrue(grab_result.GrabSucceeded(), "GrabOne() on emulator must succeed")
        self.assertEqual(grab_result.PixelType, pylon.PixelType_Mono8)
        self._grab_results.append(grab_result)
        return grab_result

    # ------------------------------------------------------------------
    # %rename + %ignore directives
    #     %rename(ImageFormatConverter) Pylon::CImageFormatConverter;
    #     %ignore CImageFormatConverterImpl;
    #     %ignore CImageFormatConverterParams_Params;
    #     %ignore Basler_ImageFormatConverterParams;
    #     %ignore Pylon::CImageFormatConverter::IOutputPixelFormatEnum;
    #     %ignore Pylon::CImageFormatConverter::Convert;
    #     %ignore Pylon::CImageFormatConverter::ImageHasDestinationFormat;
    #     %ignore Pylon::CImageFormatConverter::OutputPixelFormat;
    # ------------------------------------------------------------------

    def test_renamed_class_is_exposed(self):
        """ImageFormatConverter.i exposes the renamed ImageFormatConverter class on pylon."""
        self.assertTrue(hasattr(pylon, "ImageFormatConverter"))
        self.assertIsInstance(pylon.ImageFormatConverter, type)

    def test_original_names_are_hidden(self):
        """C-prefixed / implementation-detail class names are not exposed on pylon."""
        for ignored in IGNORED_NAMES_ON_PYLON:
            with self.subTest(name=ignored):
                self.assertFalse(
                    hasattr(pylon, ignored),
                    "pylon.%s should be hidden by %%rename / %%ignore" % ignored,
                )

    def test_ioutput_pixel_format_enum_nested_class_is_hidden(self):
        """The nested IOutputPixelFormatEnum class is not exposed on ImageFormatConverter."""
        self.assertFalse(hasattr(pylon.ImageFormatConverter, "IOutputPixelFormatEnum"))

    def test_raw_output_pixel_format_member_is_hidden(self):
        """The raw OutputPixelFormat data member is %%ignore-d; only the PROP_GETSET property is visible."""
        converter = pylon.ImageFormatConverter()
        descriptor = type(converter).__dict__.get("OutputPixelFormat")
        self.assertIsNotNone(
            descriptor,
            "OutputPixelFormat must be exposed (as the PROP_GETSET property, not the raw member)",
        )
        self.assertIsInstance(descriptor, property)

    # ------------------------------------------------------------------
    # Public method / property surface on pylon.ImageFormatConverter
    # ------------------------------------------------------------------

    def test_image_format_converter_method_surface_matches_expected(self):
        """pylon.ImageFormatConverter exposes exactly the expected set of public methods/properties."""
        runtime = frozenset(
            name for name in dir(pylon.ImageFormatConverter)
            if not name.startswith("_") and name != "thisown"
        )
        expected = frozenset(EXPECTED_IMAGE_FORMAT_CONVERTER_MEMBERS)
        missing = expected - runtime
        unexpected = runtime - expected
        self.assertFalse(missing, "missing on ImageFormatConverter: %s" % sorted(missing))
        self.assertFalse(unexpected, "unexpected on ImageFormatConverter: %s" % sorted(unexpected))

    def test_image_format_converter_methods_are_callable(self):
        """Every non-property method in the contract resolves to a callable on an instance."""
        converter = pylon.ImageFormatConverter()
        self.assertTrue(callable(converter.Convert))
        self.assertTrue(callable(converter.ImageHasDestinationFormat))
        self.assertTrue(callable(converter.SetOutputPixelFormat))
        self.assertTrue(callable(converter.GetOutputPixelFormat))
        self.assertTrue(callable(converter.GetBufferSizeForConversion))
        self.assertTrue(callable(converter.GetNodeMap))
        self.assertTrue(callable(converter.Initialize))
        self.assertTrue(callable(converter.IsInitialized))
        self.assertTrue(callable(converter.IsSupportedInputFormat))
        self.assertTrue(callable(converter.IsSupportedOutputFormat))
        self.assertTrue(callable(converter.Uninitialize))

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def test_default_construction(self):
        """Default construction produces a usable ImageFormatConverter instance."""
        converter = pylon.ImageFormatConverter()
        self.assertIsInstance(converter, pylon.ImageFormatConverter)

    def test_independent_instances_are_not_shared(self):
        """Two ImageFormatConverter instances are independent Python objects."""
        a = pylon.ImageFormatConverter()
        b = pylon.ImageFormatConverter()
        self.assertIsNot(a, b)
        a.OutputPixelFormat = pylon.PixelType_Mono8
        b.OutputPixelFormat = pylon.PixelType_RGB8packed
        self.assertEqual(a.OutputPixelFormat, pylon.PixelType_Mono8)
        self.assertEqual(b.OutputPixelFormat, pylon.PixelType_RGB8packed)

    # ------------------------------------------------------------------
    # %pythoncode legacy string constants
    # (InconvertibleEdgeHandling_*, MonoConversionMethod_*,
    #  OutputBitAlignment_*, OutputOrientation_*)
    # ------------------------------------------------------------------

    def test_legacy_string_constants_are_exposed_with_exact_values(self):
        """Every legacy *_ string constant is exposed on pylon with its documented string value."""
        self.assertEqual(pylon.InconvertibleEdgeHandling_Clip, "Clip")
        self.assertEqual(pylon.InconvertibleEdgeHandling_Extend, "Extend")
        self.assertEqual(pylon.InconvertibleEdgeHandling_SetZero, "SetZero")
        self.assertEqual(pylon.MonoConversionMethod_Gamma, "Gamma")
        self.assertEqual(pylon.MonoConversionMethod_Truncate, "Truncate")
        self.assertEqual(pylon.OutputBitAlignment_LsbAligned, "LsbAligned")
        self.assertEqual(pylon.OutputBitAlignment_MsbAligned, "MsbAligned")
        self.assertEqual(pylon.OutputOrientation_BottomUp, "BottomUp")
        self.assertEqual(pylon.OutputOrientation_TopDown, "TopDown")
        self.assertEqual(pylon.OutputOrientation_Unchanged, "Unchanged")

    def test_legacy_string_constants_match_feature_symbolics(self):
        """Every legacy *_ string constant equals one of the symbolics of its target feature."""
        converter = pylon.ImageFormatConverter()
        nodemap = converter.GetNodeMap()
        edge_handling = list(nodemap.GetNode("InconvertibleEdgeHandling").GetSymbolics())
        self.assertIn(pylon.InconvertibleEdgeHandling_Clip, edge_handling)
        self.assertIn(pylon.InconvertibleEdgeHandling_Extend, edge_handling)
        self.assertIn(pylon.InconvertibleEdgeHandling_SetZero, edge_handling)

        mono_conversion = list(nodemap.GetNode("MonoConversionMethod").GetSymbolics())
        self.assertIn(pylon.MonoConversionMethod_Gamma, mono_conversion)
        self.assertIn(pylon.MonoConversionMethod_Truncate, mono_conversion)

        bit_alignment = list(nodemap.GetNode("OutputBitAlignment").GetSymbolics())
        self.assertIn(pylon.OutputBitAlignment_LsbAligned, bit_alignment)
        self.assertIn(pylon.OutputBitAlignment_MsbAligned, bit_alignment)

        orientation = list(nodemap.GetNode("OutputOrientation").GetSymbolics())
        self.assertIn(pylon.OutputOrientation_BottomUp, orientation)
        self.assertIn(pylon.OutputOrientation_TopDown, orientation)
        self.assertIn(pylon.OutputOrientation_Unchanged, orientation)

    def test_legacy_string_constants_are_usable_to_configure_node_map(self):
        """Writing a legacy *_ constant via the node map yields a matching round-trip read."""
        converter = pylon.ImageFormatConverter()
        converter.InconvertibleEdgeHandling.Value = pylon.InconvertibleEdgeHandling_Clip
        self.assertEqual(
            converter.InconvertibleEdgeHandling.Value, pylon.InconvertibleEdgeHandling_Clip,
        )
        converter.MonoConversionMethod.Value = pylon.MonoConversionMethod_Gamma
        self.assertEqual(
            converter.MonoConversionMethod.Value, pylon.MonoConversionMethod_Gamma,
        )
        converter.OutputBitAlignment.Value = pylon.OutputBitAlignment_MsbAligned
        self.assertEqual(
            converter.OutputBitAlignment.Value, pylon.OutputBitAlignment_MsbAligned,
        )
        converter.OutputOrientation.Value = pylon.OutputOrientation_TopDown
        self.assertEqual(
            converter.OutputOrientation.Value, pylon.OutputOrientation_TopDown,
        )

    # ------------------------------------------------------------------
    # OutputPixelFormat: Set/Get methods and PROP_GETSET property
    # ------------------------------------------------------------------

    def test_get_output_pixel_format_returns_an_integer(self):
        """GetOutputPixelFormat() returns an EPixelType integer."""
        converter = pylon.ImageFormatConverter()
        self.assertIsInstance(converter.GetOutputPixelFormat(), int)

    def test_set_output_pixel_format_round_trips_via_getter(self):
        """SetOutputPixelFormat(v) is observable through GetOutputPixelFormat()."""
        converter = pylon.ImageFormatConverter()
        for pixel_type in (
            pylon.PixelType_Mono8, pylon.PixelType_Mono16,
            pylon.PixelType_RGB8packed, pylon.PixelType_BGR8packed,
        ):
            with self.subTest(pixel_type=pixel_type):
                converter.SetOutputPixelFormat(pixel_type)
                self.assertEqual(converter.GetOutputPixelFormat(), pixel_type)

    def test_output_pixel_format_property_getter_matches_method(self):
        """The OutputPixelFormat property returns the same value as GetOutputPixelFormat()."""
        converter = pylon.ImageFormatConverter()
        converter.SetOutputPixelFormat(pylon.PixelType_RGB8packed)
        self.assertEqual(converter.OutputPixelFormat, converter.GetOutputPixelFormat())

    def test_output_pixel_format_property_setter_writes_through_set_method(self):
        """Assigning to the OutputPixelFormat property routes through SetOutputPixelFormat."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        self.assertEqual(converter.GetOutputPixelFormat(), pylon.PixelType_Mono16)

    def test_output_pixel_format_property_roundtrip_for_representative_supported_formats(self):
        """OutputPixelFormat round-trips for a small contrast set of supported output formats."""
        converter = pylon.ImageFormatConverter()
        candidates = (
            pylon.PixelType_Mono8,
            pylon.PixelType_Mono16,
            pylon.PixelType_RGB8packed,
            pylon.PixelType_BGR8packed,
            pylon.PixelType_RGB16packed,
            pylon.PixelType_YUV422packed,
        )
        tested = 0
        for pixel_type in candidates:
            if converter.IsSupportedOutputFormat(pixel_type):
                with self.subTest(pixel_type=pixel_type):
                    converter.OutputPixelFormat = pixel_type
                    self.assertEqual(converter.OutputPixelFormat, pixel_type)
                tested += 1
        self.assertGreater(
            tested, 0, "no candidate EPixelType accepted as output; unable to exercise roundtrip",
        )

    # ------------------------------------------------------------------
    # GetNodeMap typemap: returns NodeMapWrapper with
    # NodeMapType_ImageFormatConverter ("ImageFormatConverter").
    # ------------------------------------------------------------------

    def test_get_node_map_returns_inodemapwrapper(self):
        """GetNodeMap() returns a pylon.NodeMapWrapper instance."""
        converter = pylon.ImageFormatConverter()
        self.assertIsInstance(converter.GetNodeMap(), pylon.NodeMapWrapper)

    def test_get_node_map_wrapper_reports_image_format_converter_type(self):
        """GetNodeMap() wrapper reports NodeMapType_ImageFormatConverter as its type."""
        converter = pylon.ImageFormatConverter()
        self.assertEqual(
            converter.GetNodeMap().GetNodeMapType(),
            pylon.NodeMapType_ImageFormatConverter,
        )

    def test_get_node_map_wrapper_reports_image_format_converter_type_string(self):
        """GetNodeMap() wrapper reports 'ImageFormatConverter' as its string type."""
        converter = pylon.ImageFormatConverter()
        self.assertEqual(
            converter.GetNodeMap().GetNodeMapTypeString(), "ImageFormatConverter",
        )

    def test_get_node_map_exposes_every_expected_feature(self):
        """GetNodeMap() exposes the expected ImageFormatConverter feature names."""
        converter = pylon.ImageFormatConverter()
        nodemap = converter.GetNodeMap()
        feature_names = set()
        for n in nodemap.GetNodes():
            try:
                node = n.GetNode()
                if node.IsFeature():
                    feature_names.add(node.GetName())
            except Exception:  # noqa: BLE001
                pass
        missing = set(EXPECTED_FEATURE_NAMES) - feature_names
        self.assertFalse(
            missing, "feature(s) missing from GetNodeMap(): %s" % sorted(missing),
        )

    # ------------------------------------------------------------------
    # __getattr__ shim: three explicit branches
    #   1. attribute in self.__dict__ / "thisown" / "this" / dunder
    #        -> object.__getattr__  (hasattr-friendly AttributeError for
    #                                 missing dunders)
    #   2. real feature name
    #        -> _LookupParameter returns the node-map parameter
    #   3. unknown (non-dunder) attribute
    #        -> _LookupParameter raises genicam.LogicalErrorException
    # ------------------------------------------------------------------

    def test_getattr_feature_returns_parameter_object(self):
        """Reading a real feature name returns the matching node-map feature parameter."""
        converter = pylon.ImageFormatConverter()
        feat = converter.InconvertibleEdgeHandling
        self.assertTrue(hasattr(feat, "Value"))
        self.assertTrue(hasattr(feat, "GetSymbolics"))

    def test_getattr_feature_value_roundtrip(self):
        """Reading-then-writing a feature's Value through __getattr__ roundtrips."""
        converter = pylon.ImageFormatConverter()
        converter.InconvertibleEdgeHandling.Value = "Extend"
        self.assertEqual(converter.InconvertibleEdgeHandling.Value, "Extend")

    def test_getattr_thisown_bypasses_node_map_lookup(self):
        """Reading 'thisown' is served from the SWIG instance state, not routed through _LookupParameter."""
        converter = pylon.ImageFormatConverter()
        self.assertIsInstance(converter.thisown, bool)
        self.assertTrue(converter.thisown)

    def test_getattr_this_bypasses_node_map_lookup(self):
        """Reading 'this' is served from the SWIG instance state, not routed through _LookupParameter."""
        converter = pylon.ImageFormatConverter()
        self.assertIsNotNone(converter.this)

    def test_getattr_unknown_feature_raises_genicam_logical_error(self):
        """Reading an unknown (non-dunder) attribute raises genicam.LogicalErrorException from _LookupParameter."""
        converter = pylon.ImageFormatConverter()
        for missing_name in ("DefinitelyNotAFeature", "XYZ", "OutputPixelFormatTypo"):
            with self.subTest(name=missing_name):
                with self.assertRaises(genicam.LogicalErrorException):
                    getattr(converter, missing_name)

    def test_getattr_unknown_feature_error_identifies_missing_name(self):
        """The LogicalErrorException from __getattr__ mentions the missing attribute and the node-map type."""
        converter = pylon.ImageFormatConverter()
        with self.assertRaises(genicam.LogicalErrorException) as ctx:
            converter.DefinitelyNotAFeature  # noqa: B018 - intentionally trigger __getattr__
        message = str(ctx.exception)
        self.assertIn("DefinitelyNotAFeature", message)
        self.assertIn("ImageFormatConverter", message)

    def test_getattr_unknown_feature_error_is_not_swallowed_by_hasattr(self):
        """hasattr() surfaces the LogicalErrorException for an unknown feature (not an AttributeError)."""
        converter = pylon.ImageFormatConverter()
        # genicam.LogicalErrorException is NOT a subclass of AttributeError,
        # so Python's hasattr() must not silently turn it into False.
        self.assertFalse(issubclass(genicam.LogicalErrorException, AttributeError))
        with self.assertRaises(genicam.LogicalErrorException):
            hasattr(converter, "DefinitelyNotAFeature")

    def test_getattr_non_identifier_names_also_go_through_node_map_lookup(self):
        """Even empty / non-identifier attribute names are routed to _LookupParameter (no local whitelist)."""
        converter = pylon.ImageFormatConverter()
        for bad_name in ("", " ", "not a feature", "123"):
            with self.subTest(name=repr(bad_name)):
                with self.assertRaises(genicam.LogicalErrorException):
                    getattr(converter, bad_name)

    def test_getattr_unknown_dunder_raises_attribute_error(self):
        """Reading an unknown __dunder__ attribute raises AttributeError (dunder branch, not _LookupParameter)."""
        converter = pylon.ImageFormatConverter()
        for dunder_name in ("__nosuchdunder__", "__does_not_exist__", "__missing__"):
            with self.subTest(name=dunder_name):
                with self.assertRaises(AttributeError):
                    getattr(converter, dunder_name)

    def test_hasattr_returns_false_for_unknown_dunder(self):
        """hasattr() returns False for an unknown __dunder__ attribute (the dunder branch raises AttributeError)."""
        converter = pylon.ImageFormatConverter()
        self.assertFalse(hasattr(converter, "__nosuchdunder__"))

    def test_getattr_failure_does_not_poison_later_real_feature_access(self):
        """A failed __getattr__ lookup does not prevent subsequent real feature access."""
        converter = pylon.ImageFormatConverter()
        with self.assertRaises(genicam.LogicalErrorException):
            converter.DefinitelyNotAFeature  # noqa: B018
        self.assertEqual(
            converter.InconvertibleEdgeHandling.Value,
            converter.GetNodeMap().GetNode("InconvertibleEdgeHandling").Value,
        )

    # ------------------------------------------------------------------
    # __setattr__ shim: OutputPixelFormat special-case, deprecated passthrough,
    # and dunder attributes.
    # ------------------------------------------------------------------

    def test_setattr_output_pixel_format_does_not_emit_deprecation_warning(self):
        """Assigning to OutputPixelFormat is the documented path; no DeprecationWarning is emitted."""
        converter = pylon.ImageFormatConverter()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            converter.OutputPixelFormat = pylon.PixelType_Mono8
        self.assertFalse(
            [w for w in caught if issubclass(w.category, DeprecationWarning)],
            "OutputPixelFormat assignment must not emit DeprecationWarning",
        )
        self.assertEqual(converter.GetOutputPixelFormat(), pylon.PixelType_Mono8)

    def test_setattr_generic_feature_emits_deprecation_warning(self):
        """Assigning to a generic feature emits a DeprecationWarning pointing at the node-map API."""
        converter = pylon.ImageFormatConverter()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            converter.InconvertibleEdgeHandling = "SetZero"
        dep_warnings = [w for w in caught if issubclass(w.category, DeprecationWarning)]
        self.assertEqual(len(dep_warnings), 1, "expected exactly one DeprecationWarning")
        self.assertIn("Setting a feature value by direct assignment is deprecated",
                      str(dep_warnings[0].message))

    def test_setattr_generic_feature_writes_through_to_node_map(self):
        """Despite the deprecation warning, the generic setattr path updates the underlying node."""
        converter = pylon.ImageFormatConverter()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            converter.MonoConversionMethod = "Truncate"
        self.assertEqual(
            converter.GetNodeMap().GetNode("MonoConversionMethod").Value, "Truncate",
        )

    def test_setattr_dunder_attribute_bypasses_feature_path(self):
        """Assigning a __dunder__ attribute is routed to object.__setattr__ (no warning, stored on the instance)."""
        converter = pylon.ImageFormatConverter()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            converter.__custom_dunder__ = "sentinel"
        self.assertFalse(
            [w for w in caught if issubclass(w.category, DeprecationWarning)],
            "dunder-attribute assignment must not emit DeprecationWarning",
        )
        self.assertEqual(converter.__custom_dunder__, "sentinel")

    # ------------------------------------------------------------------
    # __dir__ shim: merges class members + feature names.
    # ------------------------------------------------------------------

    def test_dir_contains_class_level_methods(self):
        """dir(converter) includes every method advertised by the ImageFormatConverter contract."""
        converter = pylon.ImageFormatConverter()
        members = set(dir(converter))
        for name in EXPECTED_IMAGE_FORMAT_CONVERTER_MEMBERS:
            with self.subTest(name=name):
                self.assertIn(name, members)

    def test_dir_contains_node_map_feature_names(self):
        """dir(converter) includes every feature name reported by GetNodeMap()."""
        converter = pylon.ImageFormatConverter()
        members = set(dir(converter))
        for feature in EXPECTED_FEATURE_NAMES:
            with self.subTest(feature=feature):
                self.assertIn(feature, members)

    def test_dir_is_sorted_and_deduplicated(self):
        """dir(converter) returns a sorted list with no duplicates (per the __dir__ shim)."""
        converter = pylon.ImageFormatConverter()
        members = dir(converter)
        self.assertEqual(members, sorted(members))
        self.assertEqual(len(members), len(set(members)))

    # ------------------------------------------------------------------
    # IsSupportedInputFormat / IsSupportedOutputFormat
    # ------------------------------------------------------------------

    def test_is_supported_input_format_accepts_mono8(self):
        """IsSupportedInputFormat(PixelType_Mono8) is True."""
        converter = pylon.ImageFormatConverter()
        self.assertTrue(converter.IsSupportedInputFormat(pylon.PixelType_Mono8))

    def test_is_supported_input_format_rejects_undefined(self):
        """IsSupportedInputFormat(PixelType_Undefined) is False."""
        converter = pylon.ImageFormatConverter()
        self.assertFalse(converter.IsSupportedInputFormat(pylon.PixelType_Undefined))

    def test_is_supported_output_format_accepts_mono8(self):
        """IsSupportedOutputFormat(PixelType_Mono8) is True."""
        converter = pylon.ImageFormatConverter()
        self.assertTrue(converter.IsSupportedOutputFormat(pylon.PixelType_Mono8))

    def test_is_supported_output_format_rejects_undefined(self):
        """IsSupportedOutputFormat(PixelType_Undefined) is False."""
        converter = pylon.ImageFormatConverter()
        self.assertFalse(converter.IsSupportedOutputFormat(pylon.PixelType_Undefined))

    # ------------------------------------------------------------------
    # IsInitialized / Initialize / Uninitialize (from
    # <pylon/ImageFormatConverter.h>).
    # ------------------------------------------------------------------

    def test_is_initialized_returns_bool(self):
        """IsInitialized(pixelType) returns a bool."""
        converter = pylon.ImageFormatConverter()
        self.assertIsInstance(converter.IsInitialized(pylon.PixelType_Mono8), bool)

    def test_initialize_accepts_supported_input_format(self):
        """Initialize(pixelType) does not raise for a supported input pixel type."""
        converter = pylon.ImageFormatConverter()
        converter.Initialize(pylon.PixelType_Mono8)

    def test_uninitialize_is_callable_without_arguments(self):
        """Uninitialize() is callable with no arguments and does not raise."""
        converter = pylon.ImageFormatConverter()
        converter.Initialize(pylon.PixelType_Mono8)
        converter.Uninitialize()

    def test_is_initialized_requires_pixel_type_argument(self):
        """IsInitialized() without arguments is a TypeError (required sourcePixelType)."""
        converter = pylon.ImageFormatConverter()
        with self.assertRaises(TypeError):
            converter.IsInitialized()

    # ------------------------------------------------------------------
    # GetBufferSizeForConversion (from <pylon/ImageFormatConverter.h>).
    # ------------------------------------------------------------------

    def test_get_buffer_size_for_conversion_returns_positive_size(self):
        """GetBufferSizeForConversion returns a positive destination size for a supported conversion."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        size = converter.GetBufferSizeForConversion(pylon.PixelType_Mono8, 64, 48)
        self.assertIsInstance(size, int)
        # Mono8 -> Mono16: 64 * 48 * 2 = 6144 bytes is the minimum.
        self.assertGreaterEqual(size, 64 * 48 * 2)

    # ------------------------------------------------------------------
    # %extend Convert: IImage / CGrabResultPtr overloads.  At runtime the
    # wrapper accepts a single source argument and returns a newly-owned
    # pylon.PylonImage with the converted pixels.
    # ------------------------------------------------------------------

    def test_convert_from_grab_result_returns_new_pylon_image(self):
        """Convert(grab_result) returns a newly-allocated, owned pylon.PylonImage."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        grab_result = self._grab_one_mono8()
        dst = converter.Convert(grab_result)
        self.assertIsInstance(dst, pylon.PylonImage)
        self.assertTrue(dst.thisown, "returned image must own its C++ instance")
        self.assertEqual(dst.PixelType, pylon.PixelType_Mono16)
        self.assertEqual(dst.Width,  grab_result.Width)
        self.assertEqual(dst.Height, grab_result.Height)

    def test_convert_from_iimage_returns_new_pylon_image(self):
        """Convert(iimage_src) also works when the source is an IImage (PylonImage)."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        grab_result = self._grab_one_mono8()
        # Turn the grab result into a standalone IImage (PylonImage) first.
        src = converter.Convert(grab_result)
        # Now round-trip through another converter that does Mono16 -> Mono8.
        converter2 = pylon.ImageFormatConverter()
        converter2.OutputPixelFormat = pylon.PixelType_Mono8
        dst = converter2.Convert(src)
        self.assertIsInstance(dst, pylon.PylonImage)
        self.assertTrue(dst.thisown)
        self.assertEqual(dst.PixelType, pylon.PixelType_Mono8)
        self.assertEqual(dst.Width,  src.Width)
        self.assertEqual(dst.Height, src.Height)

    def test_convert_from_pylon_image_attached_to_grab_result_buffer(self):
        """Convert(pylon_image) works when the source is a PylonImage wrapping a grab result buffer."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        grab_result = self._grab_one_mono8()
        image = pylon.PylonImage()
        image.AttachGrabResultBuffer(grab_result)
        try:
            self.assertTrue(image.IsValid())
            dst = converter.Convert(image)
            self.assertIsInstance(dst, pylon.PylonImage)
            self.assertTrue(dst.thisown)
            self.assertEqual(dst.PixelType, pylon.PixelType_Mono16)
            self.assertEqual(dst.Width,  grab_result.Width)
            self.assertEqual(dst.Height, grab_result.Height)
        finally:
            image.Release()

    def test_convert_from_pylon_data_component(self):
        """Convert(component) works when the source is a PylonDataComponent from GetFirstImageDataComponent()."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        grab_result = self._grab_one_mono8()
        component = grab_result.GetFirstImageDataComponent()
        try:
            self.assertTrue(component.IsValid())
            dst = converter.Convert(component)
            self.assertIsInstance(dst, pylon.PylonImage)
            self.assertTrue(dst.thisown)
            self.assertEqual(dst.PixelType, pylon.PixelType_Mono16)
            self.assertEqual(dst.Width,  grab_result.Width)
            self.assertEqual(dst.Height, grab_result.Height)
        finally:
            component.Release()

    def test_convert_returns_independent_images_on_each_call(self):
        """Calling Convert twice yields two distinct, independently-owned pylon.PylonImage instances."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        grab_result = self._grab_one_mono8()
        a = converter.Convert(grab_result)
        b = converter.Convert(grab_result)
        self.assertIsNot(a, b)
        self.assertTrue(a.thisown)
        self.assertTrue(b.thisown)
        # Sanity: destroying one does not invalidate the other.
        del a
        self.assertEqual(b.PixelType, pylon.PixelType_Mono16)

    def test_convert_result_outlives_source_converter(self):
        """The PylonImage returned by Convert stays valid after the converter is dropped."""
        grab_result = self._grab_one_mono8()
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        dst = converter.Convert(grab_result)
        del converter
        self.assertEqual(dst.PixelType, pylon.PixelType_Mono16)
        self.assertEqual(dst.Width,  grab_result.Width)
        self.assertEqual(dst.Height, grab_result.Height)

    def test_convert_rejects_unsupported_source_types(self):
        """Convert with a non-image argument raises a TypeError from SWIG's overload resolver."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono8
        for bad in ("astring", 123, 3.14, None, [1, 2, 3], (b"bytes-tuple",)):
            with self.subTest(arg=repr(bad)):
                with self.assertRaises(TypeError):
                    converter.Convert(bad)

    # ------------------------------------------------------------------
    # %extend ImageHasDestinationFormat: IImage / CGrabResultPtr overloads.
    # ------------------------------------------------------------------

    def test_image_has_destination_format_true_when_output_matches_source(self):
        """ImageHasDestinationFormat returns True when the source already has the converter's output format."""
        grab_result = self._grab_one_mono8()  # grab_result.PixelType == PixelType_Mono8
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono8
        self.assertTrue(converter.ImageHasDestinationFormat(grab_result))

    def test_image_has_destination_format_false_when_output_differs_from_source(self):
        """ImageHasDestinationFormat returns False when the source has a different format than the output."""
        grab_result = self._grab_one_mono8()
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_RGB8packed
        self.assertFalse(converter.ImageHasDestinationFormat(grab_result))

    def test_image_has_destination_format_accepts_iimage_source(self):
        """ImageHasDestinationFormat also accepts an IImage (PylonImage) source."""
        grab_result = self._grab_one_mono8()
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_RGB8packed
        converted = converter.Convert(grab_result)
        self.assertTrue(converter.ImageHasDestinationFormat(converted))

    def test_image_has_destination_format_rejects_unsupported_argument_types(self):
        """ImageHasDestinationFormat with a non-image argument raises a TypeError."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono8
        for bad in ("astring", 123, 3.14, None, [1, 2, 3], (b"bytes-tuple",)):
            with self.subTest(arg=repr(bad)):
                with self.assertRaises(TypeError):
                    converter.ImageHasDestinationFormat(bad)

    # ------------------------------------------------------------------
    # Backwards compatability
    # ------------------------------------------------------------------

    def test_backwards_compatibility_direct_assignment(self):
        """Setting a parameter value using direct assignment instead of using the .Value property."""
        converter = pylon.ImageFormatConverter()
        with self.assertWarns(DeprecationWarning):
            converter.InconvertibleEdgeHandling = pylon.InconvertibleEdgeHandling_Extend
        self.assertEqual(converter.InconvertibleEdgeHandling.Value, pylon.InconvertibleEdgeHandling_Extend)
        with self.assertWarns(DeprecationWarning):
            converter.InconvertibleEdgeHandling = pylon.InconvertibleEdgeHandling_Clip
        self.assertEqual(converter.InconvertibleEdgeHandling.Value, pylon.InconvertibleEdgeHandling_Clip)

    # ------------------------------------------------------------------
    # ConvertToArray: zero-copy numpy array output
    # ------------------------------------------------------------------

    def test_convert_to_array_is_callable(self):
        """ConvertToArray is callable on an ImageFormatConverter instance."""
        converter = pylon.ImageFormatConverter()
        self.assertTrue(callable(converter.ConvertToArray))

    def test_convert_to_array_from_grab_result_returns_ndarray(self):
        """ConvertToArray(grab_result) returns a numpy ndarray."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono8
        grab_result = self._grab_one_mono8()
        result = converter.ConvertToArray(grab_result)
        self.assertIsInstance(result, np.ndarray)

    def test_convert_to_array_shape_matches_output_pixel_format(self):
        """ConvertToArray returns an array whose shape matches the converter output format."""
        grab_result = self._grab_one_mono8()
        width = grab_result.Width
        height = grab_result.Height

        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono8
        result = converter.ConvertToArray(grab_result)
        self.assertEqual(result.shape, (height, width))
        self.assertEqual(result.dtype, np.uint8)

    def test_convert_to_array_rgb_shape_has_channel_dimension(self):
        """ConvertToArray with RGB8packed output yields an (H, W, 3) uint8 array."""
        grab_result = self._grab_one_mono8()
        width = grab_result.Width
        height = grab_result.Height

        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_RGB8packed
        result = converter.ConvertToArray(grab_result)
        self.assertEqual(result.shape, (height, width, 3))
        self.assertEqual(result.dtype, np.uint8)

    def test_convert_to_array_pixel_values_match_convert_array(self):
        """ConvertToArray produces the same pixel values as converter.Convert(src).Array."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        grab_result = self._grab_one_mono8()

        expected = converter.Convert(grab_result).Array
        result = converter.ConvertToArray(grab_result)
        np.testing.assert_array_equal(result, expected)

    def test_convert_to_array_raw_returns_flat_uint8(self):
        """ConvertToArray(src, raw=True) returns a flat uint8 array of the converted bytes."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        grab_result = self._grab_one_mono8()

        result = converter.ConvertToArray(grab_result, raw=True)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.ndim, 1)
        self.assertEqual(result.dtype, np.uint8)

    def test_convert_to_array_raw_byte_length_matches_buffer_size(self):
        """ConvertToArray(src, raw=True) length matches GetBufferSizeForConversion."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        grab_result = self._grab_one_mono8()

        expected_size = converter.GetBufferSizeForConversion(
            grab_result.PixelType, grab_result.Width, grab_result.Height
        )
        result = converter.ConvertToArray(grab_result, raw=True)
        self.assertEqual(result.size, expected_size)

    def test_convert_to_array_result_is_independent_ndarray(self):
        """Each ConvertToArray call returns an independently-owned ndarray."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        grab_result = self._grab_one_mono8()

        first = converter.ConvertToArray(grab_result)
        second = converter.ConvertToArray(grab_result)
        self.assertIsNot(first, second)
        # Modifying one must not affect the other.
        first.fill(0)
        self.assertFalse(np.array_equal(first, second))

    def test_convert_to_array_from_pylon_image(self):
        """ConvertToArray accepts a PylonImage as source."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        grab_result = self._grab_one_mono8()
        source_image = converter.Convert(grab_result)

        converter2 = pylon.ImageFormatConverter()
        converter2.OutputPixelFormat = pylon.PixelType_Mono8
        result = converter2.ConvertToArray(source_image)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.dtype, np.uint8)

    def test_convert_to_array_from_pylon_data_component(self):
        """ConvertToArray accepts a PylonDataComponent as source."""
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        grab_result = self._grab_one_mono8()
        component = grab_result.GetFirstImageDataComponent()
        try:
            result = converter.ConvertToArray(component)
            self.assertIsInstance(result, np.ndarray)
            self.assertEqual(result.shape, (grab_result.Height, grab_result.Width))
        finally:
            component.Release()

    # ------------------------------------------------------------------
    # ConvertToArray: packed output format
    # ------------------------------------------------------------------

    def _first_supported_packed_output(self):
        """Return the first packed EPixelType accepted by the SDK as output, or None."""
        packed_candidates = (
            pylon.PixelType_Mono10packed,
            pylon.PixelType_Mono12packed,
        )
        for pt in packed_candidates:
            converter = pylon.ImageFormatConverter()
            if converter.IsSupportedOutputFormat(pt):
                return pt
        return None

    def test_convert_to_array_raises_for_packed_output_when_not_raw(self):
        """ConvertToArray raises ValueError for a packed OutputPixelFormat when raw=False."""
        packed_pt = self._first_supported_packed_output()
        if packed_pt is None:
            self.skipTest("No packed output format accepted by this SDK build")
        grab_result = self._grab_one_mono8()
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = packed_pt
        with self.assertRaises(ValueError):
            converter.ConvertToArray(grab_result, raw=False)

    def test_convert_to_array_packed_error_message_mentions_packed(self):
        """The ValueError for a packed OutputPixelFormat with raw=False mentions 'acked'."""
        packed_pt = self._first_supported_packed_output()
        if packed_pt is None:
            self.skipTest("No packed output format accepted by this SDK build")
        grab_result = self._grab_one_mono8()
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = packed_pt
        with self.assertRaises(ValueError) as ctx:
            converter.ConvertToArray(grab_result, raw=False)
        self.assertIn("acked", str(ctx.exception))

    def test_convert_to_array_packed_output_succeeds_when_raw_true(self):
        """ConvertToArray with raw=True returns a flat uint8 array even for packed OutputPixelFormat."""
        packed_pt = self._first_supported_packed_output()
        if packed_pt is None:
            self.skipTest("No packed output format accepted by this SDK build")
        grab_result = self._grab_one_mono8()
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = packed_pt
        result = converter.ConvertToArray(grab_result, raw=True)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.ndim, 1)
        self.assertEqual(result.dtype, np.uint8)


if __name__ == "__main__":
    unittest.main()
