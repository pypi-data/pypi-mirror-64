from PIL import Image

def cut(image, subimage_definitions):
    """Cut an image into multiple images, defined by the given boundries.

    Keyword arguments:
    image -- a PIL Image
    subimage_definitions -- a dictionary defining the subimages to cut:
        {
            "first":
            {
                "top": 0.4, # start at 40% from the top
                "bottom": 0.6, # stop at 60% from the top
                "left": 0.0, # start at 0% from the left
                "right": 1.0 # stop at 100% from the left
            }
        }
    """

    subimages = {}

    for subimage_key, subimage_definition in subimage_definitions.items():
        top = subimage_definition["top"]
        bottom = subimage_definition["bottom"]
        left = subimage_definition["left"]
        right = subimage_definition["right"]
        
        cut_image = cut_subimage(image, top, bottom, left, right)
        subimages[subimage_key] = cut_image

    return subimages
        
def cut_subimage(image, top, bottom, left, right):
    #print("Relative boundries Left=%f Right=%f Top=%f Bottom=%f" % (left, right, top, bottom))

    image_width, image_height = image.size
    #print("Image Height=%d Width=%d" % (image_height, image_width))
    
    # convert relative measure to pixels
    top = int(top * image_height)
    bottom = int(bottom * image_height)
    left = int(left * image_width)
    right = int(right * image_width)
    #print("Absolute boundries Left=%d Right=%d Top=%d Bottom=%d" % (left, right, top, bottom))

    boundry_box = (left, top, right, bottom)
    cropped_image = image.crop(boundry_box)

    return cropped_image