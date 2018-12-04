#  -*- encoding：utf-8 -*-

"""主要作用在金山每日一言获取图片及相关文本做简单处理后发送给微信指定好友"""

import requests
import json
import os
from wxpy import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def jinshan_picture():
    
    url = 'http://open.iciba.com/dsapi'
    api = requests.get(url)
    api = json.loads(api.text)
    picture_url = api['fenxiang_img']
    mp3url = api['tts']
    text = api['note']
    mp3data = requests.get(mp3url)
    picture_data = requests.get(picture_url)
    with open('./data/yinping.mp3', 'wb') as f:
        f.write(mp3data.content)
    with open('./data/image.jpg', 'wb') as f:
        f.write(picture_data.content)

    background = Image.open('./data/image.jpg')
    prospect = Image.open('./static/imagebj.png')
    background.paste(prospect, (0, 757))      # 设置前景图覆盖的位置
    background.save('./data/fasong.jpg')
    background.close()
    os.remove('./data/image.jpg')

    # 开始图片处理----添加文字处理
    font = ImageFont.truetype("./STXINGKA.TTF", 26)    # 设置所使用的字体
    image_file = "./data/fasong.jpg"
    im1 = Image.open(image_file)
    draw = ImageDraw.Draw(im1)  # 画图

    if len(text) <= 18:
        draw.text((100,  800),  text, '#050505', font=font)   # 设置文字位置/内容/颜色/字体
    elif 18 < len(text) <= 36:
        draw.text((100,  800),  text[0:18], '#050505', font=font)
        draw.text((150+(440-len(text[18:])*25), 850), text[18:], '#050505', font=font)
    else:
        draw.text((100,  800),  '我爱你，你的等待并非一文不值！', '#050505', font=font)
    im1.save("./data/fenxiang.jpg")
    os.remove('./data/fasong.jpg')


def wx():
    bot = Bot()
    my_friend = bot.friends().search('the  moon')[0]
    my_friend.send_image('fenxiang.jpg')        # 发送图片
    my_friend.send_file('yinping.mp3')      # 发送文件

    #  发送文本
    #  my_friend.send('Hello,  WeChat!')
    #  发送视频
    #  my_friend.send_video('my_video.mov')
    #  以动态的方式发送图片
    #  my_friend.send('@img@my_picture.png')


if __name__ == '__main__':
    jinshan_picture()
    # wx()