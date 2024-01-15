import os
import importlib.util
import logging
from datetime import datetime
import ffmpeg

# Check if ffmpeg-python module is installed
ffmpeg_spec = importlib.util.find_spec("ffmpeg")
if ffmpeg_spec is None:
    print("ffmpeg module is not installed. Please install it and then rerun this script.")
    exit(1)

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

input_folder = r"C:\Users\urrem010\Documents\repos\ffmpeg-custom_test\samples"  # Replace with the path to your input folder
output_folder = r"C:\Users\urrem010\Documents\repos\ffmpeg-custom_test\samples\fixed"  # Replace with the path to your output folder
log_folder = r"C:\Users\urrem010\Documents\repos\ffmpeg-custom_test\logs"  # Subfolder to store log files

# Check if logs folder exist
if not os.path.exists(log_folder):
    print("Logs folder could not be found. Check if the folder path is correct.")
    exit(1)
        
# Append the date as a suffix to the log file name
today_date = datetime.now().strftime('%Y%m%d')
log_file = os.path.join(log_folder, f"log_{today_date}.txt")

# Open the log file in append mode
with open(log_file, 'a') as log:
    log.write("\n")
    log.write(f"Script execution started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

    # Check if input folder exists
    if not os.path.exists(input_folder):
        log.write("Input folder could not be found. Check if the folder path is correct.")
        exit(1)

    # Check if output folder exists
    if not os.path.exists(output_folder):
        log.write("Output folder could not be found. Check if the folder path is correct.")
        exit(1)

    # Loop through the files in the input folder
    for file in os.listdir(input_folder):
        if file.endswith('.mov'):
            input_file = os.path.join(input_folder, file)
            output_file = os.path.join(output_folder, file)

            # Modify stream metadata and overwrite the output file  
            try:
                process = (
                    ffmpeg
                    .input(input_file)
                    .output(output_file, **{'metadata:s:v:0': 'pix_fmt=rgba', 'codec': 'copy'})
                    .run_async(overwrite_output=True, pipe_stdout=True, pipe_stderr=True)
                )
                # Write ffmpeg output to the log
                log.write(f"Processing file: {file}\n")
                log.write(f"{process.communicate()}")
                log.write("\n\n")

                # Delete the processed input file
                os.remove(input_file)
            except ffmpeg.Error as e:
                    log.write(f"An error occurred while processing {file}: {e.stderr.decode('utf-8')}")

    log.write("Process completed\n\n")
