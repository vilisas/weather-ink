#!/usr/bin/python3
# -*- coding:utf-8 -*-
#
# E-Ink weather display.
# Sutemos 2023
# based on WaveShare epd examples.
#
# 800 x 480 display simulator. Because e-ink display is sloooow, so we just generate png file instead and later re-enable
# e-ink part.
# Display has two 1-bit canvases - one for black color, another for red or yellow.
#
import os, sys, time, traceback, logging, json, requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

# picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
# from waveshare_epd import epd7in5b_V2


width = 800
height = 480
radar_url = "https://beta.meteo.lt/data/radar/radarlarge+36.gif"

# API info: https://api.meteo.lt
# observed data for Vilnius
weather_json_url = "https://api.meteo.lt/v1/stations/vilniaus-ams/observations/latest"
icon_path = "lib/solid-black/png/128x128/"

logging.basicConfig(level=logging.DEBUG)
# epd = epd7in5b_V2.EPD()


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
    str_time = time.strftime("%Y-%m-%d %H:%M")

    radar_src = Image.open("lib/radarlarge+36.gif")
#    response = requests.get(radar_url)
#    radar_src = Image.open(BytesIO(response.content))

    radar_img = radar_src.crop((50, 70, 530, 420))

    logging.info("epd7in5b_V2 meteo radar")

    font24 = ImageFont.truetype(r'lib/Font.ttc', 24)
    font18 = ImageFont.truetype(r'lib/Font.ttc', 18)
    font64 = ImageFont.truetype(r'lib/Font.ttc', 64)

#    width  = epd.width
#    height = epd.height
    logging.info(("EPD width=", width, " height=", height))
    logging.info("init and Clear")
#    epd.init()
#    epd.Clear()

    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...")
    black_image = Image.new('1', (width, height), 255)  # 255: clear the frame
    red_image = Image.new('1', (width, height), 255)  # 255: clear the frame

#    Other = Image.new('1', (width, height), 255)  # 255: clear the frame
    draw_black = ImageDraw.Draw(black_image)  # black image canvas
    draw_red = ImageDraw.Draw(red_image)

    radar_offset_x = 0
    radar_offset_y = 105

    # paste to specific location
    black_image.paste(radar_img, (radar_offset_x, radar_offset_y))
    draw_black.rectangle((radar_offset_x, radar_offset_y,
                         480+radar_offset_x, 350 + radar_offset_y), outline=0)

    draw_black.text((2, height-25), ("Atnaujinta " + str_time),
                    font=font24, fill=0)
    draw_black.text((1, 1), 'Orai', font=font64, fill=0)
    draw_black.text((5, 75), 'Radaras', font=font24, fill=0)
    draw_black.rectangle((0, 0, width-1, height-1), outline=0)

    black_image.save("output/output.png", format="png")

#    display_black(epd.getbuffer(black_image))
#    epd.display(epd.getbuffer(black_image),epd.getbuffer(red_image))
#    time.sleep(2)

#                black                 red
#    epd.display(epd.getbuffer(Himage),epd.getbuffer(Other))

    logging.info("Goto Sleep...")
#    epd.sleep()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
#    epd7in5b_V2.epdconfig.module_exit()
    exit()
