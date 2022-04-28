from PIL import Image 
import random
from sql_db import main 



def generate_random_name():

    lists = ["qwertyuiopasdfg<xvf", "dbvnhf", "nmmzxsvdfeyuy"]
    random.shuffle(lists)
    lists = ''.join(lists)
    lists += ".png"
    return lists 

def number_Of_Copies(image_name, copiesNum):
    if copiesNum <= 0:
        return None
    else:

        #generate back image with white background
        width = 1200
        height = 900
        img  = Image.new( mode = "RGB", size = (width, height), color = (255, 255,  255) )
        
        #open barcode image
        im1 = Image.open(image_name).resize((200,100))
        back_im = img.copy()
        x = 0
        y = 0
        image_counter = 1
        
        #generate copies
        for _ in range(copiesNum):
            back_im.paste(im1, (x,y))
            x += 200
            if image_counter % 6 == 0:
                y += 100
                x = 0
            else:
                y += 0

            image_counter += 1

        back_im.save('barcode.png', quality=95)













