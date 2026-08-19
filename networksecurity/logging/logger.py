# 导入 Python 自带的 logging 模块，用来记录程序运行日志。
# 例子：logging.info("数据读取成功") 可以把这句话写进日志文件。
import logging

# 导入 os 模块，用来处理文件夹路径、获取当前工作目录等。
# 例子：os.getcwd() 会返回你现在终端所在的项目路径。
import os

# 从 datetime 模块里导入 datetime 类，用来获取当前时间。
# 例子：datetime.now() 可以得到当前日期和时间。
from datetime import datetime

# 生成一个日志文件名，文件名里带当前时间，避免每次运行都覆盖同一个日志文件。
# 例子：如果现在是 2026 年 8 月 19 日 14 点 35 分 08 秒，
# LOG_FILE 的值可能是 "08_19_2026_14_35_08.log"。
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# 拼出 logs 文件夹的路径。
# os.getcwd() 表示当前项目目录，比如 "/Users/bihao/Desktop/project/Network Security"。
# os.path.join(...) 会安全地拼接路径，所以 logs_path 可能是：
# "/Users/bihao/Desktop/project/Network Security/logs"
logs_path = os.path.join(os.getcwd(), "logs")

# 如果 logs 文件夹不存在，就自动创建它。
# exist_ok=True 表示：如果 logs 文件夹已经存在，也不要报错。
os.makedirs(logs_path, exist_ok=True)

# 拼出最终日志文件的完整路径。
# 例子："/Users/bihao/Desktop/project/Network Security/logs/08_19_2026_14_35_08.log"
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    # 指定日志要写入哪个文件。
    # 例子：程序里的 logging.info("开始训练模型") 会写进 LOG_FILE_PATH 对应的 .log 文件。
    filename=LOG_FILE_PATH,

    # 指定每条日志的显示格式。
    # asctime：日志发生时间。
    # lineno：是哪一行代码打印的日志。
    # name：logger 的名字，默认通常是 root。
    # levelname：日志级别，比如 INFO、WARNING、ERROR。
    # message：你自己写的日志内容。
    # 例子：[ 2026-08-19 14:35:08,123 ] 20 root - INFO - 开始读取数据
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",

    # 设置日志级别为 INFO。
    # 意思是：INFO、WARNING、ERROR、CRITICAL 这些级别的日志都会被记录。
    # DEBUG 级别更低，所以不会被记录。
    level=logging.INFO,
)
