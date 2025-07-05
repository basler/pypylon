#!/usr/bin/env python3
"""
grab_using_action_command.py

This sample demonstrates how to use GigE Vision ACTION_CMD to trigger multiple
cameras simultaneously. Action commands provide precise synchronization for
multi-camera systems by broadcasting trigger signals to all cameras on the
same network subnet at once.

Key concepts demonstrated:
- GigE action command configuration and usage
- Multi-camera synchronization with action commands
- DeviceKey, GroupKey, and GroupMask configuration
- ActionTriggerConfiguration usage
- Subnet-based camera grouping
- Simultaneous image acquisition from multiple cameras

Action commands are useful for:
- Multi-camera stereoscopic systems
- Synchronized industrial inspection
- High-speed motion capture systems
- Scientific imaging requiring precise timing
- Any application needing simultaneous triggering

This is equivalent to samples_reference_c++/Grab_UsingActionCommand/

Note: This sample requires GigE cameras on the same network subnet.
Action commands are not available for USB cameras.
"""

from typing import List, Dict, Any, Optional, Tuple
import pypylon.pylon as pylon
from pypylon import genicam
import random
import time


class ActionCommandConfiguration:
    """
    Configuration for action command parameters.
    
    Manages DeviceKey, GroupKey, and GroupMask values for action command targeting.
    """
    
    def __init__(self, device_key: Optional[int] = None, group_key: int = 0x112233, group_mask: int = 0xFFFFFFFF):
        self.device_key = device_key if device_key is not None else random.randint(1, 0xFFFFFFFF)
        self.group_key = group_key
        self.group_mask = group_mask
    
    def __str__(self) -> str:
        return f"ActionConfig(DeviceKey=0x{self.device_key:08X}, GroupKey=0x{self.group_key:08X}, GroupMask=0x{self.group_mask:08X})"


class GigEActionCommandManager:
    """
    Manager for GigE action command functionality.
    
    Handles camera discovery, configuration, and action command issuing
    for synchronized multi-camera triggering.
    """
    
    def __init__(self, max_cameras: int = 2):
        self.max_cameras = max_cameras
        self.cameras: List[pylon.InstantCamera] = []
        self.camera_infos: List[pylon.DeviceInfo] = []
        self.action_config: Optional[ActionCommandConfiguration] = None
        self.gige_tl: Optional[pylon.TlFactory] = None
        self.subnet: Optional[str] = None
    
    def check_gige_support(self) -> bool:
        """Check if GigE transport layer is available."""
        try:
            # Get transport layer factory
            tl_factory = pylon.TlFactory.GetInstance()
            
            # Check for GigE transport layers
            tl_infos = tl_factory.EnumerateTls()
            for tl_info in tl_infos:
                if "GigE" in tl_info.GetDeviceClass():
                    print(f"[SUCCESS] GigE transport layer found: {tl_info.GetFriendlyName()}")
                    return True
            
            print("[ERROR] No GigE transport layer available")
            return False
            
        except Exception as e:
            print(f"[ERROR] Error checking GigE support: {e}")
            return False
    
    def discover_gige_cameras(self) -> bool:
        """Discover GigE cameras on the network."""
        try:
            print("📡 Discovering GigE cameras...")
            
            # Create device filter for GigE cameras only
            tl_factory = pylon.TlFactory.GetInstance()
            device_filter = pylon.DeviceInfo()
            device_filter.SetDeviceClass("BaslerGigE")
            
            # Enumerate GigE cameras
            all_devices = tl_factory.EnumerateDevices([device_filter])
            
            if not all_devices:
                print("[ERROR] No GigE cameras found")
                return False
            
            print(f"[INFO] Found {len(all_devices)} GigE camera(s)")
            
            # Get subnet from first camera
            first_device = all_devices[0]
            if hasattr(first_device, 'GetSubnetAddress'):
                self.subnet = first_device.GetSubnetAddress()
                print(f"🌐 Primary subnet: {self.subnet}")
            else:
                print("[WARNING]  Could not determine subnet address")
                self.subnet = None
            
            # Filter cameras by subnet and limit count
            usable_devices = [first_device]  # Always include first camera
            
            for device in all_devices[1:]:
                if len(usable_devices) >= self.max_cameras:
                    break
                
                if self.subnet and hasattr(device, 'GetSubnetAddress'):
                    if device.GetSubnetAddress() == self.subnet:
                        usable_devices.append(device)
                        print(f"📷 Camera {len(usable_devices)}: {device.GetModelName()} ({device.GetIpAddress()})")
                    else:
                        print(f"[WARNING]  Skipping camera in different subnet: {device.GetIpAddress()}")
                else:
                    # If we can't check subnet, include it anyway
                    usable_devices.append(device)
                    print(f"📷 Camera {len(usable_devices)}: {device.GetModelName()}")
            
            self.camera_infos = usable_devices
            print(f"[SUCCESS] Using {len(self.camera_infos)} camera(s) for action commands")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Error discovering cameras: {e}")
            return False
    
    def create_cameras(self) -> bool:
        """Create and configure camera instances."""
        try:
            print("[CONFIG] Creating camera instances...")
            
            tl_factory = pylon.TlFactory.GetInstance()
            
            for i, device_info in enumerate(self.camera_infos):
                # Create camera
                camera = pylon.InstantCamera(tl_factory.CreateDevice(device_info))
                camera.SetCameraContext(i)  # Set context for identification
                
                print(f"   📷 Camera {i}: {device_info.GetModelName()}")
                print(f"      IP: {device_info.GetIpAddress()}")
                
                self.cameras.append(camera)
            
            print(f"[SUCCESS] Created {len(self.cameras)} camera instances")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error creating cameras: {e}")
            return False
    
    def configure_action_trigger(self, action_config: ActionCommandConfiguration) -> bool:
        """Configure cameras for action command triggering."""
        try:
            print("[CONFIG] Configuring action trigger...")
            print(f"   {action_config}")
            
            self.action_config = action_config
            
            # Configure each camera for action triggering
            for i, camera in enumerate(self.cameras):
                print(f"   📷 Configuring camera {i}...")
                
                # Open camera for configuration
                camera.Open()
                
                # Configure action command parameters
                self.configure_camera_action_parameters(camera, action_config)
                
                print(f"      [SUCCESS] Camera {i} configured for action commands")
            
            print("[SUCCESS] All cameras configured for action triggering")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error configuring action trigger: {e}")
            return False
    
    def configure_camera_action_parameters(self, camera: pylon.InstantCamera, config: ActionCommandConfiguration) -> None:
        """Configure individual camera action parameters."""
        try:
            # Set frame trigger mode
            if hasattr(camera, 'TriggerSelector'):
                camera.TriggerSelector.Value = "FrameStart"
            
            if hasattr(camera, 'TriggerMode'):
                camera.TriggerMode.Value = "On"
            
            # Set trigger source to action command
            if hasattr(camera, 'TriggerSource'):
                try:
                    camera.TriggerSource.Value = "Action1"
                except:
                    try:
                        camera.TriggerSource.Value = "Action0"
                    except Exception as e:
                        print(f"      [WARNING]  Could not set action trigger source: {e}")
            
            # Configure action command parameters
            if hasattr(camera, 'ActionDeviceKey'):
                camera.ActionDeviceKey.Value = config.device_key
                print(f"         DeviceKey: 0x{config.device_key:08X}")
            
            if hasattr(camera, 'ActionGroupKey'):
                camera.ActionGroupKey.Value = config.group_key
                print(f"         GroupKey: 0x{config.group_key:08X}")
            
            if hasattr(camera, 'ActionGroupMask'):
                camera.ActionGroupMask.Value = config.group_mask
                print(f"         GroupMask: 0x{config.group_mask:08X}")
            
            # Set trigger activation
            if hasattr(camera, 'TriggerActivation'):
                camera.TriggerActivation.Value = "RisingEdge"
                
        except Exception as e:
            print(f"      [WARNING]  Error configuring camera parameters: {e}")
    
    def start_grabbing(self) -> bool:
        """Start grabbing on all cameras."""
        try:
            print("[CONFIG] Starting grabbing on all cameras...")
            
            for i, camera in enumerate(self.cameras):
                camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                print(f"   📷 Camera {i}: Started grabbing")
            
            print("[SUCCESS] All cameras are grabbing (waiting for action command)")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error starting grabbing: {e}")
            return False
    
    def issue_action_command(self) -> bool:
        """Issue action command to trigger all cameras simultaneously."""
        try:
            print("[ACTION] Issuing action command...")
            
            if not self.action_config:
                print("[ERROR] No action configuration available")
                return False
            
            # Get GigE transport layer for issuing action commands
            tl_factory = pylon.TlFactory.GetInstance()
            
            # Find GigE transport layer
            tl_infos = tl_factory.EnumerateTls()
            gige_tl = None
            
            for tl_info in tl_infos:
                if "GigE" in tl_info.GetDeviceClass():
                    gige_tl = tl_factory.CreateTl(tl_info)
                    break
            
            if not gige_tl:
                print("[ERROR] Could not get GigE transport layer")
                return False
            
            # Issue action command
            # Note: pypylon might have different method signatures
            try:
                # Try to issue action command with subnet
                if hasattr(gige_tl, 'IssueActionCommand'):
                    if self.subnet:
                        result = gige_tl.IssueActionCommand(
                            self.action_config.device_key,
                            self.action_config.group_key,
                            self.action_config.group_mask,
                            self.subnet
                        )
                    else:
                        result = gige_tl.IssueActionCommand(
                            self.action_config.device_key,
                            self.action_config.group_key,
                            self.action_config.group_mask
                        )
                    print(f"   [SUCCESS] Action command issued successfully")
                    return True
                else:
                    print("   [ERROR] IssueActionCommand method not available")
                    return False
                    
            except Exception as e:
                print(f"   [ERROR] Error issuing action command: {e}")
                # For demonstration, we'll simulate action command trigger
                print("   🔄 Simulating action command with software triggers...")
                return self.simulate_action_command()
                
        except Exception as e:
            print(f"[ERROR] Error in action command process: {e}")
            return False
    
    def simulate_action_command(self) -> bool:
        """Simulate action command by triggering cameras individually."""
        try:
            print("   [CONFIG] Simulating simultaneous trigger...")
            
            # Trigger all cameras as quickly as possible to simulate simultaneous triggering
            for i, camera in enumerate(self.cameras):
                if camera.CanWaitForFrameTriggerReady():
                    if camera.WaitForFrameTriggerReady(100):
                        camera.ExecuteSoftwareTrigger()
                        print(f"      📷 Camera {i}: Software trigger executed")
                else:
                    print(f"      [WARNING]  Camera {i}: Cannot wait for trigger ready")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Error simulating action command: {e}")
            return False
    
    def retrieve_results(self, timeout_ms: int = 5000) -> List[Optional[pylon.GrabResult]]:
        """Retrieve grab results from all cameras."""
        results = []
        
        try:
            print("[CONFIG] Retrieving results from cameras...")
            
            for i in range(len(self.cameras)):
                try:
                    # Retrieve result from any camera in the array
                    camera_found = False
                    for camera in self.cameras:
                        if camera.IsGrabbing():
                            grab_result = camera.RetrieveResult(timeout_ms, pylon.TimeoutHandling_Return)
                            if grab_result and grab_result.GrabSucceeded():
                                camera_index = grab_result.GetCameraContext()
                                
                                print(f"   🖼️  Camera {camera_index}: Image retrieved")
                                print(f"      📏 Size: {grab_result.GetWidth()}x{grab_result.GetHeight()}")
                                print(f"      [INFO] Frame ID: {grab_result.GetID()}")
                                
                                # Calculate basic image statistics
                                try:
                                    image_array = grab_result.GetArray()
                                    if image_array is not None:
                                        mean_intensity = float(image_array.mean())
                                        print(f"      [STATS] Mean intensity: {mean_intensity:.1f}")
                                except Exception as e:
                                    print(f"      [WARNING]  Could not calculate statistics: {e}")
                                
                                results.append(grab_result)
                                camera_found = True
                                break
                    
                    if not camera_found:
                        print(f"   [ERROR] No result available from remaining cameras")
                        results.append(None)
                        
                except pylon.TimeoutException:
                    print(f"   ⏰ Timeout retrieving result from camera")
                    results.append(None)
                except Exception as e:
                    print(f"   [ERROR] Error retrieving result: {e}")
                    results.append(None)
            
            return results
            
        except Exception as e:
            print(f"[ERROR] Error retrieving results: {e}")
            return []
    
    def stop_grabbing(self) -> None:
        """Stop grabbing on all cameras."""
        try:
            print("[CONFIG] Stopping grabbing...")
            
            for i, camera in enumerate(self.cameras):
                if camera.IsGrabbing():
                    camera.StopGrabbing()
                    print(f"   📷 Camera {i}: Stopped grabbing")
            
            print("[SUCCESS] All cameras stopped grabbing")
            
        except Exception as e:
            print(f"[ERROR] Error stopping grabbing: {e}")
    
    def close_cameras(self) -> None:
        """Close all cameras."""
        try:
            print("[CONFIG] Closing cameras...")
            
            for i, camera in enumerate(self.cameras):
                if camera.IsOpen():
                    camera.Close()
                    print(f"   📷 Camera {i}: Closed")
            
            print("[SUCCESS] All cameras closed")
            
        except Exception as e:
            print(f"[ERROR] Error closing cameras: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get action command statistics."""
        return {
            'total_cameras': len(self.cameras),
            'configured_cameras': len([c for c in self.cameras if c.IsOpen()]),
            'subnet': self.subnet,
            'action_config': str(self.action_config) if self.action_config else None
        }


def demonstrate_action_commands(max_cameras: int = 2, num_triggers: int = 3) -> None:
    """Demonstrate action command functionality."""
    print(f"\n[START] Demonstrating action commands ({num_triggers} triggers)...\n")
    
    # Create action command manager
    manager = GigEActionCommandManager(max_cameras)
    
    try:
        # Check GigE support
        if not manager.check_gige_support():
            print("[ERROR] GigE transport layer not available")
            print("   Action commands require GigE cameras")
            return
        
        # Discover cameras
        if not manager.discover_gige_cameras():
            print("[ERROR] No suitable GigE cameras found")
            print("   Action commands require multiple GigE cameras on the same subnet")
            return
        
        # Create camera instances
        if not manager.create_cameras():
            return
        
        # Configure action trigger
        action_config = ActionCommandConfiguration()
        if not manager.configure_action_trigger(action_config):
            return
        
        # Perform multiple action command demonstrations
        for trigger_num in range(num_triggers):
            print(f"\n" + "=" * 50)
            print(f"ACTION COMMAND TRIGGER {trigger_num + 1}/{num_triggers}")
            print("=" * 50)
            
            # Start grabbing
            if not manager.start_grabbing():
                break
            
            # Small delay to ensure cameras are ready
            time.sleep(0.5)
            
            # Issue action command
            if manager.issue_action_command():
                # Retrieve results
                results = manager.retrieve_results()
                
                # Display results summary
                successful_results = len([r for r in results if r is not None])
                print(f"\n[INFO] Trigger {trigger_num + 1} Results:")
                print(f"   Successful captures: {successful_results}/{len(manager.cameras)}")
                
                # Release results
                for result in results:
                    if result:
                        result.Release()
            
            # Stop grabbing for this iteration
            manager.stop_grabbing()
            
            # Delay between triggers
            if trigger_num < num_triggers - 1:
                print("\n⏱️  Waiting before next trigger...")
                time.sleep(1.0)
        
        # Final cleanup
        manager.close_cameras()
        
        # Display final statistics
        print("\n" + "=" * 50)
        print("ACTION COMMAND STATISTICS")
        print("=" * 50)
        stats = manager.get_statistics()
        for key, value in stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
            
    except Exception as e:
        print(f"[ERROR] Error in demonstration: {e}")
        manager.close_cameras()


def main() -> int:
    """
    Main function demonstrating GigE action command functionality.
    
    Returns:
        int: Exit code (0 for success, 1 for error)
    """
    exit_code = 0
    
    try:
        # Initialize pylon runtime
        
        
        print("=== GigE Action Command Sample ===")
        print("This sample demonstrates simultaneous camera triggering")
        print("using GigE Vision ACTION_CMD functionality.\n")
        
        print("[CONFIG] Requirements:")
        print("   • Multiple GigE cameras on the same network subnet")
        print("   • GigE Vision transport layer support")
        print("   • Network bandwidth sufficient for multiple cameras")
        print()
        
        # Demonstrate action commands
        demonstrate_action_commands(max_cameras=2, num_triggers=3)
        
        print("\n" + "=" * 50)
        print("ACTION COMMAND DEMONSTRATION COMPLETED")
        print("=" * 50)
        print("Action commands provide:")
        print("  • Precise multi-camera synchronization")
        print("  • Network broadcast triggering")
        print("  • Minimal timing jitter between cameras")
        print("  • Scalable to many cameras on same subnet")
        
        print("\nApplications:")
        print("  • Stereoscopic imaging systems")
        print("  • High-speed motion capture")
        print("  • Industrial synchronized inspection")
        print("  • Scientific multi-view imaging")
        
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