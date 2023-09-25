import pyproj
import numpy as np
from scipy.spatial.transform import Rotation as R

gt_output_name = "./UrbanNav.txt"
output_gt = open(gt_output_name,'w')

def dms_to_decimal(degrees, minutes, seconds, direction):
    # 将度、分、秒转换为十进制度数
    decimal_degrees = float(degrees) + float(minutes)/60 + float(seconds)/3600
    
    # 如果方向是南半球（S），则将结果变为负数
    if direction in ['S', 's']:
        decimal_degrees = -decimal_degrees

    if direction in ['W', 'w']:
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees

# 示例：将48°30'15" N转换为十进制度数
# latitude_dms = "48 30 15 N"
# dms_parts = latitude_dms.split()
# degrees = dms_parts[0]
# minutes = dms_parts[1]
# seconds = dms_parts[2]
# direction = dms_parts[3]

# decimal_latitude = dms_to_decimal(degrees, minutes, seconds, direction)

# 创建一个Proj对象，定义输入和输出坐标系
# 这里使用WGS 84坐标系（经纬度坐标）和UTM坐标系（例如，UTM Zone 33N）
in_proj = pyproj.Proj(init='epsg:4326')  # WGS 84
out_proj = pyproj.Proj(init='epsg:32650')  # UTM Zone 33N

# 输入经纬度坐标
longitude = 11.0  # 经度
latitude = 48.0  # 纬度

# 使用Proj库进行坐标转换
x, y = pyproj.transform(in_proj, out_proj, longitude, latitude)

# 输出转换后的UTM坐标
print(f'经度：{longitude}，纬度：{latitude} 转换为 UTM x:{x},y:{y}')

# 打开文件以读取
cnt = 0
ori_x = 0.0
ori_y = 0.0
ori_z = 0.0
ori_roll = 0.0
ori_pitch = 0.0
ori_yaw = 0.0
with open('./UrbanNav_TST_GT_raw.txt', 'r') as file:
    for line in file:
        # 处理每一行
        if(cnt > 2):
            str_list = line.split()
            float_list = [float(x) for x in str_list]
            time_stamp = float_list[0]
            degrees = float_list[3]
            minutes = float_list[4]
            seconds = float_list[5]
            direction = 'N'
            decimal_latitude = dms_to_decimal(degrees, minutes, seconds, direction)
            degrees = float_list[6]
            minutes = float_list[7]
            seconds = float_list[8]
            direction = 'E'
            decimal_longitude = dms_to_decimal(degrees, minutes, seconds, direction)
            x, y = pyproj.transform(in_proj, out_proj, decimal_longitude, decimal_latitude)
            z = float_list[9]
            # 欧拉角表示（单位：度）
            roll = float_list[16]  # Roll角度
            pitch = float_list[17]  # Pitch角度
            yaw = float_list[18]  # Yaw角度
            # if(cnt == 3):
            #     ori_x = x
            #     ori_x = y
            #     ori_z = z
            #     ori_roll = roll
            #     ori_pitch = pitch
            #     ori_yaw = yaw
            #     roll = 0
            #     pitch = 0
            #     yaw = 0
            #     x = 0
            #     y = 0
            #     z = 0
            # else:
            #     x = x - ori_x
            #     y = y - ori_y
            #     z = z - ori_z
            #     roll = roll - ori_roll
            #     pitch = pitch - ori_pitch
            #     yaw = yaw - ori_yaw

            # 将欧拉角转换为弧度
            roll_rad = np.deg2rad(roll)
            pitch_rad = np.deg2rad(pitch)
            yaw_rad = np.deg2rad(yaw)

            # 创建Rotation对象
            r = R.from_euler('zyx', [yaw_rad, pitch_rad, roll_rad], degrees=False)

            # 获取四元数表示
            quaternion = r.as_quat()
            str = "%.9f %.9f %.9f %.9f %.9f %.9f %.9f %.9f\n" % (time_stamp, x, y, z, quaternion[0],  quaternion[1],  quaternion[2],  quaternion[3])
            output_gt.write(str)
            print(str)

        cnt = cnt + 1
        print(line.strip())  # 这里示例是打印，您可以根据需要执行其他操作


# output_handle.close()