#Creates compressed videos from images and makes new folders to placed there videos and other files form the same folder

import subprocess
import os
import cv2
import shutil

#if u put fourcc in the parentheses like it is supposed to be it does not work because the argument fourcc is int for some reason
def create_compress_videos(source_folder, output_folder, frame_rate, resolution, some_compression_factor, codec):
    # List all child folders in the source folder
    list_vot_child = os.listdir(source_folder)

    # Iterate through each child folder
    for child in list_vot_child:
        # Construct the path to the 'color' folder within the child folder
        color_path = os.path.join(source_folder, child, "color")

        # List all image files in the 'color' folder
        list_img_nums = os.listdir(color_path)

        # Create a folder with the same name as the video (without .mp4)
        video_folder_path = os.path.join(output_folder, child)
        os.makedirs(video_folder_path, exist_ok=True)

        # Create the name of the output video file
        video_name = child + ".mp4"
        video_full_path = os.path.join(video_folder_path, video_name)

        # Create a list of paths to each image file
        list_num_paths = [os.path.join(color_path, num) for num in list_img_nums]

        # Initialize VideoWriter properties
        cv2_fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        frame = cv2.imread(list_num_paths[0])
        size = (frame.shape[1], frame.shape[0])
        video_property = cv2.VideoWriter(video_full_path, cv2_fourcc, frame_rate, size)

        # Iterate through each image path, read the image, and write it to the video
        for img_path in list_num_paths:
            try:
                frame = cv2.imread(img_path)
                video_property.write(frame)
            except:
                print(f"Skipping {img_path} as it's not an image.")

        # Release the VideoWriter
        video_property.release()

        # Create a temporary compressed video file
        temp_compressed_path = os.path.join(video_folder_path, "temp_compressed.mp4")
        
        
        # Compress the video using FFmpeg
        command = f'ffmpeg -i "{video_full_path}" -c:v {codec} -crf {some_compression_factor} -vf scale={resolution} "{temp_compressed_path}"'
        subprocess.run(command, shell=True)
        
        # Delete or move the existing file if it exists
        if os.path.exists(video_full_path):
            os.remove(video_full_path)
        
        # Rename the temporary compressed video to the original filename
        os.rename(temp_compressed_path, video_full_path)

        # Print the output video information
        video_number = list_vot_child.index(child) + 1
        print('Outputed and compressed video number', str(video_number), 'to', video_full_path.replace("\\", "/"))

        #Copy all other files in the sequence_folders
        source_item_folder = os.path.join(source_folder, child)
        output_item_folder = os.path.join(output_folder, child)
        for item in os.listdir(source_item_folder):
            source_item = os.path.join(source_item_folder, item)
            output_item = os.path.join(output_item_folder, item)
            
            # Exclude the "color" folder
            if os.path.isfile(source_item) and item != "color":  
                shutil.copy2(source_item, output_item)
            elif os.path.isdir(source_item) and item != "color":
                shutil.copytree(source_item, output_item)

    print('Done successfully!')

if __name__ == '__main__':
    source_folder = "C:/Users/machm/fel"  # VOT dataset path with structure: MAIN -> SEQUENCES_FOLDERS -> COLOR -> IMGS_BY_NUMBER
    output_folder = "C:/Users/machm/fel2"  # where u want the result videos with compression
                                               # output structure: OUTPUT_FOLDER -> SEQUENCES_FOLDERS(name of video) -> VIDEO
    frame_rate = 30  # fps, same for all videos
    resolution = '1280x720'
    some_compression_factor = 30 # maximum is 51, it makes lower quality
    codec = 'h264'

    create_compress_videos(source_folder, output_folder, frame_rate, resolution, some_compression_factor, codec) 