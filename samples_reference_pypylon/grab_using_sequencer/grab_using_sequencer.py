#!/usr/bin/env python3
"""
grab_using_sequencer.py

This sample demonstrates how to use the camera sequencer feature for automated
parameter changes during image acquisition. The sequencer allows the camera to
automatically cycle through different parameter settings (sequence sets) for
each captured image.

Key concepts demonstrated:
- Camera sequencer configuration (SFNC 2.0+ vs 1.x)
- Multiple sequence sets with different parameters
- Automatic parameter cycling during acquisition
- Sequence set configuration and saving
- Sequencer mode enabling/disabling
- Interactive sequence demonstration

The sequencer is useful for:
- Automated exposure bracketing
- Multi-resolution image capture
- Parameter sweeps and optimization
- Complex acquisition patterns
- Time-lapse with varying settings

This is equivalent to samples_reference_c++/Grab_UsingSequencer/
"""

from typing import List, Dict, Any, Optional
import pypylon.pylon as pylon
from pypylon import genicam
import time


class SequenceSetConfiguration:
    """
    Configuration for a single sequence set.
    
    Contains the parameters that will be applied when this sequence set is active.
    """
    
    def __init__(self, set_index: int, name: str, height_percent: float):
        self.set_index = set_index
        self.name = name
        self.height_percent = height_percent
        self.parameters = {}
    
    def add_parameter(self, name: str, value: Any) -> None:
        """Add a parameter to this sequence set."""
        self.parameters[name] = value
    
    def __str__(self) -> str:
        return f"SequenceSet {self.set_index}: {self.name} (Height: {self.height_percent}%)"


class SequencerManager:
    """
    Manager for camera sequencer functionality.
    
    Handles the configuration and control of camera sequencer features,
    including SFNC version compatibility.
    """
    
    def __init__(self, camera: pylon.InstantCamera):
        self.camera = camera
        self.sequence_sets: List[SequenceSetConfiguration] = []
        self.is_sfnc_2_0_plus = False
        self.sequencer_supported = False
        self.original_height = None
        self.original_width = None
        
    def check_sequencer_support(self) -> bool:
        """Check if the camera supports sequencer functionality."""
        try:
            # Check SFNC version
            self.is_sfnc_2_0_plus = self.camera.GetSfncVersion() >= pylon.Sfnc_2_0_0
            
            if self.is_sfnc_2_0_plus:
                # SFNC 2.0+ (USB cameras) - check for SequencerMode
                if hasattr(self.camera, 'SequencerMode') and genicam.IsWritable(self.camera.SequencerMode):
                    self.sequencer_supported = True
                    print(f"[SUCCESS] Sequencer supported (SFNC 2.0+)")
                    return True
            else:
                # SFNC 1.x (GigE cameras) - check for SequenceEnable
                if hasattr(self.camera, 'SequenceEnable') and genicam.IsWritable(self.camera.SequenceEnable):
                    self.sequencer_supported = True
                    print(f"[SUCCESS] Sequencer supported (SFNC 1.x)")
                    return True
            
            print("[ERROR] Sequencer not supported by this camera")
            return False
            
        except Exception as e:
            print(f"[ERROR] Error checking sequencer support: {e}")
            return False
    
    def store_original_parameters(self) -> None:
        """Store original camera parameters for restoration."""
        try:
            if hasattr(self.camera, 'Height') and genicam.IsReadable(self.camera.Height):
                self.original_height = self.camera.Height.Value
            if hasattr(self.camera, 'Width') and genicam.IsReadable(self.camera.Width):
                self.original_width = self.camera.Width.Value
            print(f"[CONFIG] Original parameters stored: {self.original_width}x{self.original_height}")
        except Exception as e:
            print(f"[WARNING]  Could not store original parameters: {e}")
    
    def setup_base_parameters(self) -> None:
        """Set up base camera parameters before configuring sequencer."""
        try:
            print("[CONFIG] Setting up base camera parameters...")
            
            # Maximize image area of interest (AOI)
            if hasattr(self.camera, 'OffsetX'):
                self.camera.OffsetX.TrySetToMinimum()
            if hasattr(self.camera, 'OffsetY'):
                self.camera.OffsetY.TrySetToMinimum()
            if hasattr(self.camera, 'Width'):
                self.camera.Width.SetToMaximum()
            if hasattr(self.camera, 'Height'):
                self.camera.Height.SetToMaximum()
            
            # Set pixel format to Mono8
            if hasattr(self.camera, 'PixelFormat'):
                try:
                    self.camera.PixelFormat.Value = "Mono8"
                    print("   [SUCCESS] Pixel format set to Mono8")
                except Exception as e:
                    print(f"   [WARNING]  Could not set pixel format: {e}")
            
            print("   [SUCCESS] Base parameters configured")
            
        except Exception as e:
            print(f"[ERROR] Error setting up base parameters: {e}")
    
    def disable_sequencer(self) -> None:
        """Disable sequencer before configuration."""
        try:
            print("[CONFIG] Disabling sequencer for configuration...")
            
            if self.is_sfnc_2_0_plus:
                # SFNC 2.0+ cameras
                if hasattr(self.camera, 'SequencerMode'):
                    self.camera.SequencerMode.Value = "Off"
                if hasattr(self.camera, 'SequencerConfigurationMode'):
                    self.camera.SequencerConfigurationMode.Value = "Off"
            else:
                # SFNC 1.x cameras
                if hasattr(self.camera, 'SequenceEnable'):
                    self.camera.SequenceEnable.Value = False
                if hasattr(self.camera, 'SequenceConfigurationMode'):
                    self.camera.SequenceConfigurationMode.TrySetValue("Off")
            
            print("   [SUCCESS] Sequencer disabled")
            
        except Exception as e:
            print(f"[ERROR] Error disabling sequencer: {e}")
    
    def add_sequence_set(self, set_index: int, name: str, height_percent: float) -> None:
        """Add a sequence set configuration."""
        sequence_set = SequenceSetConfiguration(set_index, name, height_percent)
        self.sequence_sets.append(sequence_set)
        print(f"   📝 Added sequence set: {sequence_set}")
    
    def configure_sequencer_sfnc_2_0_plus(self) -> bool:
        """Configure sequencer for SFNC 2.0+ cameras (USB)."""
        try:
            print("[CONFIG] Configuring sequencer (SFNC 2.0+)...")
            
            # Enable configuration mode
            self.camera.SequencerConfigurationMode.Value = "On"
            
            # Get sequencer set parameters
            initial_set = self.camera.SequencerSetSelector.Min
            inc_set = self.camera.SequencerSetSelector.Inc
            current_set = initial_set
            
            print(f"   [INFO] Sequencer sets: initial={initial_set}, increment={inc_set}")
            
            # Configure each sequence set
            for i, seq_set in enumerate(self.sequence_sets):
                print(f"   📝 Configuring sequence set {i}: {seq_set.name}")
                
                # Select the sequence set
                self.camera.SequencerSetSelector.Value = current_set
                
                # Configure sequencer paths (common for all sets)
                if i == 0:  # Only configure paths for first set
                    # Reset path (path 0) - reset on software signal 1
                    self.camera.SequencerPathSelector.Value = 0
                    self.camera.SequencerSetNext.Value = initial_set
                    self.camera.SequencerTriggerSource.Value = "SoftwareSignal1"
                    
                    # Advance path (path 1) - advance on frame start
                    self.camera.SequencerPathSelector.Value = 1
                    try:
                        self.camera.SequencerTriggerSource.Value = "FrameStart"
                    except:
                        try:
                            self.camera.SequencerTriggerSource.Value = "ExposureStart"
                        except Exception as e:
                            print(f"     [WARNING]  Could not set sequencer trigger source: {e}")
                
                # Set next sequence set
                if i < len(self.sequence_sets) - 1:
                    self.camera.SequencerSetNext.Value = current_set + inc_set
                else:
                    self.camera.SequencerSetNext.Value = initial_set  # Loop back to start
                
                # Set the height for this sequence set
                if hasattr(self.camera, 'Height'):
                    self.camera.Height.SetValuePercentOfRange(seq_set.height_percent)
                    print(f"     📏 Height set to {seq_set.height_percent}%")
                
                # Save the sequence set
                self.camera.SequencerSetSave.Execute()
                print(f"     [SUCCESS] Sequence set {i} saved")
                
                current_set += inc_set
            
            # Disable configuration mode and enable sequencer
            self.camera.SequencerConfigurationMode.Value = "Off"
            self.camera.SequencerMode.Value = "On"
            
            print("   [SUCCESS] Sequencer enabled (SFNC 2.0+)")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error configuring SFNC 2.0+ sequencer: {e}")
            return False
    
    def configure_sequencer_sfnc_1_x(self) -> bool:
        """Configure sequencer for SFNC 1.x cameras (GigE)."""
        try:
            print("[CONFIG] Configuring sequencer (SFNC 1.x)...")
            
            # Enable configuration mode if available
            if hasattr(self.camera, 'SequenceConfigurationMode'):
                self.camera.SequenceConfigurationMode.TrySetValue("On")
            
            # Configure sequence advance mode
            if hasattr(self.camera, 'SequenceAdvanceMode'):
                self.camera.SequenceAdvanceMode.Value = "Auto"
                print("   🔄 Sequence advance mode set to Auto")
            
            # Set total number of sequence sets
            if hasattr(self.camera, 'SequenceSetTotalNumber'):
                self.camera.SequenceSetTotalNumber.Value = len(self.sequence_sets)
                print(f"   [INFO] Total sequence sets: {len(self.sequence_sets)}")
            
            # Configure each sequence set
            for i, seq_set in enumerate(self.sequence_sets):
                print(f"   📝 Configuring sequence set {i}: {seq_set.name}")
                
                # Select the sequence set
                if hasattr(self.camera, 'SequenceSetIndex'):
                    self.camera.SequenceSetIndex.Value = i
                
                # Set the height for this sequence set
                if hasattr(self.camera, 'Height'):
                    self.camera.Height.SetValuePercentOfRange(seq_set.height_percent)
                    print(f"     📏 Height set to {seq_set.height_percent}%")
                
                # Store the sequence set
                if hasattr(self.camera, 'SequenceSetStore'):
                    self.camera.SequenceSetStore.Execute()
                    print(f"     [SUCCESS] Sequence set {i} stored")
            
            # Disable configuration mode if available
            if hasattr(self.camera, 'SequenceConfigurationMode'):
                self.camera.SequenceConfigurationMode.TrySetValue("Off")
            
            # Enable sequence
            self.camera.SequenceEnable.Value = True
            
            print("   [SUCCESS] Sequencer enabled (SFNC 1.x)")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error configuring SFNC 1.x sequencer: {e}")
            return False
    
    def configure_sequencer(self) -> bool:
        """Configure the sequencer based on camera SFNC version."""
        if not self.sequence_sets:
            print("[ERROR] No sequence sets defined")
            return False
        
        if self.is_sfnc_2_0_plus:
            return self.configure_sequencer_sfnc_2_0_plus()
        else:
            return self.configure_sequencer_sfnc_1_x()
    
    def disable_sequencer_final(self) -> None:
        """Disable sequencer after acquisition."""
        try:
            print("\n[CONFIG] Disabling sequencer...")
            
            if self.is_sfnc_2_0_plus:
                # SFNC 2.0+ cameras
                if hasattr(self.camera, 'SequencerMode'):
                    self.camera.SequencerMode.Value = "Off"
            else:
                # SFNC 1.x cameras
                if hasattr(self.camera, 'SequenceEnable'):
                    self.camera.SequenceEnable.Value = False
            
            # Try to disable configuration mode
            if hasattr(self.camera, 'SequenceConfigurationMode'):
                self.camera.SequenceConfigurationMode.TrySetValue("Off")
            
            print("   [SUCCESS] Sequencer disabled")
            
        except Exception as e:
            print(f"[ERROR] Error disabling sequencer: {e}")
    
    def restore_original_parameters(self) -> None:
        """Restore original camera parameters."""
        try:
            if self.original_height is not None and hasattr(self.camera, 'Height'):
                self.camera.Height.Value = self.original_height
            if self.original_width is not None and hasattr(self.camera, 'Width'):
                self.camera.Width.Value = self.original_width
            print("[CONFIG] Original parameters restored")
        except Exception as e:
            print(f"[WARNING]  Could not restore original parameters: {e}")


def create_sequence_sets() -> List[SequenceSetConfiguration]:
    """Create predefined sequence sets for demonstration."""
    sequence_sets = [
        SequenceSetConfiguration(0, "Quarter Height", 25.0),
        SequenceSetConfiguration(1, "Half Height", 50.0),
        SequenceSetConfiguration(2, "Full Height", 100.0)
    ]
    return sequence_sets


def demonstrate_sequencer_acquisition(camera: pylon.InstantCamera, images_to_grab: int = 10) -> None:
    """Demonstrate image acquisition with sequencer."""
    print(f"\n[START] Starting sequencer demonstration ({images_to_grab} images)...")
    print("[IMAGE] Each image will use different sequence set parameters.\n")
    
    # Start grabbing
    camera.StartGrabbingMax(images_to_grab)
    
    image_count = 0
    sequence_cycle = 0
    
    try:
        while camera.IsGrabbing():
            # Execute software trigger
            if camera.CanWaitForFrameTriggerReady():
                if camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException):
                    camera.ExecuteSoftwareTrigger()
            
            # Retrieve result
            grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            
            if grab_result.GrabSucceeded():
                image_count += 1
                sequence_index = (image_count - 1) % 3  # 3 sequence sets
                
                print(f"🖼️  Image {image_count}:")
                print(f"    📏 Size: {grab_result.GetWidth()}x{grab_result.GetHeight()}")
                print(f"    📝 Sequence Set: {sequence_index} ({'Quarter' if sequence_index == 0 else 'Half' if sequence_index == 1 else 'Full'} Height)")
                print(f"    [INFO] Frame ID: {grab_result.GetID()}")
                
                # Calculate and display basic image statistics
                try:
                    image_array = grab_result.GetArray()
                    if image_array is not None:
                        mean_intensity = float(image_array.mean())
                        print(f"    [STATS] Mean intensity: {mean_intensity:.1f}")
                except Exception as e:
                    print(f"    [WARNING]  Could not calculate image statistics: {e}")
                
                if sequence_index == 2:  # Completed a full cycle
                    sequence_cycle += 1
                    print(f"    🔄 Completed sequence cycle {sequence_cycle}")
                
                print()
            else:
                print(f"[ERROR] Image {image_count + 1} grab failed:")
                print(f"    Error: {grab_result.GetErrorCode()} - {grab_result.GetErrorDescription()}")
            
            grab_result.Release()
            
            # Pause for demonstration (remove in production)
            time.sleep(0.5)
    
    except Exception as e:
        print(f"[ERROR] Error during acquisition: {e}")
    
    print(f"[SUCCESS] Sequencer demonstration completed!")
    print(f"[INFO] Total images: {image_count}")
    print(f"🔄 Sequence cycles: {sequence_cycle}")


def main() -> int:
    """
    Main function demonstrating camera sequencer functionality.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    exit_code = 0
    
    try:
        # Initialize pylon runtime
        
        
        print("=== Camera Sequencer Sample ===")
        print("This sample demonstrates camera sequencer functionality.")
        print("The sequencer automatically cycles through different parameter sets.\n")
        
        # Create camera instance
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        
        print(f"Using device: {camera.GetDeviceInfo().GetModelName()}")
        print(f"Serial Number: {camera.GetDeviceInfo().GetSerialNumber()}")
        
        # Register software trigger configuration
        camera.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), 
                                   pylon.RegistrationMode_ReplaceAll, 
                                   pylon.Cleanup_Delete)
        
        # Open camera
        camera.Open()
        
        # Create sequencer manager
        sequencer = SequencerManager(camera)
        
        # Check sequencer support
        if not sequencer.check_sequencer_support():
            print("\n[ERROR] This camera doesn't support sequencer functionality.")
            camera.Close()
            return 1
        
        # Store original parameters
        sequencer.store_original_parameters()
        
        # Disable sequencer for configuration
        sequencer.disable_sequencer()
        
        # Set up base parameters
        sequencer.setup_base_parameters()
        
        # Create sequence sets
        print("\n[CONFIG] Creating sequence sets...")
        sequence_sets = create_sequence_sets()
        for seq_set in sequence_sets:
            sequencer.add_sequence_set(seq_set.set_index, seq_set.name, seq_set.height_percent)
        
        # Configure sequencer
        if not sequencer.configure_sequencer():
            print("[ERROR] Failed to configure sequencer")
            camera.Close()
            return 1
        
        print(f"\n[SUCCESS] Sequencer configured successfully!")
        print(f"[INFO] SFNC Version: {'2.0+' if sequencer.is_sfnc_2_0_plus else '1.x'}")
        print(f"🔄 Sequence Sets: {len(sequencer.sequence_sets)}")
        
        # Demonstrate sequencer acquisition
        demonstrate_sequencer_acquisition(camera, images_to_grab=9)  # 3 complete cycles
        
        # Disable sequencer
        sequencer.disable_sequencer_final()
        
        # Restore original parameters
        sequencer.restore_original_parameters()
        
        # Close camera
        camera.Close()
        
        print("\n" + "=" * 50)
        print("SEQUENCER DEMONSTRATION COMPLETED")
        print("=" * 50)
        print("The sequencer automatically cycled through different parameter sets:")
        for seq_set in sequence_sets:
            print(f"  • {seq_set}")
        
        print("\nSequencer features enable:")
        print("  • Automated parameter changes")
        print("  • Complex acquisition patterns")
        print("  • Parameter sweeps and optimization")
        print("  • Time-lapse with varying settings")
        
    except genicam.GenericException as e:
        print(f"[ERROR] A pylon exception occurred: {e}")
        exit_code = 1
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        exit_code = 1
    finally:
        # Ensure pylon resources are released
        
    
    return exit_code


if __name__ == "__main__":
    import sys
    
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[STOP] Interrupted by user")
        
        sys.exit(1) 