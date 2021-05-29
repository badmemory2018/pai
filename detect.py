import logging
import os
import sys
import time,os
from datetime import datetime
from log import logger
from config import readID
from iddect import calHash
def detLoginInfo(votenum,driver):
    while votenum is None:
        try:
            votenum = driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[2]/ul/li[2]/span")
        except Exception:
            logger.info("用户未登陆")
            time.sleep(3)
            continue

def detReadyInfo(driver,flag):
            votenumInfo = driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[2]/ul/li[2]/span").text
            votepeople = driver.find_element_by_xpath(
                "/html/body/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[2]/span[3]/span").text
            limit = driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[1]/span[2]/span").text
            cur_time = driver.find_element_by_xpath(
                "/html/body/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[2]/span[2]/span").text
            end_time = driver.find_element_by_xpath(
                "/html/body/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[1]/span[4]/span[2]").text
            logger.info("检测到其他登陆信息")
            logger.info("进入第二阶段")
            logger.info("投标号:" + votenumInfo)
            logger.info("额度:"+ limit)
            logger.info("投标人数:" + votepeople)
            logger.info("目前时间:" + cur_time)
            logger.info("结束时间" + end_time)
            flag = True
            return flag


def detFreshInfo(driver,flag,interval):
            votenumInfo = driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[2]/ul/li[2]/span").text
            votepeople = driver.find_element_by_xpath(
                "/html/body/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[2]/span[3]/span").text
            cur_time = driver.find_element_by_xpath(
                "/html/body/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[2]/span[2]/span").text
            end_time = driver.find_element_by_xpath(
                "/html/body/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[1]/span[4]/span[2]").text
            cur_vaule = driver.find_element_by_xpath("//span[text()='目前最低可成交价:']").text.split(':')[1]
            logger.info("投标号:" + votenumInfo)
            logger.info("投标人数:" + votepeople)
            logger.info("目前时间:" + cur_time)
            logger.info("结束时间" + end_time)
            logger.info("最低成交价:"+cur_vaule)
            difflefttime = detTime(cur_time,end_time)
            lefttime = difflefttime-interval
            logger.info("离出价还有{}秒".format(lefttime))
            if difflefttime <= interval:
                flag = cur_vaule
                return flag
            else:
                flag = False
                return flag


def detTime(t1, t2):
    d1 = datetime.strptime(t1,"%H:%M:%S")
    d2 = datetime.strptime(t2, "%H:%M")
    d3 = d2-d1
    return d3.seconds

def detVoteNumExist(driver,flag):
    xpath = "/html/body/div/div/div[2]/div/div[2]/ul/li[2]/span"
    info = driver.find_element_by_xpath(xpath).text
    if info:
        logger.info("进入第一阶段")
        logger.info("已登陆,检测到投标号:"+info)
        idhash1 = readID(info)
        idhash2 = calHash(info)
        print("hash1:",idhash1)
        print("hash2:", idhash2)
        print(idhash1 == idhash2)
        if idhash1 != idhash2:
            print("账号未注册")
            print("请联系客服进行注册")
            sys.exit(1)

        else:
            flag = True
            return flag

def subReq(driver,value):
    driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div[3]/div[2]/div/input").send_keys(value)
    driver.find_element_by_xpath("/html/body/div/div/div[2]/div/div[3]/div[2]/div[2]/div/div[2]/div[3]/div[3]/div").click()

def confirm(driver, confirmTime, submitValue):
    cur_time = driver.find_element_by_xpath(
        "/html/body/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[2]/span[2]/span").text
    end_time = driver.find_element_by_xpath(
        "/html/body/div/div/div[2]/div/div[3]/div[1]/div[2]/div/div[1]/span[4]/span[2]").text
    endsecs = detTime(cur_time,end_time)
    leftSubSecs = endsecs-confirmTime
    cur_vaule = driver.find_element_by_xpath("//span[text()='目前最低可成交价:']").text.split(':')[1]
    cur_vaule = int(cur_vaule) + 300
    logger.info("当前时间："+cur_time)
    logger.info("结束时间"+end_time)
    logger.info("还有{}秒拍卖结束".format(str(endsecs)))
    logger.info("目前可提交最高成交价:"+str(cur_vaule))
    logger.info("目前提交价格为:"+str(submitValue))
    logger.info("剩余{}秒点击确定:".format(str(leftSubSecs)))

    if cur_vaule >= submitValue:
        logger.info("达到可提交价格，进行点击确认")
        btn = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[3]/div[1]").click()
        logger.info("点击完成")
        return True
    elif leftSubSecs <= 0:
        logger.info("已达到强制提交时间，进行强制提交")
        btn = driver.find_element_by_xpath(
            "/html/body/div[1]/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[3]/div[1]").click()
        logger.info("强制提交点击成功")
        return True

    return False

def getRes1(driver):
    info = driver.find_element_by_xpath("//div[@class='walertcontent']/span").text
    return info

def getRes2(driver):
    info = driver.find_element_by_xpath("//div[@class='wralertcontent']/span").text
    logger.info("获取结果成功.结果为:")
    logger.info(info)
    return info


if __name__ == "__main__":
    t1="12:35:00"
    t2="12:45"
    t3 = detTime(t1,t2)