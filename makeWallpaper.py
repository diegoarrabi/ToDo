from os import listdir, path
from subprocess import run

from PIL import Image, ImageDraw

from config import log, myLog, path_dict, tableStyle, timeLabel

############################################################################


def makeWallpaper(arg: list = []):
    myLog("__makeWallpaper.py__")

    images_dir = path_dict["images"]
    base_wallpaper_name = "Wallpaper.png"
    base_wallpaper_name_MultiDisplay = "WallpaperMultiDisplay.png"
    wallpaper_name = getDisplayInfo(base_wallpaper_name, base_wallpaper_name_MultiDisplay)

    new_wallpaper_partial_name = "ToDoWallpaper"
    new_wallpaper_name = new_wallpaper_partial_name + timeLabel("_") + ".png"
    base_wallpaper_path = path.join(images_dir, wallpaper_name)
    new_wallpaper_savepath = path.join(images_dir, new_wallpaper_name)
    table_path = getTablePath(images_dir)
    
    deletePreviousWallpaper(images_dir)

    if table_path == "":
        todoListEmpty(base_wallpaper_path, new_wallpaper_savepath)
    else:
        createBoxTable(table_path, base_wallpaper_path, new_wallpaper_savepath)

    updateWallpaper(new_wallpaper_savepath)
    myLog("-[ DONE ]-")


############################################################################
############################################################################
############################################################################


def getDisplayInfo(wallpaper_retina: str, wallpaper_multidisplay: str) -> str:
    applescript = """set screen_width to (do shell script "system_profiler SPDisplaysDataType | awk '/Resolution/{print $2}'")"""
    script_output = run(["osascript", "-e", applescript], capture_output=True, text=True)
    screen_size = (script_output.stdout).strip().lstrip().splitlines()
    if screen_size[0] == "2560":
        return wallpaper_multidisplay
    elif screen_size[0] == "3024":
        return wallpaper_retina
    else:
        return wallpaper_retina


def deletePreviousWallpaper(directory_path: str) -> None:
    """
    Deletes previous wallpaper.
    Searches directory for file containting basename and time-prefix but not actual time.
    This allows for saving and recovering image without having to store it in a dedicated directory.

    Args:
        directory_path (str): Main Image Directory Path
    """

    myLog("method: deletePreviousWallpaper")
    previous_wallpaper = [x for x in listdir(directory_path) if x.startswith("ToDoWallpaper_")]
    if len(previous_wallpaper) == 0:
        return
    previous_path = path.join(directory_path, previous_wallpaper[0])
    run(["rm", "-f", previous_path])


############################################################################


def getTablePath(directory_path: str) -> str:
    """
    Iterates through project's image directory in search of image of table.
    If to-do list is empty and no table exists, it returns an empty string.

    Args:
        directory_path (str): Full path of images directory

    Returns:
        str: Full path to image of to-do list table OR empty string if to-do list is empty
    """

    myLog("method: getTablePath")
    table_image = [x for x in listdir(directory_path) if x.startswith("table")]
    if len(table_image) == 0:
        return ""
    return path.join(directory_path, table_image[0])


############################################################################


def todoListEmpty(stockwallpaper_path: str, savepath: str) -> None:
    """
    Takes the blank stock_wallpaper and saves it with a new name.
    A new name is needed for applescript to actually update the wallpaper on change.

    Args:
        stockwallpaper_path (str): Full path to Stock Wallpaper
        savepath (str): Full path to New Wallpaper
    """
    myLog("method: todoListEmpty")
    wallpaper_py = Image.open(stockwallpaper_path)
    wallpaper_py.save(savepath, "png")
    wallpaper_py.close()


############################################################################


def createBoxTable(table_image_path: str, stock_wallpaper: str, savepath: str) -> None:
    """
    Pastes to-do list table image on top of a rounded rectangle image to appear as a border.
    Pastes the new bordered table image to the stock wallpaper and saves it with a unique timestamped name.

    Args:
        table_image_path (str): Full path to to-do list table image
        stock_wallpaper (str): Full path to stock wallpaper
        savepath (str): Full path of new wallpaper to be saved with a unique timestamped name
    """

    def makeRect(image_width: int, image_height: int) -> Image:
        """
        Makes a colored rounded rectangle.
        Used to give the todo list a border once pasted (this step occurs elsewhere in the code)

        Args:
            image_width (int): image width
            image_height (int): image height

        Returns:
            Image: Image Object; rounded rectangle
        """
        myLog("method: makeRect [method: createBoxTable]")
        color_style = tableStyle()
        box_background = color_style["box_color"]
        box_background = "#" + str(box_background)
        corner_radius = 100

        box_py = Image.new("RGBA", (image_width, image_height))
        draw_py = ImageDraw.Draw(box_py)
        draw_py.rounded_rectangle(((0, 0), (image_width, image_height)), corner_radius, fill=box_background)
        return box_py

    myLog("method: createBoxTable")
    screen_x = 80
    screen_y = 475
    crop = 5
    table_image_py = Image.open(table_image_path)
    table_image_py = table_image_py.crop((crop, crop, table_image_py.width - crop, table_image_py.height - crop))

    table_width = table_image_py.width
    table_height = table_image_py.height
    # width_ratio = (1+(4.75/100))
    # height_ratio = (1+(7/100))
    # top_shift_ratio = (20.5/100)
    width_ratio = 1 + (6 / 100)
    height_ratio = 1 + (20 / 100)
    top_shift_ratio = 40 / 100
    # new_width = round(table_width * width_ratio)
    # new_height = round(table_height * height_ratio)
    new_width = round(table_width + 100)
    new_height = round(table_height + 150)
    border_image_py = makeRect(new_width, new_height)
    table_x = round((new_width - table_width) / 2)
    table_y = round(round((new_height - table_height)) * top_shift_ratio)

    bordered_table_py = border_image_py.resize([new_width, new_height])
    border_image_py.close()
    bordered_table_py.paste(table_image_py, [table_x, table_y])
    table_image_py.close()
    wallpaper_image_py = Image.open(stock_wallpaper)

    resize_ratio = 0.5
    new_table_width = round((bordered_table_py.width) * resize_ratio, None)
    new_table_height = round((bordered_table_py.height) * resize_ratio, None)
    final_table_py = bordered_table_py.resize([new_table_width, new_table_height])
    bordered_table_py.close()
    _, _, _, mask = final_table_py.split()
    wallpaper_image_py.paste(final_table_py, (screen_x, screen_y), mask)
    final_table_py.close()

    wallpaper_image_py.save(savepath, "png")
    wallpaper_image_py.close()


############################################################################


def updateWallpaper(item_path: str) -> None:
    """
    Updates wallpaper with image passed.
    For immediate effects, requires a filename different than the current wallpaper.

    Args:
        item_path (str): Full Path to image to use as wallpaper
    """
    myLog("method: updateWallpaper")
    script = 'tell application "Finder" to set desktop picture to POSIX file "%s"' % (item_path)
    try:
        run(["osascript", "-e", script], capture_output=True, text=True)
    except Exception:
        myLog("DataFrame_Image Module Error", log.ERROR)


############################################################################


if __name__ == "__main__":
    makeWallpaper()
