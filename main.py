import test
from PIL import ImageFont, ImageDraw, Image
import random
import os
import re
import shutil
os.makedirs('3月')
print('please input you need month')
month = input(str())
# 生成1到28之间的15个不重复的随机数
random_numbers = random.sample(range(1, 29), 15)

# 对生成的随机数进行排序
sorted_numbers = sorted(random_numbers)

for i in sorted_numbers:
    pace, distance, time = test.generate_run_stats()
    pace_get = '0' + str(pace)[0] + "'" + str(pace)[2:4] + '"'
    distance_get = str(distance)[:4]
    time1 = test.convert_pace_to_time_format(time)
    time_get = "00:0" + time1
    random_time = test.generate_random_time_between_22_and_23()

    img = Image.open('back.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('msyh.ttc', size=34)
    text = "{}月{}日".format(month,i)
    draw.rectangle((46, 50, 178, 83), fill='white')
    draw.text((46, 50), text, font=font, fill=(105, 105, 105))

    text2 = "户外跑步{} 公里".format(distance_get)
    font2 = ImageFont.truetype('msyh.ttc', size=40)
    draw.rectangle((169, 172, 512, 210), fill='white')
    draw.text((169, 172), text2, font=font2, fill=(35, 35, 35))

    text3 = "用时 {}  配速 {}".format(time_get, pace_get)
    font = ImageFont.truetype('msyh.ttc', size=34)
    draw.rectangle((170, 247, 589, 275), fill='white')
    draw.text((170, 242), text3, font=font, fill=(74, 74, 74))

    text4 = random_time
    font = ImageFont.truetype('msyh.ttc', size=36)
    draw.rectangle((938, 209, 1030, 238), fill='white')
    draw.text((938, 209), text4, font=font, fill=(152, 152, 152))
    img.save('./3月/{}.jpg'.format(i))

# 设置图片所在的文件夹路径
image_dir = '3月'  # 替换为你的图片文件夹路径
shutil.copyfile('100.jpg','3月/100.jpg')
# 获取文件夹中所有的图片文件名
image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]


# 使用正则表达式提取文件名中的数字，并根据数字对文件名进行排序
image_files.sort(key=lambda x: int(re.search(r'\d+', x).group()), reverse=True)

# 初始化一个空白图像，宽度为最宽图片的宽度，高度为所有图片高度之和
widths, heights = zip(*(Image.open(os.path.join(image_dir, f)).size for f in image_files))
max_width = max(widths)
total_height = sum(heights)

# 创建一个新的空白图像，用于拼接所有图片
new_img = Image.new('RGB', (max_width, total_height))

# 初始化y坐标（从上到下拼接）
y_offset = 0

# 遍历排序后的图片文件，将它们拼接到新图像上
for img_file in image_files:
    img_path = os.path.join(image_dir, img_file)
    with Image.open(img_path) as img:
        # 将图片粘贴到新图像的指定位置
        new_img.paste(img, (0, y_offset))
        # 更新y坐标，以便下一张图片可以紧接着上一张图片粘贴
        y_offset += img.height

    # 保存拼接后的图像
new_img.save('combined_image.jpg')
shutil.rmtree('3月')