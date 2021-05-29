import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logfile = "./log.txt"
formatter = logging.Formatter(
    '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(funcName)s : %(message)s')
fh = logging.FileHandler(logfile, mode='w') # 写入文件log
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
ch = logging.StreamHandler() # 无参数，只是用于打印在屏幕
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)


if __name__ == "__main__":
    debug("xxxxxxxx")