import subprocess
import os
import time
import keyboard

# Paths to the scripts
face_detection_script = r"C:\fork\Python_microcontroller_v1\Python\System for loading data from the camera\main.py"
microcontroller_script = r"C:\fork\Python_microcontroller_v1\Thonny\Microcontroller.py"
simulation_script = r"C:\fork\Python_microcontroller_v1\Python\Reaction simulation system\main.py"

# Path to the Python interpreter (within a virtual environment)
python_interpreter = r"C:\fork\Python_microcontroller_v1\Python\Smart Control Center\venv\Scripts\python.exe"

# Error log file path
log_file = "error_log.txt"


def wait_for_file(filepath, timeout=5):
    """
    Waits for a file to appear in the filesystem within a specified timeout period.

    Parameters:
        filepath (str): The full path of the file to monitor.
        timeout (int, optional): Maximum time in seconds to wait for the file. Defaults to 5 seconds.

    Returns:
        bool: True if the file is detected within the timeout; otherwise, False.

    If the file is not detected within the timeout, an error message is logged to the error log file.
    """
    start_time = time.time()
    while not os.path.exists(filepath):
        # Check if the waiting time has exceeded the timeout limit.
        if time.time() - start_time > timeout:
            with open(log_file, "a") as log:
                log.write(f"ERROR: File {filepath} did not appear within {timeout} seconds!\n")
            return False
        time.sleep(0.1)  # Check every 100 milliseconds.
    return True


# Launch the scripts in their respective directories using the specified Python interpreter.
# The 'cwd' parameter sets the current working directory for each process.
# Errors (stderr) are redirected to the log file for later analysis.

face_proc = subprocess.Popen(
    [python_interpreter, face_detection_script],
    cwd=os.path.dirname(face_detection_script),
    stderr=open(log_file, "a")
)

micro_proc = subprocess.Popen(
    [python_interpreter, microcontroller_script],
    cwd=os.path.dirname(microcontroller_script),
    stderr=open(log_file, "a")
)

sim_proc = subprocess.Popen(
    [python_interpreter, simulation_script],
    cwd=os.path.dirname(simulation_script),
    stderr=open(log_file, "a")
)

print("Processes started. Press 'q' to terminate all processes.")

# Main loop to monitor for the 'q' key press.
# When 'q' is pressed, termination signals are sent to all subprocesses.
try:
    while True:
        if keyboard.is_pressed("q"):
            print("\nTerminating all processes...")
            face_proc.terminate()
            micro_proc.terminate()
            sim_proc.terminate()
            break
        time.sleep(0.1)  # Sleep to minimize CPU usage during the loop.
except KeyboardInterrupt:
    # If the user interrupts the script (e.g., with Ctrl+C), the exception is caught and the script exits gracefully.
    pass

print("Processes terminated.")
