import glob
import os
import random
import shutil
import string
from datetime import datetime
from typing import List, Tuple, Union

import cv2
import matplotlib.pyplot as plt
import numpy as np


def create_directory(dir_path: str) -> None:
    """
    Creates a directory if it does not exist.

    Args:
        dir_path (str): The path of the directory to be created.

    Returns:
        None
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Directory Created: {dir_path}")


def generate_random_id() -> str:
    """
    Generates a random ID consisting of alphanumeric characters.

    Returns:
        str: A random alphanumeric ID of length 10.
    """
    characters = string.ascii_letters + string.digits
    random_id = "".join(random.choice(characters) for i in range(10))
    return random_id


def move_images(source_directory: str) -> None:
    """
    Moves all .jpg files from the source directory to a subdirectory named with the current timestamp.

    Args:
        source_directory (str): The path to the source directory containing .jpg files.

    Returns:
        None
    """
    # Create a subdirectory with the current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    destination_directory = os.path.join(source_directory, current_time)
    files_to_move = glob.glob(f"{source_directory}/*.jpg")

    if files_to_move:
        create_directory(destination_directory)

        # Move each file to the destination directory
        for file_path in files_to_move:
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(destination_directory, file_name)
            print(destination_path)
            shutil.move(file_path, destination_path)
            print(f"Moving: {file_name} to {destination_directory}")
    else:
        print("No images found.")
        return


def save_image(
    img_array: Union[np.ndarray, List[np.ndarray]], file_name: str
) -> List[str]:
    """
    Save image or list of images to files with appropriate file names.

    Parameters:
        - img_array (Union[np.ndarray, List[np.ndarray]]): Image or list of images as NumPy arrays.
        - file_name (str): Base file name for saving images.

    Returns:
        - List[str]: List of file paths where the images are saved.
    """
    file_paths = []
    if isinstance(img_array, list) and len(img_array) == 1:
        save_path = f"{file_name}.jpg"
        cv2.imwrite(f"{file_name}.jpg", img_array[0])
        file_paths.append(save_path)
        return file_paths

    if isinstance(img_array, list):
        for i, img in enumerate(img_array):
            save_path = f"{file_name}_{i}.jpg"
            cv2.imwrite(f"{file_name}_{i}.jpg", img)
            file_paths.append(save_path)
    else:
        cv2.imwrite(f"{file_name}.jpg", img_array)
        save_path = f"{file_name}.jpg"
        cv2.imwrite(f"{file_name}.jpg", img_array[0])
        file_paths.append(save_path)

    return file_paths


def get_image_crops(
    img_array: np.ndarray, bounding_boxes: List[Tuple[int, int, int, int]]
) -> List[np.ndarray]:
    """
    Extract image crops specified by the given bounding boxes.

    Parameters:
        - img_array (np.ndarray): Input image as a NumPy array.
        - bounding_boxes (List[Tuple[int, int, int, int]]): List of bounding boxes, each represented as (xmin, ymin, xmax, ymax).

    Returns:
        - List[np.ndarray]: List of image crops.
    """
    crop_holder = []

    for i in range(len(bounding_boxes)):
        bbox = bounding_boxes[i]
        xmin, ymin, xmax, ymax = bbox[0], bbox[1], bbox[2], bbox[3]
        crop_holder.append(img_array[ymin:ymax, xmin:xmax])

    return crop_holder


def plot_images(
    img_array: Union[np.ndarray, List[np.ndarray]],
    title: str = "Image Plot",
    fig_size: Tuple[int, int] = (15, 20),
    nrows: int = 1,
    ncols: int = 4,
) -> None:
    """
    Plot one or multiple images in a grid.

    Parameters:
        - img_array (Union[np.ndarray, List[np.ndarray]]): Image or list of images to be plotted.
        - title (str): Title of the plot (default: "Image Plot").
        - fig_size (Tuple[int, int]): Size of the figure in inches (default: (15, 20)).
        - nrows (int): Number of rows in the grid (default: 1).
        - ncols (int): Number of columns in the grid (default: 4).
    """
    if isinstance(img_array, list) and len(img_array) == 1:
        img_array = img_array[0]

    if isinstance(img_array, list):
        ncols = ncols if ncols < len(img_array) else len(img_array)
        if nrows * ncols < len(img_array):
            nrows = int(len(img_array) / ncols)
        fig, axs = plt.subplots(
            nrows=nrows, ncols=ncols, figsize=(ncols * 3, nrows * 2)
        )
        for i, ax in enumerate(axs.flatten()):
            if i < len(img_array):
                if len(img_array[i].shape) == 2:
                    cmap = "gray"
                else:
                    cmap = "cividis"
                ax.imshow(img_array[i], cmap=cmap)
        fig.suptitle(title)
        plt.tight_layout()
    else:
        if len(img_array.shape) == 2:
            cmap = "gray"
        else:
            cmap = "cividis"
        plt.figure(figsize=fig_size)
        plt.imshow(img_array, interpolation="nearest", cmap=cmap)
        plt.title(title)

    plt.show()
