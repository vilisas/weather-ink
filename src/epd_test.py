#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# 800 x 480
#
import sys
import os
#picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd7in5b_V2
import time
import requests
from io import BytesIO
from PIL import Image,ImageDraw,ImageFont

import traceback

width=800
height=480
radar_url="https://beta.meteo.lt/data/radar/radarlarge+36.gif"
logging.basicConfig(level=logging.DEBUG)
epd = epd7in5b_V2.EPD()


def display_black(buffer):
#  epd.display(epd.getbuffer(buffer),epd.getbuffer(buffer))
  epd.send_command(0x10)
  for i in range(len(buffer)):
    buffer[i] ^= 0xFF
  epd.send_data2(buffer)
  epd.send_command(0x12)
  time.sleep(0.5)
  epd.ReadBusy()



try:
    str_time=time.strftime("%Y-%m-%d %H:%M")

#    radar_src = Image.open("./radarlarge+36.gif")
    response = requests.get(radar_url)
    radar_src = Image.open(BytesIO(response.content))


    radar_img = radar_src.crop((50,70,530,420))


    logging.info("epd7in5b_V2 meteo radar")

    font24 = ImageFont.truetype(r'./Font.ttc', 24)
    font18 = ImageFont.truetype(r'./Font.ttc', 18)
    font32 = ImageFont.truetype(r'./Font.ttc', 64)


    logging.info(("EPD width=", epd.width, " height=", epd.height))
    logging.info("init and Clear")
    epd.init()
#    epd.Clear()
    width  = epd.width
    height = epd.height



    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...")
    black_image = Image.new('1', (width, height), 255)  # 255: clear the frame
    red_image = Image.new('1', (width, height), 255)  # 255: clear the frame



#    Other = Image.new('1', (width, height), 255)  # 255: clear the frame
    draw_black = ImageDraw.Draw(black_image) # black image canvas
    draw_red = ImageDraw.Draw(red_image)

    radar_offset_x=0
    radar_offset_y=105

    black_image.paste(radar_img, (radar_offset_x, radar_offset_y))  # paste to specific location
    draw_black.rectangle((radar_offset_x, radar_offset_y, 480+radar_offset_x, 350 + radar_offset_y), outline=0)



    draw_red.text((2, height-25), ("Atnaujinta " + str_time), font = font24, fill = 0)
    draw_black.text((1, 1), 'Send dunes', font = font32, fill = 0)
    draw_black.text((5, 75), 'Radaras', font = font24, fill = 0)

    draw_black.rectangle((0, 0, width-1, height-1), outline=0)


#    draw_Himage.text((10, 0), 'hello world', font = font24, fill = 0)
#    draw_Himage.text((10, 20), '7.5inch e-Paper', font = font24, fill = 0)
#    draw_Himage.text((150, 0), u'šūdai myžalai', font = font24, fill = 0)    
#    draw_other.line((20, 50, 70, 100), fill = 0)
#    draw_other.line((70, 50, 20, 100), fill = 0)
#    draw_other.rectangle((20, 50, 70, 100), outline = 0)
#    draw_other.line((165, 50, 165, 100), fill = 0)
#    draw_Himage.line((140, 75, 190, 75), fill = 0)
#    draw_Himage.arc((140, 50, 190, 100), 0, 360, fill = 0)
#    draw_Himage.rectangle((80, 50, 130, 100), outline=0)
#    draw_Himage.chord((200, 50, 250, 100), 0, 360, fill = 0)

#    black_image.save("./output.png", format="png")
#    display_black(epd.getbuffer(black_image))
    epd.display(epd.getbuffer(black_image),epd.getbuffer(red_image))
    time.sleep(2)

#                black                 red
#    epd.display(epd.getbuffer(Himage),epd.getbuffer(Other))
#    time.sleep(2)

    # Drawing on the Vertical image
#    logging.info("2.Drawing on the Vertical image...")
#    Limage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
#    Limage_Other = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
#    draw_Himage = ImageDraw.Draw(Limage)
#    draw_Himage_Other = ImageDraw.Draw(Limage_Other)
#    draw_Himage.text((2, 0), 'hello world', font = font18, fill = 0)
#    draw_Himage.text((2, 20), '7.5inch epd', font = font18, fill = 0)
#    draw_Himage_Other.text((20, 50), u'微雪电子', font = font18, fill = 0)
#    draw_Himage_Other.line((10, 90, 60, 140), fill = 0)
#    draw_Himage_Other.line((60, 90, 10, 140), fill = 0)
#    draw_Himage_Other.rectangle((10, 90, 60, 140), outline = 0)
#    draw_Himage_Other.line((95, 90, 95, 140), fill = 0)
#    draw_Himage.line((70, 115, 120, 115), fill = 0)
#    draw_Himage.arc((70, 90, 120, 140), 0, 360, fill = 0)
#    draw_Himage.rectangle((10, 150, 60, 200), fill = 0)
#    draw_Himage.chord((70, 150, 120, 200), 0, 360, fill = 0)
#    epd.display(epd.getbuffer(Limage), epd.getbuffer(Limage_Other))
#    time.sleep(2)

#    logging.info("3.read bmp file")
#    Himage = Image.open(os.path.join(picdir, '7in5_V2_b.bmp'))
#    Himage_Other = Image.open(os.path.join(picdir, '7in5_V2_r.bmp'))
#    epd.display(epd.getbuffer(Himage),epd.getbuffer(Himage_Other))
#    time.sleep(2)

#    logging.info("4.read bmp file on window")
#    Himage2 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
#    Himage2_Other = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
#    bmp = Image.open(os.path.join(picdir, '2in9.bmp'))
#    Himage2.paste(bmp, (50,10))
#    Himage2_Other.paste(bmp, (50,300))
#    epd.display(epd.getbuffer(Himage2), epd.getbuffer(Himage2_Other))
#    time.sleep(2)

#    logging.info("Clear...")
#    epd.init()
#    epd.Clear()

#    logging.info("Goto Sleep...")
#    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
#    epd7in5b_V2.epdconfig.module_exit()
    exit()




#    def display(self, imageblack, imagered):
#        self.send_command(0x10)
#        # The black bytes need to be inverted back from what getbuffer did
#        for i in range(len(imageblack)):
#            imageblack[i] ^= 0xFF
#        self.send_data2(imageblack)
#        
#        self.send_command(0x13)
#        self.send_data2(imagered)
#
#        self.send_command(0x12)
#        epdconfig.delay_ms(100)
#        self.ReadBusy()
