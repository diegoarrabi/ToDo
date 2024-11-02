from config import timeLabel, myLog, getDialog, path_dict, add_legominifigure, lego_config
from os import remove, path, listdir
from time import sleep
from PIL import Image
from subprocess import run


def main():

    file_prefix = "_"
    file_basename = "stockWallpaper"
    new_ext = ".png"
    screen_size = getScreenSize()
    directory_images = path_dict['images']

    # save_path = path.join(directory_images, (file_basename + timeLabel(file_prefix) + new_ext))

    save_path = path.join(directory_images, ("Wallpaper" + new_ext))

    deleteWallpaper(directory_images)

    newWallpaper = createWallpaper(
        file_basename, screen_size[0], screen_size[1])
    newWallpaper.save(save_path, "png")

    py_script = "makeTable.py"
    script = path.join(path_dict['Project'], py_script)
    run(['python3', script])
    return


def getScreenSize() -> list[int]:
    """
    Uses osascript to get size of display

    Returns:
        list[int]: [width*2, height*2]
    """
    script = 'tell application "Finder" to return (bounds of window of desktop)'
    process_return = run(
        ["osascript", "-e", script], capture_output=True, text=True)
    stdout_raw = (process_return.stdout).strip()
    stderr_raw = (process_return.stderr).strip()
    if stderr_raw != "":
        myLog(stderr_raw)
        getDialog("Error getting Display Size", True)
    display_matrix = stdout_raw.split(',')
    return [int(var)*2 for var in display_matrix if int(var) != 0]


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
    


def createWallpaper(basename: str, screen_width: int, screen_height: int):
    stock_wallpaper_path = path.join(path_dict['images'], f'{basename}.jpg')
    stock_wallpaper_image = Image.open(stock_wallpaper_path)
    if not add_legominifigure:
        return stock_wallpaper_image
    lego_filename = "legoMiniFigure.png"
    lego_path = path.join(path_dict['images'], lego_filename)
    lego_image = Image.open(lego_path)
    lego_width = round((lego_image.width) * lego_config['resize_ratio'])
    lego_height = round((lego_image.height) * lego_config['resize_ratio'])
    lego_x_coord = round(screen_width * lego_config['x_percent'])
    lego_y_coord = round(screen_height * lego_config['y_percent'])
    new_lego_image = lego_image.resize([lego_width, lego_height])
    new_lego_image = new_lego_image.rotate(lego_config['rotation'])
    _, _, _, mask = new_lego_image.split()
    stock_wallpaper_image.paste(
        new_lego_image, [lego_x_coord, lego_y_coord], mask)
    lego_image.close()
    new_lego_image.close()
    return stock_wallpaper_image


if __name__ == '__main__':
    main()
