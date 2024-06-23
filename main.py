import os
import random
import re
import shutil
import tkinter as tk
from tkinter import *
from tkinter import filedialog

from PIL import ImageFont, ImageDraw, Image

import test


def save_image():
    filepath = filedialog.asksaveasfilename(defaultextension='.jpg', filetypes=[("JPEG files", "*.jpg")])
    if filepath:
        try:
            img = Image.open('combined_image.jpg')  # 打开之前生成的图片
            img.save(filepath)  # 保存到用户指定的位置
            print(f"Image saved to: {filepath}")
        except Exception as e:
            print(f"Error saving image: {e}")

        # 窗口主函数


def create_window():
    root = tk.Tk()
    root.title("Input Window")

    # 创建变量来保存输入框的内容
    month_var = tk.StringVar()
    num_suiji_var = tk.StringVar()
    pace_min_var = tk.StringVar()
    pace_max_var = tk.StringVar()
    distance_min_var = tk.StringVar()
    distance_max_var = tk.StringVar()

    # 创建输入框
    entries = [
        (tk.Entry(root, textvariable=month_var), "月份，输入整数"),
        (tk.Entry(root, textvariable=num_suiji_var), "次数，输入整数,2月次数不超28,其余月份次数不超过30或31"),
        (tk.Entry(root, textvariable=pace_min_var), "配速最小值，输入整数（分钟/公里）"),
        (tk.Entry(root, textvariable=pace_max_var), "配速最大值，输入整数（分钟/公里）"),
        (tk.Entry(root, textvariable=distance_min_var), "路程最小值，输入整数（公里）"),
        (tk.Entry(root, textvariable=distance_max_var), "路程最大值，输入整数（公里）")
    ]

    # 布局输入框
    for i, (entry, label) in enumerate(entries):
        entry.grid(row=i, column=0)
        tk.Label(root, text=label).grid(row=i, column=1)

        # 创建处理按钮
    tk.Button(root, text="Process", command=lambda: main(
        month_var.get(), num_suiji_var.get(), pace_min_var.get(), pace_max_var.get(), distance_min_var.get(),
        distance_max_var.get()
    )).grid(row=6, column=0, columnspan=2)

    # 创建另存为按钮
    tk.Button(root, text="Save Image", command=save_image).grid(row=7, column=0, columnspan=2)

    root.mainloop()


def main(month, num_suiji, pace_min, pace_max, distance_min, distance_max):
    os.makedirs('3月')
    # 生成1到28之间的15个不重复的随机数
    if month == "2":
        random_numbers = random.sample(range(1, 29), int(num_suiji))
    elif month == "1" or "3" or "5" or "7" or "8" or "10" or "12":
        random_numbers = random.sample(range(1, 32), int(num_suiji))
    else:
        random_numbers = random.sample(range(1, 30), int(num_suiji))

    # 对生成的随机数进行排序
    sorted_numbers = sorted(random_numbers)

    for i in sorted_numbers:
        pace, distance, time = test.generate_run_stats(int(pace_min), int(pace_max), float(distance_min),
                                                       float(distance_max))
        pace_get = pace
        distance_get = str(distance)[:4]
        time1 = test.convert_pace_to_time_format(time)
        time_get = time1
        random_time = test.generate_random_time_between_22_and_23()

        img = Image.open('back.jpg')
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('msyh.ttc', size=34)
        text = "{}月{}日".format(month, i)
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
    shutil.copyfile('100.jpg', '3月/100.jpg')
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
    message = '图片创建成功，请点击Save Image获取'
    tk.messagebox.showinfo(title='提示', message=message)


# 运行窗口主函数
create_window()
