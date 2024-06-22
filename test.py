import time
import sys

def load_modules():
    # Print the initial message
    print("loading modules...", end='', flush=True)
    
    # Simulate a loading process
    time.sleep(3)  # Replace this with actual loading code
    
    # Print the final message
    print("\rloading modules... Done!", flush=True)

# Call the function
load_modules()
