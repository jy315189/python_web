from pyzbar.pyzbar import decode
from PIL import Image
from threading import Timer
from datetime import datetime
from PIL import ImageGrab
import pymysql
import datetime
import time


def generate_sqls(data):
    # 将字符串拆分成列表
    data_list = data.split(',')
    first_23 = data_list[:23]

    listName = ["硝酸配置槽液位", "硝酸萃取配料计量槽液位", "硝酸高位槽液位", "溶解反应槽液位", "气体探测器1",
                "气体探测器2", "气体探测器3", "气体探测器4", "气体探测器5", "气体探测器6", "气体探测器7",
                "气体探测器8", "气体探测器9", "1号罐体液位", "2号罐体液位", "3号罐体液位", "4号罐体液位",
                "5号罐体液位", "6号罐体液位", "7号罐体液位", "8号罐体液位", "9号罐体液位", "10号罐体液位"]

    # 生成sql1列表
    sql1_list = []
    for i in range(len(first_23)):
        sql1 = "insert into collectdata_copy1 (NAME,QUALITY,TIME,VALUE) values ('" + listName[
            i] + "','GOOD','" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "','" + first_23[i] + "')"
        sql1_list.append(sql1)

    # 生成sql2
    sql2 = "INSERT INTO `bxasafety_whp`.`whp_lrlydj` (`id`, `lydw`, `create_date`, `lrr`) VALUES ('{}', '{}', '{}', '{}')".format(
        data_list[23], data_list[24], data_list[25], data_list[26])
    sql1_list.append(sql2)

    # 生成sql3
    sql3 = "INSERT INTO `bxasafety_whp`.`whp_lrlydj_info` (`id`, `lrlydj_id`, `whp_id`, `sfsl`, `jcl`, `sync_timestamp`,`jbr`) VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}')".format(
        data_list[27], data_list[28], data_list[29], float(data_list[30]), data_list[31], data_list[32], data_list[32])
    sql1_list.append(sql3)

    # 返回简单的列表
    return sql1_list


def task():
    # 拼接文件名
    filename = f'aa.png'
    # 截屏并保存到指定位置
    im = ImageGrab.grab()
    im.save(f'F:/python/jx/{filename}')

    # 强制等待3秒
    time.sleep(3)

    # 获取二维码
    decodeQR = decode(Image.open("F:/python/jx/aa.png"))
    data = decodeQR[0].data.decode('utf-8')
    # 生成的SQL语句列表

    sql_list = generate_sqls(data)

    # 连接到数据库
    conn = pymysql.connect(host="127.0.0.1", user="zhjx", passwd="123456", db="zhdp_whp", charset='utf8mb4')

    # 创建游标对象
    cursor = conn.cursor()

    # 循环执行SQL语句
    for sql in sql_list:
        try:
            cursor.execute(sql)
        except pymysql.Error as err:
            print(err)

    # 提交事务
    conn.commit()
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()


def func():
    try:
        task()
        print('执行成功')
    except Exception as e:
        print(e)
        print('执行失败')
    finally:
        print('执行完毕')
    t = Timer(5, func)
    t.start()


func()
