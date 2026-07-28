# from config import timeLabel, myLog, getDialog, path_dict, add_legominifigure, lego_config
from os import remove, path, listdir
from time import sleep
from PIL import Image
from subprocess import run


def main():

    base_directory = path.dirname(__file__)

    file_basename = "stockWallpaper"
    new_ext = ".png"
    screen_size = [1800, 1169]

    directory_images = path.join(base_directory, "images")
    save_path = path.join(directory_images, ("Wallpaper" + new_ext))

    deleteWallpaper(directory_images)

    createWallpaper(directory_images, file_basename, screen_size[0], screen_size[1], save_path)
    
    return


def deleteWallpaper(directory_path: str) -> None:
    """
    Deletes previous wallpaper. Searches directory for file containting basename and time-prefix but not actual time.
    This allows for saving and recovering image without having to store it in a dedicated directory.

    Args:
        directory_path (str): Main Image Directory Path
    """
    previous_wallpaper = [x for x in listdir(directory_path) if x.startswith("Wallpaper")]
    if len(previous_wallpaper) == 0:
        return
    previous_path = path.join(directory_path, previous_wallpaper[0])
    run(["rm", "-f", previous_path])
    


def createWallpaper(image_dir: str, basename: str, screen_width: int, screen_height: int, savepath: str):
    lego_config = {
        'resize_ratio': 0.20,
        'x_percent': 0.97,
        'y_percent': 0.89,
        'rotation': 15
        }
    
    stock_wallpaper_path = path.join(image_dir, f'{basename}.jpg')

    with Image.open(stock_wallpaper_path) as stock_wallpaper_image:

        lego_filename = "legoMiniFigure.png"
        lego_path = path.join(image_dir, lego_filename)
        img_width = stock_wallpaper_image.width
        img_height = stock_wallpaper_image.height
        
        with Image.open(lego_path) as lego_image:
            # lego_image = Image.open(lego_path)
            lego_width = round((lego_image.width) * lego_config['resize_ratio'])
            lego_height = round((lego_image.height) * lego_config['resize_ratio'])
            lego_x_coord = round(img_width * lego_config['x_percent'])
            lego_y_coord = round(img_height * lego_config['y_percent'])
            
            new_lego_image = lego_image.resize([lego_width, lego_height])
            new_lego_image = new_lego_image.rotate(lego_config['rotation'])
            _, _, _, mask = new_lego_image.split()
            stock_wallpaper_image.paste(new_lego_image, [lego_x_coord, lego_y_coord], mask)
            new_lego_image.close()
        stock_wallpaper_image.save(savepath, "png")
    


if __name__ == '__main__':
    main()
