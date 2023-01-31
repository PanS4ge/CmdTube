import youtube_dl
import pytube
import string
import sys
from PIL import Image
import cv2
import glob
import os

def mp4topng():
    # Read the video from specified path
    name = sys.argv[0]

    cam = cv2.VideoCapture(os.getcwd().replace(name, "") + "\\vid.mp4")

    try:

        # creating a folder named data
        if not os.path.exists('data'):
            os.makedirs('data')

    # if not created then raise error
    except OSError:
        print('Error: Creating directory of data')

    # frame
    currentframe = 0

    while (True):
        # reading from frame
        ret, frame = cam.read()

        if ret:
            # if video is still left continue creating images
            name = './data/frame' + str(currentframe) + '.jpg'
            #print('Creating...' + name)

            # writing the extracted images
            cv2.imwrite(name, frame)

            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

def convert(image):
    # pass the image as command line argument
    img = Image.open(image)

    # resize the image
    width, height = img.size
    aspect_ratio = height/width
    new_width = 120
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
    # new size of image
    # print(img.size)

    # convert image to greyscale format
    img = img.convert('L')

    pixels = img.getdata()

    # replace each pixel with a character from array
    #chars = ["B","S","#","&","@","$","%","*","!",":","."]
    chars = string.punctuation + string.digits + string.ascii_letters
    new_pixels = [chars[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)

    # split string of chars into multiple strings of length equal to new width and create a list
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)

    return ascii_image

page = -1
MAINPAGE = ['Exit', 'Search']

def handlePage(handl):
    if(handl == 0):
        exit()
    elif(handl == 1):
        s = pytube.Search(str(input("Search query >> ")))
        #print(s.results)
        for x in range(len(s.results)):
            if(hasattr(s.results[x], "title")):
                print(f"[{x}] {s.results[x].title}")
        which = int(input("Which one? >> "))
        if(which > len(s.results)):
            print("Wrong answer")
            handlePage(handl)
        else:
            v = s.results[which]
            print(f"You selected: {v.title}")
            print(f"Uploaded by: {v.author}")
            print(f"Length is {v.length}")
            print(f"Views: {v.views}")
            print(f"Sent on {v.publish_date}")
            print(f"Rating: {v.rating}")
            print(f"Watch        - put \"W\"")
            print(f"Go Back      - put \"B\"")
            c = str(input("Choice: "))
            if("w" == c.lower()):
                watch(v)
            else:
                page = -1
                mainPage()
            #print(f"{v.description}")

def watch(vid):
    #print("Here will be watchin'")
    #youtube = pytube.YouTube(vid.watch_url).streams.get_highest_resolution()
    #youtube.download(output_path=os.getcwd().replace(name, "") + "\\vid.mp4")
    #mp4topng()
    #a = glob.glob(output_path=os.getcwd().replace(name, "") + "\\data\\")
    #for x in a:
    #    print(convert(x))
    os.system(f"cmd /c start {vid.watch_url}")

def mainPage():
    for x in range(len(MAINPAGE)):
        print(f"[{x}] {MAINPAGE[x]}")
    yourPage = int(input("Selection >> "))
    if(yourPage > len(MAINPAGE)):
        print("Please validate your selection")
        mainPage()
    page = yourPage
    handlePage(page)

if(page == -1):
    mainPage()