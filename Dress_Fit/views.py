from django.shortcuts import render
from django.http.response import StreamingHttpResponse

from django.contrib import messages
from Dress_Fit import models as Umodels
from django.http import HttpResponseRedirect
import Dress_Fit.camera as webcamara
import json
from django.http import HttpResponse
from django.template import loader
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3
import numpy as np
# Create your views here.

def index(request):
	return render(request, 'Dress_Fit/home.html')

#---------------------------------------------- BOT ----------------------------------------

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.contrib import messages
# Create your views here.


import numpy as np
import cv2
from sklearn.cluster import KMeans
from collections import Counter
import imutils


import os, sys




def index(request):
     return render(request, 'home.html')




def DRESS_OVER(request):

    if request.method == 'POST':
        import cv2
        import numpy as np
        import urllib

        imagein = request.POST.get('imagein', '')
        Path_loaded = cv2.imread("overlap test images/"+imagein)
        print(Path_loaded)
        urllib.request.urlretrieve('https://i.ibb.co/BwGnzdR/man.jpg', "man")
        frame = cv2.imread("man")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define range of green color in HSV
        lower_green = np.array([25, 52, 72])
        upper_green = np.array([102, 255, 255])

        # Threshold the HSV image to get only blue colors
        mask_white = cv2.inRange(hsv, lower_green, upper_green)
        mask_black = cv2.bitwise_not(mask_white)

        # converting mask_black to 3 channels
        W, L = mask_black.shape
        mask_black_3CH = np.empty((W, L, 3), dtype=np.uint8)
        mask_black_3CH[:, :, 0] = mask_black
        mask_black_3CH[:, :, 1] = mask_black
        mask_black_3CH[:, :, 2] = mask_black

        # cv2.imshow('orignal',frame)
        # cv2.imshow('mask_white', mask_white)
        # cv2.imshow('mask_black',mask_black_3CH)

        dst3 = cv2.bitwise_and(mask_black_3CH, frame)
        # cv2.imshow('Pic+mask_inverse',dst3)

        # ----------------------------------------------
        W, L = mask_white.shape
        mask_white_3CH = np.empty((W, L, 3), dtype=np.uint8)
        mask_white_3CH[:, :, 0] = mask_white
        mask_white_3CH[:, :, 1] = mask_white
        mask_white_3CH[:, :, 2] = mask_white

        # cv2.imshow('Wh_mask',mask_white_3CH)
        dst3_wh = cv2.bitwise_or(mask_white_3CH, dst3)
        # cv2.imshow('Pic+mask_wh',dst3_wh)

        # -------------------------------------------------

        # changing for design
        # urllib.request.urlretrieve('https://m.media-amazon.com/images/I/51xt0EdcQ3L._UX679_.jpg', "dress")

        design = Path_loaded
        design = cv2.resize(design, mask_black.shape[1::-1])

        # cv2.imshow('design resize',design)

        design_mask_mixed = cv2.bitwise_or(mask_black_3CH, design)
        # cv2.imshow('design_mask_mixed',design_mask_mixed)

        final_mask_black_3CH = cv2.bitwise_and(design_mask_mixed, dst3_wh)
        output_img = cv2.resize(final_mask_black_3CH, (500, 600))

        filename = 'static/Temp_img.jpg'
        cv2.imwrite(filename, output_img)


        context = {'filename_path': filename }
        return render(request, 'DRESS_OVER.html', context)
    return render(request, 'DRESS_OVER.html')




def DRESS_ML(request):
    if request.method == 'POST':


        def extractSkin(image):
            # Taking a copy of the image
            img = image.copy()
            # Converting from BGR Colours Space to HSV
            img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            # Defining HSV Threadholds
            lower_threshold = np.array([0, 48, 80], dtype=np.uint8)
            upper_threshold = np.array([20, 255, 255], dtype=np.uint8)

            # Single Channel mask,denoting presence of colours in the about threshold
            skinMask = cv2.inRange(img, lower_threshold, upper_threshold)

            # Cleaning up mask using Gaussian Filter
            skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)

            # Extracting skin from the threshold mask
            skin = cv2.bitwise_and(img, img, mask=skinMask)

            # Return the Skin image
            return cv2.cvtColor(skin, cv2.COLOR_HSV2BGR)

        def removeBlack(estimator_labels, estimator_cluster):
            # Check for black
            hasBlack = False

            # Get the total number of occurance for each color
            occurance_counter = Counter(estimator_labels)

            # Quick lambda function to compare to lists
            def compare(x, y):
                return Counter(x) == Counter(y)

            # Loop through the most common occuring color
            for x in occurance_counter.most_common(len(estimator_cluster)):

                # Quick List comprehension to convert each of RBG Numbers to int
                color = [int(i) for i in estimator_cluster[x[0]].tolist()]

                # Check if the color is [0,0,0] that if it is black
                if compare(color, [0, 0, 0]) == True:
                    # delete the occurance
                    del occurance_counter[x[0]]
                    # remove the cluster
                    hasBlack = True
                    estimator_cluster = np.delete(estimator_cluster, x[0], 0)
                    break

            return (occurance_counter, estimator_cluster, hasBlack)

        def getColorInformation(estimator_labels, estimator_cluster, hasThresholding=False):
            # Variable to keep count of the occurance of each color predicted
            occurance_counter = None

            # Output list variable to return
            colorInformation = []

            # Check for Black
            hasBlack = False

            # If a mask has be applied, remove th black
            if hasThresholding == True:

                (occurance, cluster, black) = removeBlack(estimator_labels, estimator_cluster)
                occurance_counter = occurance
                estimator_cluster = cluster
                hasBlack = black

            else:
                occurance_counter = Counter(estimator_labels)

            # Get the total sum of all the predicted occurances
            totalOccurance = sum(occurance_counter.values())

            # Loop through all the predicted colors
            for x in occurance_counter.most_common(len(estimator_cluster)):
                index = (int(x[0]))

                # Quick fix for index out of bound when there is no threshold
                index = (index - 1) if ((hasThresholding & hasBlack)
                                        & (int(index) != 0)) else index

                # Get the color number into a list
                color = estimator_cluster[index].tolist()

                # Get the percentage of each color
                color_percentage = (x[1] / totalOccurance)

                # make the dictionay of the information
                colorInfo = {"cluster_index": index, "color": color,
                             "color_percentage": color_percentage}

                # Add the dictionary to the list
                colorInformation.append(colorInfo)

            return colorInformation

        def extractDominantColor(image, number_of_colors=5, hasThresholding=False):
            # Quick Fix Increase cluster counter to neglect the black
            if hasThresholding == True:
                number_of_colors += 1

            # Taking Copy of the image
            img = image.copy()

            # Convert Image into RGB Colours Space
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Reshape Image
            img = img.reshape((img.shape[0] * img.shape[1]), 3)

            # Initiate KMeans Object
            estimator = KMeans(n_clusters=number_of_colors, random_state=0)

            # Fit the image
            estimator.fit(img)

            # Get Colour Information
            colorInformation = getColorInformation(estimator.labels_, estimator.cluster_centers_, hasThresholding)
            return colorInformation

        def prety_print_data(color_info):
            for x in color_info:
                #     print(pprint.pformat(x))
                11

        def compute(img, min_percentile, max_percentile):
            max_percentile_pixel = np.percentile(img, max_percentile)
            min_percentile_pixel = np.percentile(img, min_percentile)

            return max_percentile_pixel, min_percentile_pixel

        def aug(src):
            if get_lightness(src) < 130:
                print("The brightness of the picture is not sufficient, so enhancement is required.")

            max_percentile_pixel, min_percentile_pixel = compute(src, 1, 99)

            # Remove values ​​outside the quantile range
            src[src >= max_percentile_pixel] = max_percentile_pixel
            src[src <= min_percentile_pixel] = min_percentile_pixel

            # Stretch the quantile range from 0 to 255. 255*0.1 and 255*0.9 are taken here because pixel values ​​may overflow, so it is best not to set it to 0 to 255.
            out = np.zeros(src.shape, src.dtype)
            cv2.normalize(src, out, 255 * 0.1, 255 * 0.9, cv2.NORM_MINMAX)

            return out

        def get_lightness(src):
            # Calculate brightness
            hsv_image = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
            lightness = hsv_image[:, :, 2].mean()

            return lightness

        imagein = request.POST.get('imagein', '')
        print("Selected the path here")
        print(imagein)

        image = cv2.imread("TestImages/" + imagein)

        # Resize image to a width of 250
        image = imutils.resize(image, width=250)

        # Show image
        # plt.subplot(3, 1, 1)
        # plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # plt.title("Original Image")
        # plt.show()

        # Apply Skin Mask
        skin = extractSkin(image)

        # Find the dominant color. Default is 1 , pass the parameter 'number_of_colors=N' where N is the specified number of colors
        dominantColors = extractDominantColor(skin, hasThresholding=True)

        # Show in the dominant color information
        # print("Color Information")

        def getSkinTone(colorInformation):
            skinToneColor = sum(colorInformation[0]['color'])
            if skinToneColor < 250:
                userSkinTone = "Medium"

                return userSkinTone
            elif skinToneColor > 250 and skinToneColor < 500:
                userSkinTone = "Medium"

                return userSkinTone
            else:
                userSkinTone = "Fair"
            return userSkinTone

        prety_print_data(dominantColors)

        skinTone = getSkinTone(dominantColors)
        print(skinTone)

        import os

        skinTone0 = "static/Recommend/"+skinTone
        skinTone = os.listdir(skinTone0)
        print(skinTone)


        context = {'skinTone': skinTone , 'skinTone0':skinTone0}
        return render(request, 'DRESS_ML.html', context)

    return render(request, 'DRESS_ML.html')


from tkinter import *
from PIL import Image, ImageTk
import os

def DRESS_OVER2(request):
    global sht_in , pnt_in
    if 'shirt_dis' in request.POST:
        print("DONEEEEEEEEEEEEEEE")
        sht_in = ("-1")
    elif 'shirt_red' in request.POST:
        print("DONEEEEEEEEEEEEEEE")
        sht_in = ("0")
    elif 'shirt_creme' in request.POST:
        print("DONEEEEEEEEEEEEEEE")
        sht_in = ("1")
    elif 'shirt_yellow' in request.POST:
        print("DONEEEEEEEEEEEEEEE")
        sht_in = ("2")

    elif 'shirt_blue' in request.POST:
        print("DONEEEEEEEEEEEEEEE")
        sht_in = ("3")
    elif 'shirt_pink' in request.POST:
        print("DONEEEEEEEEEEEEEEE")
        sht_in = ("4")


    if 'pant_dis' in request.POST:
        print("DONEEEEEEEEEEEEEEE")
        pnt_in = ("-1")
    elif 'fullpant_olive' in request.POST:
        print("DONEEEEEEEEEEEEEEE")
        pnt_in =("0")
    elif 'fullpant_white' in request.POST:
        print("DONEEEEEEEEEEEEEEE")
        pnt_in =("1")
    elif 'fullpant_blue' in request.POST:
        print("DONEEEEEEEEEEEEEEE")
        pnt_in = ("5")

    elif 'fullpant_red' in request.POST:
        print("DONEEEEEEEEEEEEEEE")
        pnt_in = ("4")

    elif 'fullpant_green' in request.POST:
        print("DONEEEEEEEEEEEEEEE")
        pnt_in = ("3")



    if 'load_video' in request.POST:

        shirt_color_dict = {"DISABLED.png": '-1', "full_shirt_red.png": '0', "full_shirt_creme.png": '1',
                            "full_shirt_yellow.png": '2', "full_shirt_blue.png": '3', "full_shirt_pink.png": '4'}

        pant_color_dict = {"DISABLED.png": '-1', "fullpant_olive.png": '0', "fullpant_white.png": '1',
                           "fullpant_blue.png": '2',
                           "fullpant_green.png": '3', "fullpant_red.png": '4', "fullpant_brown.png": '5'}

        glass_color_dict = {"DISABLED.png": '-1', "glasses0.png": '0', "glasses1.png": '1', "glasses2.png": '2',
                            "glasses3.png": '3'}

        def clicked():
            shirtcolor_val = shirt_color_dict[str(shirtcolor.get())]
            print(shirtcolor_val)

            pantcolor_val = pant_color_dict[str(pantcolor.get())]
            print(pantcolor_val)
            glasssrc = glass_color_dict[str(glasscolor.get())]
            shirt_size = str(shirtsize.get())
            pant_size = str(pantsize.get())
            print(shirtcolor_val, pantcolor_val, glasssrc, shirt_size, pant_size)
            os.system(
                "python Main.py " + str(sht_in) + " " + str(pnt_in) + " " + str(-1) + " " + shirt_size + " " + pant_size)

        def clicked1():
            print("Running pose detector")
            os.system("python Pose_est.py")

        def changeshirt():
            load = Image.open("images/" + str(shirtcolor.get()))
            if str(shirtcolor.get()) == "DISABLED.png":
                load = load.resize((200, 200), Image.ANTIALIAS)
            else:
                load = load.resize((150, 200), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(load)

        #    shirt.configure(image=render)
        #    shirt.image = render
        # if str(shirtcolor.get()) == "DISABLED.png":
        #     shirt.grid(column=0,row=1,padx=0)
        # else:
        #     shirt.grid(column=0,row=1,padx=100)

        def changepant():
            load = Image.open("images/" + str(pantcolor.get()))
            if str(pantcolor.get()) == "DISABLED.png":
                load = load.resize((200, 200), Image.ANTIALIAS)
            else:
                load = load.resize((100, 200), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(load)

        #    pant.configure(image=render)
        #    pant.image = render

        def changeglass():
            load = Image.open("images/" + str(glasscolor.get()))
            if str(glasscolor.get()) == "DISABLED.png":
                load = load.resize((200, 200), Image.ANTIALIAS)
            else:
                load = load.resize((200, 100), Image.ANTIALIAS)
            render = ImageTk.PhotoImage(load)

        #   glass.configure(image=render)
        #   glass.image = render

        window = Tk()
        window.title("Virtual Dressing Room")

        btn = Button(window, text="sss Launch Trial", bg="orange", fg="red", font=("Comic Sans MS", 15), width=25,
                     command=clicked)
        btn.grid(column=1, row=10, pady=20)
        btn1 = Button(window, text="View Pose Estimation", bg="orange", fg="dark green", font=("Comic Sans MS", 10),
                      width=15,
                      command=clicked1)
        btn1.grid(column=2, row=10, pady=20)
        shirtcolor = StringVar()
        pantcolor = StringVar()
        glasscolor = StringVar()
        shirtsize = StringVar()
        pantsize = StringVar()

        shirt_rad1 = Radiobutton(window, variable=shirtcolor, width=10, indicator=0, background="light blue",
                                 text='Disable',
                                 value="DISABLED.png", command=changeshirt, justify=LEFT, compound=LEFT,
                                 font=("Comic Sans MS", 10))
        shirt_rad1.select()
        shirt_rad2 = Radiobutton(window, variable=shirtcolor, width=10, indicator=0, background="light blue",
                                 text='REDa',
                                 value="full_shirt_red.png", command=changeshirt, justify=LEFT, compound=LEFT,
                                 font=("Comic Sans MS", 10))

        shirt_rad3 = Radiobutton(window, variable=shirtcolor, width=10, indicator=0, background="light blue",
                                 text='CREME',
                                 value="full_shirt_creme.png", command=changeshirt, justify=LEFT, compound=LEFT,
                                 font=("Comic Sans MS", 10))

        shirt_rad4 = Radiobutton(window, variable=shirtcolor, width=10, indicator=0, background="light blue",
                                 text='YELLOW',
                                 value="full_shirt_yellow.png", command=changeshirt, justify=LEFT, compound=LEFT,
                                 font=("Comic Sans MS", 10))

        shirt_rad5 = Radiobutton(window, variable=shirtcolor, width=10, indicator=0, background="light blue",
                                 text='BLUE',
                                 value="full_shirt_blue.png", command=changeshirt, justify=LEFT, compound=LEFT,
                                 font=("Comic Sans MS", 10))

        shirt_rad6 = Radiobutton(window, variable=shirtcolor, width=10, indicator=0, background="light blue",
                                 text='PINK',
                                 value="full_shirt_pink.png", command=changeshirt, justify=LEFT, compound=LEFT,
                                 font=("Comic Sans MS", 10))

        shirt_rad1.grid(column=0, row=2, sticky='w', padx=100)
        shirt_rad2.grid(column=0, row=3, sticky='w', padx=100)
        shirt_rad3.grid(column=0, row=4, sticky='w', padx=100)
        shirt_rad4.grid(column=0, row=5, sticky='w', padx=100)
        shirt_rad5.grid(column=0, row=6, sticky='w', padx=100)
        shirt_rad6.grid(column=0, row=7, sticky='w', padx=100)

        pant_rad1 = Radiobutton(window, variable=pantcolor, width=10, indicator=0, background="light blue",
                                text='Disable',
                                value="DISABLED.png", command=changepant, justify=LEFT, font=("Comic Sans MS", 10))
        pant_rad1.select()
        pant_rad2 = Radiobutton(window, variable=pantcolor, width=10, indicator=0, background="light blue",
                                text='OLIVE',
                                value="fullpant_olive.png", command=changepant, justify=LEFT,
                                font=("Comic Sans MS", 10))
        pant_rad3 = Radiobutton(window, variable=pantcolor, width=10, indicator=0, background="light blue",
                                text='WHITE',
                                value="fullpant_white.png", command=changepant, justify=LEFT,
                                font=("Comic Sans MS", 10))
        pant_rad4 = Radiobutton(window, variable=pantcolor, width=10, indicator=0, background="light blue", text='BLUE',
                                value="fullpant_blue.png", command=changepant, justify=LEFT, font=("Comic Sans MS", 10))
        pant_rad5 = Radiobutton(window, variable=pantcolor, width=10, indicator=0, background="light blue",
                                text='GREEN',
                                value="fullpant_green.png", command=changepant, justify=LEFT,
                                font=("Comic Sans MS", 10))
        pant_rad6 = Radiobutton(window, variable=pantcolor, width=10, indicator=0, background="light blue", text='RED',
                                value="fullpant_red.png", command=changepant, justify=LEFT, font=("Comic Sans MS", 10))
        pant_rad7 = Radiobutton(window, variable=pantcolor, width=10, indicator=0, background="light blue",
                                text='BROWN',
                                value="fullpant_brown.png", command=changepant, justify=LEFT,
                                font=("Comic Sans MS", 10))
        pant_rad1.grid(column=1, row=2, sticky='w', padx=200)
        pant_rad2.grid(column=1, row=3, sticky='w', padx=200)
        pant_rad3.grid(column=1, row=4, sticky='w', padx=200)
        pant_rad4.grid(column=1, row=5, sticky='w', padx=200)
        pant_rad5.grid(column=1, row=6, sticky='w', padx=200)
        pant_rad6.grid(column=1, row=7, sticky='w', padx=200)
        pant_rad7.grid(column=1, row=8, sticky='w', padx=200)

        glass_rad1 = Radiobutton(window, variable=glasscolor, width=10, indicator=0, background="light blue",
                                 text='Disable',
                                 value="DISABLED.png", command=changeglass, justify=LEFT, font=("Comic Sans MS", 10))
        glass_rad1.select()
        glass_rad2 = Radiobutton(window, variable=glasscolor, width=10, indicator=0, background="light blue",
                                 text='GREY',
                                 value="glasses0.png", command=changeglass, justify=LEFT, font=("Comic Sans MS", 10))
        glass_rad3 = Radiobutton(window, variable=glasscolor, width=10, indicator=0, background="light blue",
                                 text='GOLD-RIM',
                                 value="glasses1.png", command=changeglass, justify=LEFT, font=("Comic Sans MS", 10))
        glass_rad4 = Radiobutton(window, variable=glasscolor, width=10, indicator=0, background="light blue",
                                 text='RED',
                                 value="glasses2.png", command=changeglass, justify=LEFT, font=("Comic Sans MS", 10))
        glass_rad5 = Radiobutton(window, variable=glasscolor, width=10, indicator=0, background="light blue",
                                 text='THUG-LIFE',
                                 value="glasses3.png", command=changeglass, justify=LEFT, font=("Comic Sans MS", 10))
        glass_rad1.grid(column=2, row=2, sticky='w', padx=50)
        glass_rad2.grid(column=2, row=3, sticky='w', padx=50)
        glass_rad3.grid(column=2, row=4, sticky='w', padx=50)
        glass_rad4.grid(column=2, row=5, sticky='w', padx=50)
        glass_rad5.grid(column=2, row=6, sticky='w', padx=50)

        shirt_sizer = Frame(window, background="light blue")
        shirt_sizer.grid(column=0, row=9, sticky='w', padx=50, pady=10)
        for i, text in enumerate(['XS', 'S', 'M', 'L', 'XL']):
            Label(shirt_sizer, text=text, background="light blue").grid(row=0, column=i, padx=10, sticky="w")

        slider1 = Scale(shirt_sizer, showvalue=0, from_=1, to=5, length=180, orient=HORIZONTAL, relief="sunken",
                        background="light blue", variable=shirtsize)
        slider1.grid(row=1, column=0, columnspan=5, ipadx=0)

        pant_sizer = Frame(window, background="light blue")
        pant_sizer.grid(column=1, row=9, sticky='w', padx=150, pady=10)
        for i, text in enumerate(['XS', 'S', 'M', 'L', 'XL']):
            Label(pant_sizer, text=text, background="light blue").grid(row=0, column=i, padx=10, sticky="w")

        slider2 = Scale(pant_sizer, showvalue=0, from_=1, to=5, length=180, orient=HORIZONTAL, relief="sunken",
                        background="light blue", variable=pantsize)
        slider2.grid(row=1, column=0, columnspan=5, ipadx=0)
        lbl2 = Label(window, text="Click to start trial\n Press Q anytime to quit", font=("Comic Sans MS", 10),
                     background="light blue")
        lbl2.grid(row=11, column=1, pady=10)

        clicked()








    return render(request, 'DRESS_OVER2.html')



def AdminLogin(request):
    if request.method == 'POST':
        UserName = request.POST.get('UserName', '')
        Password = request.POST.get('Password', '')

        User_found = Umodels.admin_user.objects.all().filter(UserName=UserName, Password=Password).count()
        if User_found > 0:
            #	print("Pass")
            request.session['UserName'] = UserName
            return render(request, 'Dress_Fit/Cust_orders.html')

        else:
            #	print("Failed")
            messages.success(request, 'Invalid ! Please Check Your UserName and Password')
            return HttpResponseRedirect(request.path_info)

    return render(request, 'Dress_Fit/AdminLogin.html')






