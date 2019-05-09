from PIL import Image, ImageDraw
from PIL.ImageColor import colormap
import string
import pathlib

# Coordinates: x:horizontal,y vertical. (x,y)=(0,0) upper -left
# coordinate of the first and last(A,K) hold column (in pixels )
XMIN, XMAX = 61, 389
# coordinate of the first and last(18,1) hold row (in pixels)
YMIN, YMAX = 56, 612
#image size
W,H = None,None

#xy hold spacing
DX = (XMAX - XMIN) / 10.0
DY = (YMAX - YMIN) / 17.

#XY columns/rows  holds names
X_GRID_NAMES = string.ascii_uppercase[0:11]
Y_GRID_NAMES = list(range(1, 19))

# holds row/columns coordinates (in pixels)
X = {xk:int(XMIN + n * DX) for n,xk in enumerate(X_GRID_NAMES)}
Y = {yk:int(YMIN + (18-yk) * DY) for yk in Y_GRID_NAMES}

IMG_FOLDER_PATH = pathlib.Path(__file__).resolve().parent.joinpath("img")

def background_image_path(setup, holdset):
    #return path of image of the specified holsets
    hold_setup = [f"{h}_{setup}" for h in sorted(holdset)]
    name = "-".join(hold_setup)
    return IMG_FOLDER_PATH.joinpath(name + ".png")

def emphHold(img, xc, yc, color, width=4):
    """draw rectagle around hold position"""
    x,y = X[xc],Y[yc]
    draw = ImageDraw.Draw(img)
    for i in range(width):
        draw.rectangle([x - DX / 2 + i, y - DY / 2 + i, x + DX / 2 - i, y + DY / 2 - i], outline=color)
    return img

def draw_Problem(setup, holdset, holds, hold_colors={}):
    """draw problen and save image """
    bg_image_path = background_image_path(setup, holdset)
    bg_image = Image.open(bg_image_path)

    colors = {k: hold_colors.get(k, (255, 0, 0)) for k in holds.keys()}

    for k,holds in holds.items():
        color = colors[k]
        for h in holds:
            emphHold(bg_image,h[0],int(h[1:]),color)
    return bg_image

if __name__=="__main__":
    """
    draw grid on image for testing coordinates
    """

    colors = {
        'MOVE': colormap["red"],
        'TOP': colormap["blue"],
        'START': colormap["violet"]
    }
    holds = {
        'MOVE': [f"F{c}"for c in Y_GRID_NAMES],
        'TOP': [f"{r}{Y_GRID_NAMES[-1]}" for r in X_GRID_NAMES],
        'START': [f"{r}1" for r in X_GRID_NAMES]
    }
    image = draw_Problem("2016", ['A', 'B', 'OS'],
                         holds=holds, hold_colors=colors)

    W,H = image.size
    draw = ImageDraw.Draw(image)

    for k,x in X.items():
        draw.line((x, 0,x,H), fill=colormap["red"])
    for k,y in Y.items():
        draw.line((0,y,W,y), fill=colormap["black"])

    image.save("test_image.png","PNG")
