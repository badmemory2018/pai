from selenium import webdriver
import time,sys
from detect import detVoteNumExist, detReadyInfo, detFreshInfo,subReq,confirm,getRes1,getRes2
from log import logger
from config import read
from iddect import calHash
if __name__ == "__main__":
    #读取配置文件
    print("*" * 50)
    print("入口1：正式网站")
    print("入口2：测试网站")
    print("*" * 50)
    choice = input("输入软口:")
    if choice == "1":
        gourl = "https://paimai2.alltobid.com/login?type=individual"
    else :
        gourl = "https://testh5.alltobid.com/login?type=individual"
    print("*"*50)
    print("策略1：倒数13秒加价900")
    print("策略2：倒数15秒加价1000")
    print("策略3：倒数11秒加价800")
    print("*" * 50)
    policy = input("输入策略号:")
    if policy == "1":
        INTERVAL, pricediff = read("POLICY1")
    elif policy == "2":
        INTERVAL, pricediff = read("POLICY2")
    elif policy == "3":
        INTERVAL, pricediff = read("POLICY3")
    else:
        logger.error("选择策略有误，退出")

    # 在倒数INTERVAL秒提交当前价+pricediff, 在倒数subTime秒强行提交

    curValue = 0
    subTime = 3 #还剩余X秒强制提交价格

    profile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox()


    driver.get(gourl)
    # 1.投标号是否存在
    time.sleep(5)
    flaglist=list()
    flag = False
    while flag == False:
        try:
            time.sleep(3)
            flag = detVoteNumExist(driver,flaglist)
        except:
            logger.warning("未检测到投标号，请登陆")
            continue
    # 2.检测其他信息是否存在,投房额度，投标人数，curTime,
    flag = False
    while flag == False:
        try:
            time.sleep(1)
            flag = detReadyInfo(driver,flag)
        except:
            logger.warning("已登陆，拍牌尚未开始")
            continue
    flag = False
    while flag == False:
    # 3.循环查看信息,检测时间
        try:
            time.sleep(1)
            flag = detFreshInfo(driver,flag, INTERVAL)
        except Exception as e:
            logger.error("刷新信息出错")
            logger.error(e)
    # 4.时间触发,输入价格，提交
    curValue = int(flag) + pricediff
    while True:
        try:
            logger.info("即将出价:"+str(curValue))
            subReq(driver,curValue)
            break
        except Exception as e:
            logger.warning("未到最后出价阶段")
            logger.warning(e)
            continue
    ifCon = False
    while ifCon == False:
        try:
            # 点击确认框
            logger.info("尝试点击确认进行提交")
            ifCon = confirm(driver, subTime, curValue)



        except Exception as e:
            logger.error("出价确认出错")
            logger.error(e)
