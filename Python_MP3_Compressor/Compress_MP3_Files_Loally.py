###################################
###################################
# 1. Install 'pydub' library
# 2. Make 2 folders (directories) for input and output files
# 3. Put all your MP3 files on 'input' folder
# 4. Run the script, and enter the location of folder when asked
# 5. Specify(y/n) whether to delete the original file after compression
###################################
###################################


import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from pydub import AudioSegment

def compress_mp3(input_file, output_file, error_folder, delete_original=False, bitrate="64k"):
    """
    Compresses an MP3 file by reducing the bitrate, while showing the status of each step.
    
    Args:
        input_file (str): Path to the input MP3 file.
        output_file (str): Path where the compressed MP3 file will be saved.
        error_folder (str): Path to save the file if an error occurs during processing.
        delete_original (bool): Whether to delete the original file after compressing.
        bitrate (str): Bitrate for the compressed file. Default is 64k.
    """
    try:
        # Fetching the file
        print(f"Fetching: {os.path.basename(input_file)}")
        
        # Load the audio file
        audio = AudioSegment.from_mp3(input_file)
        
        # Compressing the file
        print(f"Compressing: {os.path.basename(input_file)}")
        
        # Export the audio file with the specified bitrate
        audio.export(output_file, format="mp3", bitrate=bitrate)
        
        # Saving the file
        print(f"Saving: {os.path.basename(output_file)}")
        
        # Delete the original file if required
        if delete_original:
            os.remove(input_file)
            print(f"Deleted original file: {os.path.basename(input_file)}")
        
        return f"File {os.path.basename(input_file)} compressed and saved successfully."
    
    except Exception as e:
        # Move problematic file to the error folder
        print(f"Error processing {input_file}: {e}")
        if not os.path.exists(error_folder):
            os.makedirs(error_folder)
        shutil.move(input_file, os.path.join(error_folder, os.path.basename(input_file)))
        return f"File {os.path.basename(input_file)} moved to Error Files due to an error."

def process_files(input_folder, output_folder, delete_original=False, bitrate="64k"):
    """
    Compress all MP3 files from the input folder and save to the output folder in parallel.
    
    Args:
        input_folder (str): Folder path containing MP3 files to compress.
        output_folder (str): Folder path where compressed files will be saved.
        delete_original (bool): Whether to delete the original file after compressing.
        bitrate (str): Bitrate for the compressed files. Default is 64k.
    """
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get list of MP3 files in the input folder
    mp3_files = [f for f in os.listdir(input_folder) if f.endswith(".mp3")]
    
    if not mp3_files:
        print(f"No MP3 files found in {input_folder}")
        return
    
    # Define error folder path
    error_folder = os.path.join(output_folder, "Error Files")
    
    # Function to handle individual file processing
    def process_file(file):
        input_file_path = os.path.join(input_folder, file)
        output_file_path = os.path.join(output_folder, file)
        return compress_mp3(input_file_path, output_file_path, error_folder, delete_original, bitrate)
    
    # Using ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        # Process files in parallel
        results = list(executor.map(process_file, mp3_files))

    # Print results for each file
    for result in results:
        print(result)

if __name__ == "__main__":
    # Input folder (you can change this to your folder location)
    input_folder = input("Enter the input folder path containing MP3 files: ").strip()

    # Output folder (you can change this to your folder location)
    output_folder = input("Enter the output folder path to save compressed files: ").strip()

    # Ask the user if they want to delete the original files after compressing
    delete_original_input = input("Do you want to delete the original files after compressing? (y/n): ").strip().lower()
    delete_original = True if delete_original_input == 'y' or delete_original_input == 'Y' else False

    # Compress with a specified bitrate (e.g., 64k)
    process_files(input_folder, output_folder, delete_original, bitrate="64k")
