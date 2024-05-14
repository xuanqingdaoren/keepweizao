from PIL import ImageFont, ImageDraw, Image
import random


def generate_run_stats():
    # 设置配速和路程的区间
    pace_min, pace_max = 5, 7  # 配速区间（分钟/公里）
    distance_min, distance_max = 0.8, 1.2  # 路程区间（公里）

    # 随机生成配速和路程
    random_pace = random.uniform(pace_min, pace_max)
    random_distance = random.uniform(distance_min, distance_max)

    # 计算所需时间（配速乘以路程）
    time_needed = random_pace * random_distance

    # 返回配速、路程和所需时间
    return random_pace, random_distance, time_needed


# 调用函数并输出结果
def convert_pace_to_time_format(pace_in_minutes_per_km):
    # 分离整数部分和小数部分
    minutes = int(pace_in_minutes_per_km)
    seconds = round((pace_in_minutes_per_km - minutes) * 60)

    # 使用字符串格式化来确保秒数是两位数
    seconds_str = f"{seconds:02d}"

    # 拼接成时间格式
    time_str = f"{minutes}:{seconds_str}"

    return time_str

def generate_random_time_between_22_and_23():
    # 生成0到59之间的随机分钟数
    random_minutes = random.randint(0, 59)

    # 格式化时间为24小时制字符串
    random_time = f"22:{random_minutes:02d}"

    return random_time

# 生成并打印随机时间
