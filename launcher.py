# launcher.py - Main entry point for the Geforce Hybrid Capture application.

import json
import os
import sys
import time
import scripts.temporary as temporary
from scripts.recorder import init_nvidia_apis, start_capture, stop_capture, cleanup

def load_configuration():
    """
    Loads the application's configuration from the 'data/configuration.json' file.
    If the file is not found, it prints an error message and exits.
    """
    try:
        with open("data/configuration.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: configuration.json not found. Please run the installer.")
        sys.exit(1)

def save_configuration(config):
    """
    Saves the provided configuration dictionary to the 'data/configuration.json' file.
    """
    with open("data/configuration.json", "w") as f:
        json.dump(config, f, indent=4)

def start_recording(config):
    """
    Starts the screen recording process. It sets the 'is_recording' flag,
    records the start time, and calls the 'start_capture' function from the recorder module.
    """
    if not temporary.is_recording:
        start_capture(config)
        temporary.is_recording = True
        temporary.recording_start_time = time.time()
        print("Recording started.")
    else:
        print("Already recording.")

def stop_recording():
    """
    Stops the screen recording process. It clears the 'is_recording' flag,
    resets the start time, and calls the 'stop_capture' function from the recorder module.
    """
    if temporary.is_recording:
        stop_capture()
        temporary.is_recording = False
        temporary.recording_start_time = None
        print("Recording stopped.")
    else:
        print("Not currently recording.")

def display_recording_stats():
    """
    Displays the current recording status (ON/OFF) and the elapsed time if a recording is in progress.
    """
    if temporary.is_recording:
        elapsed_time = time.time() - temporary.recording_start_time
        print(f"\nRecording Status: ON")
        print(f"  Duration: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}")
    else:
        print("\nRecording Status: OFF")

def configure_settings(config):
    """
    Presents a menu to the user to configure the application's settings,
    including resolution, FPS, codec, bitrate, and NVENC preset.
    The changes are saved to the configuration file.
    """
    resolution_index = 0
    codec_index = 0
    bitrate_index = 0
    preset_index = 0

    # Find the initial indices
    for i, res in enumerate(temporary.resolutions):
        if res['width'] == config['resolution']['width'] and res['height'] == config['resolution']['height']:
            resolution_index = i
            break

    if config['codec'] in temporary.codecs:
        codec_index = temporary.codecs.index(config['codec'])
    
    bitrate_str = config.get('bitrate', '5M')
    if bitrate_str in temporary.bitrates:
        bitrate_index = temporary.bitrates.index(bitrate_str)
    
    preset_str = config.get('preset', 'medium')
    if preset_str in temporary.nvenc_presets:
        preset_index = temporary.nvenc_presets.index(preset_str)

    while True:
        print("\nConfiguration Menu:")
        print(f"1. Cycle Resolution: {config['resolution']['width']}x{config['resolution']['height']}")
        print(f"2. Cycle Codec: {config['codec']}")
        print(f"3. Set FPS: {config.get('fps', 30)}")
        print(f"4. Cycle Bitrate: {config.get('bitrate', '5M')}")
        
        # Only show preset option if using NVENC codec
        if 'nvenc' in config['codec']:
            print(f"5. Cycle NVENC Preset: {config.get('preset', 'medium')}")
            print("6. Back to Main Menu")
            max_choice = 6
        else:
            print("5. Back to Main Menu")
            max_choice = 5
            
        choice = input("Enter your choice: ")
        
        if choice == "1":
            resolution_index = (resolution_index + 1) % len(temporary.resolutions)
            config['resolution'] = temporary.resolutions[resolution_index]
            save_configuration(config)
            print(f"Resolution set to: {config['resolution']['width']}x{config['resolution']['height']}")
            
        elif choice == "2":
            codec_index = (codec_index + 1) % len(temporary.codecs)
            config['codec'] = temporary.codecs[codec_index]
            save_configuration(config)
            print(f"Codec set to: {config['codec']}")
            
        elif choice == "3":
            try:
                fps = int(input("Enter new FPS (15-60 recommended): "))
                if 1 <= fps <= 120:
                    config['fps'] = fps
                    save_configuration(config)
                    print(f"FPS set to: {fps}")
                else:
                    print("FPS must be between 1 and 120.")
            except ValueError:
                print("Invalid input. Please enter an integer.")
                
        elif choice == "4":
            bitrate_index = (bitrate_index + 1) % len(temporary.bitrates)
            config['bitrate'] = temporary.bitrates[bitrate_index]
            save_configuration(config)
            print(f"Bitrate set to: {config['bitrate']}")
            
        elif choice == "5":
            if 'nvenc' in config['codec']:
                preset_index = (preset_index + 1) % len(temporary.nvenc_presets)
                config['preset'] = temporary.nvenc_presets[preset_index]
                save_configuration(config)
                print(f"NVENC Preset set to: {config['preset']}")
            else:
                break  # Back to main menu
                
        elif choice == "6" and max_choice == 6:
            break  # Back to main menu
            
        else:
            print("Invalid choice. Please try again.")

def display_system_info():
    """
    Display information about the system and available encoders.
    """
    print("\nSystem Information:")
    print(f"Python Version: {sys.version.split()[0]}")
    
    try:
        import av
        print(f"PyAV Version: {av.__version__}")
        
        # Check for available codecs
        print("\nAvailable Hardware Encoders:")
        hw_encoders = ['h264_nvenc', 'hevc_nvenc', 'h264_qsv', 'hevc_qsv']
        for encoder in hw_encoders:
            if encoder in av.codec.codecs_available:
                print(f"  ✓ {encoder}")
            else:
                print(f"  ✗ {encoder}")
                
        print("\nAvailable Software Encoders:")
        sw_encoders = ['libx264', 'libx265', 'mpeg4']
        for encoder in sw_encoders:
            if encoder in av.codec.codecs_available:
                print(f"  ✓ {encoder}")
    except ImportError:
        print("  PyAV not installed")
    
    try:
        import d3dshot
        print("\n✓ d3dshot (Desktop Duplication API) available")
    except ImportError:
        print("\n✗ d3dshot not available - screen capture will not work")
    
    input("\nPress ENTER to continue...")

def main():
    """
    The main function of the application. It initializes the capture system,
    loads the configuration, and then enters the main application loop.
    """
    if not init_nvidia_apis():
        print("\nERROR: Failed to initialize capture system.")
        print("Please ensure:")
        print("  1. You have run the installer (option 2 in batch menu)")
        print("  2. You have a compatible GPU with updated drivers")
        print("  3. All dependencies are installed")
        input("\nPress ENTER to exit...")
        sys.exit(1)
        
    config = load_configuration()
    
    print("\n" + "="*60)
    print("Geforce Hybrid Capture - ALPHA")
    print("="*60)
    print("Using Desktop Duplication API + NVENC Hardware Encoding")
    print("Compatible with driver 399.07 and GTX 1060")
    print("="*60)
    
    while True:
        display_recording_stats()
        print("\nMenu:")
        print("1. Start Recording")
        print("2. Stop Recording")
        print("3. Configure Settings")
        print("4. System Information")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            start_recording(config)
            
        elif choice == "2":
            stop_recording()
            
        elif choice == "3":
            configure_settings(config)
            # Reload config after changes
            config = load_configuration()
            
        elif choice == "4":
            display_system_info()
            
        elif choice == "5":
            if temporary.is_recording:
                print("Stopping recording before exit...")
                stop_recording()
            cleanup()
            print("Exiting.")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()