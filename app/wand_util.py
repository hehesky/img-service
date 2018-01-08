from wand.image import Image
import os.path
import db_util

def make_thumbnail(source_file,user_folder):
    imgdir=os.path.join(user_folder,source_file)
    with Image(filename=imgdir) as original:
        with original.clone() as clone:
            height=clone.height
            width=clone.width
            factor=1.0*150/height
            clone.resize(int(width*factor),int(height*factor))
            clone.save(filename=os.path.join(user_folder,"thumbnail_"+source_file))


def make_grayscale(source_file,user_folder):
    imgdir=os.path.join(user_folder,source_file)
    with Image(filename=imgdir) as original:
            with original.clone() as clone:
                clone.type='grayscale'
                clone.save(filename=os.path.join(user_folder,"grey_"+source_file))

def make_redshift(source_file,user_folder):
    imgdir=os.path.join(user_folder,source_file)
    
    with Image(filename=imgdir) as original:
        with original.clone() as clone:
            clone.evaluate(operator="rightshift",value=1,channel='blue')
            clone.evaluate(operator="leftshift",value=1,channel='red')
            clone.save(filename=os.path.join(user_folder,"redshift_"+source_file))

def make_scifi(source_file,user_folder):
    imgdir=os.path.join(user_folder,source_file)
    with Image(filename=imgdir) as original:
        with original.clone() as clone:    

            frequency = 3
            phase_shift = -90
            amplitude = 0.2
            bias = 0.7
            clone.function('sinusoid', [frequency, phase_shift, amplitude, bias])
            clone.save(filename=os.path.join(user_folder,"scifi_"+source_file))



def process_img(source_file,user_folder,username):
    #assume original img file is saved in user's folder
    """Input type (str,str) return None"""

    make_thumbnail(source_file,user_folder)

    make_grayscale(source_file,user_folder)

    make_redshift(source_file,user_folder)

    make_scifi(source_file,user_folder)
