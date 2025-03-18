import os
import subprocess
import time

def run_python_scripts_sequentially(directory, delays):
    # List all files in the specified directory in the order of ls -la
    files = sorted(os.listdir(directory))
    
    # Filter out only Python scripts
    python_scripts = [f for f in files if f.endswith('.py')]
    
    # Run each Python script in the order they appear in the directory
    for i, script in enumerate(python_scripts):
        script_path = os.path.join(directory, script)
        print(f"Running {script_path}...")
        result = subprocess.run(['python3', script_path], capture_output=True, text=True)
        print(result.stdout)
        print(result.stderr)
        
        # Introduce a delay if it's not the last script
        if i < len(python_scripts) - 1:
            time.sleep(delays[i])

if __name__ == "__main__":

    # Specify the directory containing the Python scripts
    directory = '/aws_EC2/sequential_master' # Replace with actual directory path
    
    # Specify the delays between running each script
    delays = [5, 120, 90, 90]  # Replace with actual delay values
    
    run_python_scripts_sequentially(directory, delays)

