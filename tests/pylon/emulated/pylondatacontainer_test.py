"""\
This unit test checks the mapped pypylon PylonDataContainer and
PylonDataComponent API introduced by src/pylon/PylonDataContainer.i and
src/pylon/PylonDataComponent.i.  Tests are usage-centric: each test method
exercises a coherent group of related methods so that the overall number
of tests stays manageable while still covering every public method and
property.
"""
from pylonemutestcase import PylonEmuTestCase
from pypylon import pylon
from pypylon import genicam
import tempfile
import unittest
import os


class DataContainerTestSuite(PylonEmuTestCase):

    def _grab_one(self, gen_dc=False):
        """Open the first emulator camera and return a single grab result."""
        with self.create_first() as camera:
            if gen_dc:
                camera.GenDC.Value = True
            return camera.GrabOne(5000)

    def _tmp_path(self, suffix):
        """Return a temporary file path with a unicode prefix and the given suffix.

        The unicode prefix (e.g. 'pylön_') exercises unicode path support in Save/Load.
        The file is created and immediately unlinked so the caller owns the path.
        """
        fd, path = tempfile.mkstemp(prefix="pylön_", suffix=suffix)
        os.close(fd)
        os.unlink(path)
        return path

    def _assert_components_equivalent(self, expected, actual):
        """Field-by-field equality of two PylonDataComponent instances, including data bytes."""
        self.assertEqual(expected.IsValid(), actual.IsValid())
        self.assertEqual(expected.ComponentType, actual.ComponentType)
        self.assertEqual(expected.GetComponentIndex(), actual.GetComponentIndex())
        self.assertEqual(expected.PixelType, actual.PixelType)
        self.assertEqual(expected.Width, actual.Width)
        self.assertEqual(expected.Height, actual.Height)
        self.assertEqual(expected.OffsetX, actual.OffsetX)
        self.assertEqual(expected.OffsetY, actual.OffsetY)
        self.assertEqual(expected.PaddingX, actual.PaddingX)
        self.assertEqual(expected.DataSize, actual.DataSize)
        self.assertEqual(expected.TimeStamp, actual.TimeStamp)
        self.assertEqual(expected.GetData(), actual.GetData())
        self.assertEqual(expected.GetSourceId(), actual.GetSourceId())

    # ------------------------------------------------------------------
    # Default construction
    # ------------------------------------------------------------------

    def test_empty_container(self):
        """A default-constructed container reports zero components and rejects index lookups."""
        testee = pylon.PylonDataContainer()
        self.assertEqual(testee.DataComponentCount, 0)
        self.assertEqual(testee.GetDataComponentCount(), 0)
        testee.Release()
        with self.assertRaises(genicam.OutOfRangeException):
            testee.GetDataComponentByIndex(0)

    def test_empty_container_copy(self):
        """Copy-constructing an empty container yields another empty container."""
        empty = pylon.PylonDataContainer()
        assigned = pylon.PylonDataContainer(empty)
        self.assertEqual(assigned.DataComponentCount, empty.DataComponentCount)
        self.assertEqual(assigned.GetDataComponentCount(), 0)
        with self.assertRaises(genicam.OutOfRangeException):
            assigned.GetDataComponentByIndex(1)

    def test_empty_container_component(self):
        """A default-constructed component is invalid and reports zero/undefined for every metadata field."""
        testee = pylon.PylonDataComponent()
        self.assertEqual(testee.PixelType, pylon.PixelType_Undefined)
        self.assertEqual(testee.ComponentType, 0)
        self.assertEqual(testee.IsValid(), False)
        self.assertEqual(testee.Width, 0)
        self.assertEqual(testee.Height, 0)
        self.assertEqual(testee.OffsetX, 0)
        self.assertEqual(testee.OffsetY, 0)
        self.assertEqual(testee.PaddingX, 0)
        self.assertEqual(testee.DataSize, 0)
        self.assertEqual(testee.TimeStamp, 0)
        self.assertEqual(testee.ComponentIndex, 0)
        self.assertEqual(testee.SourceId, 0)

        self.assertEqual(testee.GetComponentType(), 0)
        self.assertEqual(testee.GetPixelType(), pylon.PixelType_Undefined)
        self.assertEqual(testee.GetWidth(), 0)
        self.assertEqual(testee.GetHeight(), 0)
        self.assertEqual(testee.GetOffsetX(), 0)
        self.assertEqual(testee.GetOffsetY(), 0)
        self.assertEqual(testee.GetPaddingX(), 0)
        self.assertEqual(testee.GetDataSize(), 0)
        self.assertEqual(testee.GetTimeStamp(), 0)
        self.assertIsNone(testee.GetData())
        self.assertEqual(testee.GetStride(), [False, 0])
        self.assertEqual(testee.GetComponentIndex(), 0)
        self.assertEqual(testee.GetSourceId(), 0)

    def test_empty_container_component_copy(self):
        """Copy-constructing an empty component preserves every default field."""
        empty = pylon.PylonDataComponent()
        assigned = pylon.PylonDataComponent(empty)
        self._assert_components_equivalent(empty, assigned)
        self.assertEqual(assigned.IsValid(), False)
        self.assertEqual(assigned.PixelType, pylon.PixelType_Undefined)
        self.assertEqual(assigned.ComponentType, 0)

    # ------------------------------------------------------------------
    # Construction from file or grab result
    # ------------------------------------------------------------------

    def test_construct_from_filename(self):
        """The filename ctor is equivalent to default-construct + Load(filename)."""
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')

        testee = pylon.PylonDataContainer(filename)
        self.assertEqual(testee.DataComponentCount, 3)
        component_0 = testee.GetDataComponentByIndex(0)
        self.assertEqual(component_0.IsValid(), True)
        component_0.Release()
        testee.Release()

        with self.assertRaises(genicam.GenericException):
            pylon.PylonDataContainer("")
        with self.assertRaises(genicam.GenericException):
            pylon.PylonDataContainer("valid_but_not_existing__")

    def test_construct_from_grab_result(self):
        """A live grab result becomes a container; a failed/empty one yields zero components."""
        with self._grab_one(gen_dc=True) as grab_result_gen_dc:
            self.assertEqual(grab_result_gen_dc.PayloadType, pylon.PayloadType_GenDC)
            container_gen_dc = pylon.PylonDataContainer(grab_result_gen_dc)
            self.assertGreater(container_gen_dc.DataComponentCount, 0)
            for i in range(container_gen_dc.DataComponentCount):
                self.assertEqual(
                    container_gen_dc.GetDataComponentByIndex(i).IsValid(), True
                )
            container_gen_dc.Release()

        empty_grab_result = pylon.GrabResult()
        container_invalid = pylon.PylonDataContainer(empty_grab_result)
        self.assertEqual(container_invalid.DataComponentCount, 0)

        with self._grab_one() as grab_result_image:
            container_image = pylon.PylonDataContainer(grab_result_image)
            self.assertGreater(container_image.DataComponentCount, 0)

            intensity_components = container_image.GetDataComponentByType(
                pylon.ComponentType_Intensity
            )
            self.assertGreater(len(intensity_components), 0)
            component_intensity = intensity_components[0]

            self.assertEqual(component_intensity.IsValid(), True)
            self.assertEqual(component_intensity.ComponentType, pylon.ComponentType_Intensity)
            self.assertEqual(component_intensity.PixelType, grab_result_image.PixelType)
            self.assertEqual(component_intensity.Width, grab_result_image.Width)
            self.assertEqual(component_intensity.Height, grab_result_image.Height)
            self.assertEqual(component_intensity.OffsetX, grab_result_image.OffsetX)
            self.assertEqual(component_intensity.OffsetY, grab_result_image.OffsetY)
            self.assertEqual(component_intensity.PaddingX, grab_result_image.PaddingX)
            self.assertEqual(component_intensity.DataSize, grab_result_image.PayloadSize)
            self.assertEqual(component_intensity.TimeStamp, grab_result_image.TimeStamp)
            container_image.Release()

    # ------------------------------------------------------------------
    # Copy construction (populated)
    # ------------------------------------------------------------------

    def test_copy_construction(self):
        """Copy-constructing a populated container or component preserves every field."""
        with self._grab_one() as grab_result:
            grab_result_container = pylon.PylonDataContainer(grab_result)
            self.assertGreater(grab_result_container.DataComponentCount, 0)
            grab_result_component = grab_result_container.GetDataComponentByIndex(0)
            self.assertEqual(grab_result_component.IsValid(), True)

            copied_container = pylon.PylonDataContainer(grab_result_container)
            self.assertEqual(
                copied_container.DataComponentCount,
                grab_result_container.DataComponentCount,
            )
            copied_component = copied_container.GetDataComponentByIndex(0)
            self._assert_components_equivalent(grab_result_component, copied_component)

            copied_component_alone = pylon.PylonDataComponent(grab_result_component)
            self._assert_components_equivalent(grab_result_component, copied_component_alone)

            copied_component_alone.Release()
            copied_component.Release()
            copied_container.Release()
            grab_result_component.Release()
            grab_result_container.Release()

    # ------------------------------------------------------------------
    # Component access (by index / by type / deprecated alias)
    # ------------------------------------------------------------------

    def test_get_data_component_by_type(self):
        """GetDataComponentByType returns one match per present ComponentType and an empty list otherwise."""
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        container = pylon.PylonDataContainer(filename)
        self.assertEqual(container.DataComponentCount, 3)

        for component_type, expected_pixel in (
            (pylon.ComponentType_Range, pylon.PixelType_Coord3D_ABC32f),
            (pylon.ComponentType_Intensity, pylon.PixelType_Mono16),
            (pylon.ComponentType_Confidence, pylon.PixelType_Confidence16),
        ):
            matches = container.GetDataComponentByType(component_type)
            self.assertIsInstance(matches, list)
            self.assertEqual(len(matches), 1)
            self.assertEqual(matches[0].IsValid(), True)
            self.assertEqual(matches[0].ComponentType, component_type)
            self.assertEqual(matches[0].PixelType, expected_pixel)

        absent = container.GetDataComponentByType(pylon.ComponentType_Undefined)
        self.assertIsInstance(absent, list)
        self.assertEqual(len(absent), 0)

        container.Release()

    def test_get_data_component_deprecated(self):
        """The legacy GetDataComponent(index) alias warns and forwards to GetDataComponentByIndex."""
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        container = pylon.PylonDataContainer(filename)

        with self.assertWarnsRegex(DeprecationWarning, "GetDataComponentByIndex"):
            deprecated_comp = container.GetDataComponent(1)

        canonical_comp = container.GetDataComponentByIndex(1)
        self._assert_components_equivalent(canonical_comp, deprecated_comp)

        deprecated_comp.Release()
        canonical_comp.Release()
        container.Release()

    # ------------------------------------------------------------------
    # Loaded-fixture inspection (little_boxes.gendc)
    # ------------------------------------------------------------------

    def test_container_load(self):
        """Load() of the little_boxes.gendc fixture reproduces three components with the expected metadata and pixel data."""
        container = pylon.PylonDataContainer()
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        container.Load(filename)
        self.assertEqual(container.DataComponentCount, 3)

        range_component = container.GetDataComponentByIndex(0)
        self.assertEqual(range_component.IsValid(), True)
        self.assertEqual(range_component.PixelType, pylon.PixelType_Coord3D_ABC32f)
        self.assertEqual(range_component.ComponentType, pylon.ComponentType_Range)
        self.assertEqual(range_component.Width, 160)
        self.assertEqual(range_component.Height, 120)
        self.assertEqual(range_component.OffsetX, 80)
        self.assertEqual(range_component.OffsetY, 60)
        self.assertEqual(range_component.PaddingX, 0)
        self.assertEqual(range_component.DataSize, 230400)
        self.assertEqual(range_component.TimeStamp, 62653150103775)
        self.assertEqual(range_component.Array.shape, (120, 160, 3))
        self.assertEqual(range_component.GetData()[0], 79)
        self.assertEqual(range_component.GetMemoryView()[0], 79)

        intensity_component = container.GetDataComponentByIndex(1)
        self.assertEqual(intensity_component.IsValid(), True)
        self.assertEqual(intensity_component.PixelType, pylon.PixelType_Mono16)
        self.assertEqual(intensity_component.ComponentType, pylon.ComponentType_Intensity)
        self.assertEqual(intensity_component.Width, 160)
        self.assertEqual(intensity_component.Height, 120)
        self.assertEqual(intensity_component.OffsetX, 80)
        self.assertEqual(intensity_component.OffsetY, 60)
        self.assertEqual(intensity_component.PaddingX, 0)
        self.assertEqual(intensity_component.DataSize, 38400)
        self.assertEqual(intensity_component.TimeStamp, 62653150103775)
        self.assertEqual(intensity_component.Array[0, 0], 20388)
        self.assertEqual(intensity_component.GetData()[0], 164)
        self.assertEqual(intensity_component.GetMemoryView()[0], 164)

        confidence_component = container.GetDataComponentByIndex(2)
        self.assertEqual(confidence_component.IsValid(), True)
        self.assertEqual(confidence_component.PixelType, pylon.PixelType_Confidence16)
        self.assertEqual(confidence_component.ComponentType, pylon.ComponentType_Confidence)
        self.assertEqual(confidence_component.Width, 160)
        self.assertEqual(confidence_component.Height, 120)
        self.assertEqual(confidence_component.OffsetX, 80)
        self.assertEqual(confidence_component.OffsetY, 60)
        self.assertEqual(confidence_component.PaddingX, 0)
        self.assertEqual(confidence_component.DataSize, 38400)
        self.assertEqual(confidence_component.TimeStamp, 62653150103775)
        self.assertEqual(confidence_component.Array[0, 0], 1769)
        self.assertEqual(confidence_component.GetData()[0], 233)
        self.assertEqual(confidence_component.GetMemoryView()[0], 233)

        confidence_component.Release()
        self.assertEqual(confidence_component.IsValid(), False)
        intensity_component.Release()
        range_component.Release()
        container.Release()

    def test_container_load_zero_copy(self):
        """GetArrayZeroCopy yields a zero-copy numpy view of the component buffer."""
        testee1 = pylon.PylonDataContainer()
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        testee1.Load(filename)
        self.assertEqual(testee1.DataComponentCount, 3)
        testee3 = testee1.GetDataComponentByIndex(1)
        with testee3.GetArrayZeroCopy() as zc:
            self.assertEqual(zc[0,0], 20388)
        testee3.Release()
        testee1.Release()

    def test_component_array_and_format_accessors(self):
        """Data, ImageFormat / GetImageFormat, and GetArray (default + raw) agree with each other and with the component metadata."""
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        container = pylon.PylonDataContainer(filename)
        intensity_component = container.GetDataComponentByIndex(1)

        self.assertEqual(intensity_component.PixelType, pylon.PixelType_Mono16)
        self.assertEqual(intensity_component.Data, intensity_component.GetData())
        self.assertEqual(intensity_component.ImageFormat, intensity_component.GetImageFormat())

        shape, dtype, fmt = intensity_component.GetImageFormat()
        self.assertEqual(shape, (intensity_component.Height, intensity_component.Width))
        self.assertEqual(dtype.__name__, "uint16")
        self.assertEqual(fmt, "H")

        typed_array = intensity_component.GetArray()
        self.assertEqual(typed_array.shape, shape)
        self.assertEqual(typed_array.dtype.name, "uint16")
        self.assertEqual(typed_array[0, 0], 20388)

        raw_array = intensity_component.GetArray(raw=True)
        self.assertEqual(raw_array.ndim, 1)
        self.assertEqual(raw_array.shape, (intensity_component.DataSize,))
        self.assertEqual(raw_array.dtype.name, "uint8")
        self.assertEqual(raw_array[0], intensity_component.GetData()[0])

        bytes_per_pixel = 2
        expected_stride = intensity_component.Width * bytes_per_pixel + intensity_component.PaddingX
        self.assertEqual(
            intensity_component.GetStride(),
            [True, expected_stride],
        )

        intensity_component.Release()
        container.Release()

    # ------------------------------------------------------------------
    # Save / Load
    # ------------------------------------------------------------------

    def test_empty_container_save_rejects(self):
        """Save() on an empty container raises LogicalErrorException regardless of filename."""
        testee = pylon.PylonDataContainer()
        with self.assertRaises(genicam.LogicalErrorException):
            testee.Save("dummyfilename")

    def test_save_load_roundtrip(self):
        """Save() persists a container, and Load() reproduces every component field."""
        with self._grab_one(gen_dc=True) as grab_result_gen_dc:
            container_valid = pylon.PylonDataContainer(grab_result_gen_dc)
            self.assertGreater(container_valid.DataComponentCount, 0)

            with self.assertRaises(genicam.GenericException):
                container_valid.Save("")

            save_path = self._tmp_path(".gendc")
            try:
                container_valid.Save(save_path)

                container_loaded = pylon.PylonDataContainer()
                container_loaded.Load(save_path)
                self.assertEqual(
                    container_loaded.DataComponentCount,
                    container_valid.DataComponentCount,
                )
                for i in range(container_loaded.DataComponentCount):
                    self._assert_components_equivalent(
                        container_valid.GetDataComponentByIndex(i),
                        container_loaded.GetDataComponentByIndex(i),
                    )
                container_loaded.Release()
            finally:
                if os.path.exists(save_path):
                    os.unlink(save_path)

            container_valid.Release()

        with self._grab_one() as grab_result_image:
            container_from_image = pylon.PylonDataContainer(grab_result_image)
            image_path = self._tmp_path(".gendc")
            try:
                container_from_image.Save(image_path)

                container_from_image_loaded = pylon.PylonDataContainer()
                container_from_image_loaded.Load(image_path)
                self.assertEqual(
                    container_from_image_loaded.DataComponentCount,
                    container_from_image.DataComponentCount,
                )
                container_from_image_loaded.Release()

                container_constructed = pylon.PylonDataContainer(image_path)
                self.assertEqual(
                    container_constructed.DataComponentCount,
                    container_from_image.DataComponentCount,
                )
                container_constructed.Release()
            finally:
                if os.path.exists(image_path):
                    os.unlink(image_path)
            container_from_image.Release()

    def test_load_rejects_invalid(self):
        """Load() and the filename ctor reject empty/malformed/missing/garbage paths."""
        container = pylon.PylonDataContainer()

        for bad_path in ("", "valid_but_not_existing__"):
            with self.assertRaises(genicam.GenericException):
                container.Load(bad_path)
            self.assertEqual(container.DataComponentCount, 0)

        empty_path = self._tmp_path(".gendc")
        open(empty_path, "wb").close()
        try:
            with self.assertRaises(genicam.GenericException):
                container.Load(empty_path)
            self.assertEqual(container.DataComponentCount, 0)
        finally:
            os.unlink(empty_path)

        illegal_path = self._tmp_path(".gendc")
        with open(illegal_path, "wb") as f:
            for i in range(1, 10):
                f.write(str(i).encode("ascii"))
        try:
            with self.assertRaises(genicam.GenericException):
                container.Load(illegal_path)
            self.assertEqual(container.DataComponentCount, 0)
        finally:
            os.unlink(illegal_path)

    # ------------------------------------------------------------------
    # GetComponentIndex (PylonDataComponent.h / pylon 2605+)
    # ------------------------------------------------------------------

    def test_get_component_index_matches_position_in_container(self):
        """GetComponentIndex() returns the zero-based position of each component within its container."""
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        container = pylon.PylonDataContainer(filename)
        self.assertEqual(container.DataComponentCount, 3)

        for expected_index in range(container.DataComponentCount):
            component = container.GetDataComponentByIndex(expected_index)
            self.assertTrue(component.IsValid())
            # Method access
            self.assertEqual(component.GetComponentIndex(), expected_index)
            component.Release()

        container.Release()

    def test_get_component_index_survives_copy(self):
        """GetComponentIndex() is preserved when a component is copy-constructed."""
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        container = pylon.PylonDataContainer(filename)

        original = container.GetDataComponentByIndex(1)
        copied = pylon.PylonDataComponent(original)

        self.assertEqual(copied.GetComponentIndex(), original.GetComponentIndex())
        self.assertEqual(copied.GetComponentIndex(), 1)

        original.Release()
        copied.Release()
        container.Release()

    def test_get_component_index_for_live_grab_result(self):
        """GetComponentIndex() returns 0 for the single component of a standard image grab result."""
        with self._grab_one() as grab_result:
            container = pylon.PylonDataContainer(grab_result)
            self.assertEqual(container.DataComponentCount, 1)
            component = container.GetDataComponentByIndex(0)
            self.assertEqual(component.GetComponentIndex(), 0)
            component.Release()
            container.Release()

    # ------------------------------------------------------------------
    # GetFirstImageDataComponent (PylonDataContainer.h / pylon 2605+)
    # ------------------------------------------------------------------

    def test_container_get_first_image_data_component_no_args(self):
        """GetFirstImageDataComponent() returns a valid Intensity component from a multi-component container."""
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        container = pylon.PylonDataContainer(filename)
        self.assertEqual(container.DataComponentCount, 3)

        component = container.GetFirstImageDataComponent()
        self.assertTrue(component.IsValid())
        self.assertEqual(component.ComponentType, pylon.ComponentType_Intensity)

        component.Release()
        container.Release()

    def test_container_get_first_image_data_component_throw_true_succeeds_when_found(self):
        """GetFirstImageDataComponent(True) returns a valid component without raising when one exists."""
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        container = pylon.PylonDataContainer(filename)

        component = container.GetFirstImageDataComponent(True)
        self.assertTrue(component.IsValid())
        self.assertEqual(component.ComponentType, pylon.ComponentType_Intensity)

        component.Release()
        container.Release()

    def test_container_get_first_image_data_component_throw_false_returns_invalid_on_empty_container(self):
        """GetFirstImageDataComponent(False) returns an invalid component when the container is empty."""
        empty_container = pylon.PylonDataContainer()
        component = empty_container.GetFirstImageDataComponent(False)
        self.assertFalse(component.IsValid())
        component.Release()
        empty_container.Release()

    def test_container_get_first_image_data_component_throw_true_raises_on_empty_container(self):
        """GetFirstImageDataComponent(True) raises an exception when the container has no image component."""
        empty_container = pylon.PylonDataContainer()
        with self.assertRaises(genicam.GenericException):
            empty_container.GetFirstImageDataComponent(True)
        empty_container.Release()

    def test_container_get_first_image_data_component_from_live_grab(self):
        """GetFirstImageDataComponent() on a container built from a live grab returns the image component."""
        with self._grab_one() as grab_result:
            container = pylon.PylonDataContainer(grab_result)
            component = container.GetFirstImageDataComponent()
            self.assertTrue(component.IsValid())
            self.assertEqual(component.ComponentType, pylon.ComponentType_Intensity)
            self.assertEqual(component.Width, grab_result.Width)
            self.assertEqual(component.Height, grab_result.Height)
            self.assertEqual(component.PixelType, grab_result.PixelType)
            component.Release()
            container.Release()

    def test_container_get_first_image_data_component_index_is_consistent_with_by_index(self):
        """GetFirstImageDataComponent() returns the same component as GetDataComponentByIndex at its index."""
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        container = pylon.PylonDataContainer(filename)

        first = container.GetFirstImageDataComponent()
        by_index = container.GetDataComponentByIndex(first.GetComponentIndex())

        self.assertEqual(first.ComponentType, by_index.ComponentType)
        self.assertEqual(first.PixelType, by_index.PixelType)
        self.assertEqual(first.Width, by_index.Width)
        self.assertEqual(first.Height, by_index.Height)

        first.Release()
        by_index.Release()
        container.Release()

    def test_container_get_first_image_data_component_call_variants(self):
        """GetFirstImageDataComponent() works with all mapped overloads."""
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        container = pylon.PylonDataContainer(filename)

        component1 = container.GetFirstImageDataComponent()
        component2 = container.GetFirstImageDataComponent(True)
        self._assert_components_equivalent(component1, component2)
        component2.Release()

        component2 = container.GetFirstImageDataComponent(pylon.ComponentType_Intensity)
        self._assert_components_equivalent(component1, component2)
        component2.Release()

        component2 = container.GetFirstImageDataComponent(pylon.ComponentType_Intensity, 0)
        self._assert_components_equivalent(component1, component2)
        component2.Release()

        component2 = container.GetFirstImageDataComponent(pylon.ComponentType_Intensity, 0, True)
        self._assert_components_equivalent(component1, component2)
        component2.Release()

        container.Release()

    # ------------------------------------------------------------------
    # PaddingY / context manager
    # ------------------------------------------------------------------

    def test_get_padding_y_default_component(self):
        """GetPaddingY() and PaddingY both return 0 for a default-constructed component."""
        testee = pylon.PylonDataComponent()
        self.assertEqual(testee.GetPaddingY(), 0)
        self.assertEqual(testee.PaddingY, 0)

    def test_get_padding_y_from_loaded_fixture(self):
        """GetPaddingY() and PaddingY return 0 for every component in the little_boxes.gendc fixture."""
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        container = pylon.PylonDataContainer(filename)
        self.assertEqual(container.DataComponentCount, 3)

        for i in range(container.DataComponentCount):
            component = container.GetDataComponentByIndex(i)
            self.assertEqual(component.GetPaddingY(), 0)
            self.assertEqual(component.PaddingY, 0)
            component.Release()

        container.Release()

    def test_component_context_manager(self):
        """Using a component as a context manager returns self on __enter__ and releases it on __exit__."""
        thisdir = os.path.dirname(__file__)
        filename = os.path.join(thisdir, 'little_boxes.gendc')
        container = pylon.PylonDataContainer(filename)

        component = container.GetDataComponentByIndex(0)
        self.assertTrue(component.IsValid())

        with component as c:
            self.assertIs(c, component)
            self.assertTrue(c.IsValid())

        self.assertFalse(component.IsValid())
        container.Release()


if __name__ == "__main__":
    unittest.main()
