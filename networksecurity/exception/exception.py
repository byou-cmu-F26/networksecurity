# 导入 Python 自带的 sys 模块。
# 这里主要用 sys.exc_info()，它可以拿到当前异常的详细信息。
# 例子：try 里面发生 ZeroDivisionError 后，sys.exc_info() 能拿到错误类型、错误对象、错误位置。
import sys


# 从 networksecurity.logging 包里导入 logger.py 这个模块。
# 注意：这里的 logger 不是一个类，而是 logger.py 这个“模块文件”本身。
# 因为 logger.py 里面 import 了 Python 自带的 logging 模块，
# 所以下面可以写 logger.logging.info(...) 来调用 logging.info(...)。
from networksecurity.logging import logger


# 自定义一个异常类，让项目里的报错信息更清楚。
# Exception 是 Python 所有普通异常类的父类。
# 例子：ZeroDivisionError、ValueError、FileNotFoundError 都属于 Exception 的子类。
class NetworkSecurityException(Exception):

    # __init__ 是创建异常对象时自动执行的方法。
    # error_message：真正的错误信息，比如 division by zero。
    # error_details：传进来的 sys 模块，用来调用 sys.exc_info() 获取错误发生的位置。
    # 例子：NetworkSecurityException(e, sys)，这里 e 是原始错误，sys 用来查文件名和行号。
    def __init__(self, error_message, error_details: sys):
        # 把原始错误信息保存到当前异常对象里。
        # 例子：如果错误是 1/0，那么 error_message 可能是 "division by zero"。
        self.error_message = error_message

        # exc_info() 会返回 3 个东西：
        # 第 1 个：错误类型，比如 ZeroDivisionError。
        # 第 2 个：错误对象，比如 division by zero。
        # 第 3 个：traceback 对象，里面包含错误发生的文件、行号等信息。
        # 前两个这里暂时不用，所以用 _ 忽略掉，只保留 exc_tb。
        _, _, exc_tb = error_details.exc_info()

        # 从 traceback 里取出错误发生的行号。
        # 例子：如果 a = 1 / 0 在第 44 行，那么 self.lineno 就是 44。
        self.lineno = exc_tb.tb_lineno

        # 从 traceback 里取出错误发生的 Python 文件路径。
        # 例子："/Users/bihao/Desktop/project/Network Security/networksecurity/exception/exception.py"
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    # __str__ 决定 print(异常对象) 或报错显示时，要显示什么文字。
    # 也就是说，raise NetworkSecurityException(...) 后，终端里看到的错误内容来自这里。
    def __str__(self):
        # 把文件名、行号、原始错误信息拼成一句完整的报错说明。
        # 例子：Error occurred in python script name [exception.py] line number [52] error message [division by zero]
        return "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.file_name, self.lineno, str(self.error_message)
        )


# 这句表示：只有直接运行这个文件时，下面的测试代码才会执行。
# 例子：python networksecurity/exception/exception.py 会执行下面代码。
# 如果别的文件只是 import NetworkSecurityException，下面代码不会执行。
if __name__ == "__main__":
    # try 用来包住可能会出错的代码。
    # 如果 try 里面出错，程序会跳到 except 里面处理。
    try:
        # 写一条 INFO 级别日志，表示程序进入了 try 代码块。
        # 因为 logger.py 已经配置过 basicConfig，所以这条日志会被写到 logs 文件夹里的 .log 文件。
        logger.logging.info("Enter the try block")

        # 这里故意制造一个错误：1 除以 0 在数学上不允许。
        # Python 会抛出 ZeroDivisionError: division by zero。
        a = 1 / 0

        # 因为上一行已经报错了，所以这一行不会执行。
        print("This will not be printed", a)

    # except 会接住 try 里面发生的普通异常。
    # as e 表示把原始异常对象保存到变量 e 里面。
    except Exception as e:
        # 把原始异常 e 包装成我们自己定义的 NetworkSecurityException。
        # sys 会被传进去，用来定位原始错误发生在哪个文件、哪一行。
        raise NetworkSecurityException(e, sys)