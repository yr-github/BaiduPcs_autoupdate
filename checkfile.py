#判断文件是否更改
#两个功能
#一个文件夹下自动上传
#另一个文件夹下上传完成后删除本地文件
import os
import logging
import hashlib
import filesql
import subprocess
import configparser
import time


config = configparser.ConfigParser()
config.read('/srv/myweb/KODExplorer/data/User/zhili/home/code/config.ini',encoding = "utf-8")
log_name = config["prconfig"]["loglocate"]
LOGGER = logging.getLogger(__name__)
fh = logging.FileHandler(encoding='utf-8', mode='a', filename=log_name)
logging.basicConfig(handlers=[fh], format='[%(asctime)s %(levelname)s]<%(process)d> %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

#判断某一个文件md5是否有变化
#返回True有变化
#返回Fals无变化
def checkMd5(file_):
    filemd5 = hashlib.md5(open(file_.encode('utf-8'),'rb').read()).hexdigest()
    sqlobj = filesql.OperateSQL("filemd5",LOGGER)
    lastmd5 =sqlobj.getFileMd5(file_,filemd5)
    if filemd5 != lastmd5:
        return True
    return False

#判断文件夹下是否有文件发生了变化，缺少文件不做处理。
#输入文件夹路径 一定要再最后加上/
#输出变化文件名list
def checkFile(filepath_):
    changelist = []
    #当前路径,路径下目录名，当前路径下文件名
    for root, dirs, files in os.walk(filepath_,'utf-8'):
        path = root.encode('utf-8', errors='surrogateescape').decode('utf-8')
        if not path.endswith('/'):
            path = path + '/'
        for file in files:
            file = file.encode('utf-8', errors='surrogateescape').decode('utf-8')
            if checkMd5(path + file):
                changefile = [path,file]
                changelist.append(changefile)
    return changelist

#改变百度用户
#适合多用户使用
def changeUser(uid_):
    try:
        cmd = "BaiduPCS-Go su" + uid_
        outbytes = subprocess.check_output(cmd, shell=True)
        cmd = "BaiduPCS-Go who"
        outbytes = subprocess.check_output(cmd, shell=True)
        outtext = outbytes.decode('utf-8')
        if uid_ in outtext:
            return True
    except:
        LOGGER.info("用户校验失败")
        return False
    return False

#上传变化后的文件名，并将变化后的md5更新数据库
#单用户使用前两行直接屏蔽即可
#文件名不能有空格
def uploadFile(changelist_,uid_,rootpath_):
    if not changeUser(uid_):
        return "用户校验失败，严重错误"
    for changefile in changelist_:
        file = changefile[0] +changefile[1]
        cmd = "BaiduPCS-Go upload \'" + file  + "\' /autoupdata/" + changefile[0].replace(rootpath_,"")
        try:
            outbytes = subprocess.check_output(cmd.encode('utf-8'),shell=True)
            outtext = outbytes.decode('utf-8')
            if "上传文件失败" not in outtext:
                sqlobj = filesql.OperateSQL("filemd5", LOGGER)
                filemd5 = hashlib.md5(open(file.encode('utf-8'),'rb').read()).hexdigest()
                sqlobj.updateMd5(file,filemd5)
            LOGGER.info(outtext)
        except subprocess.CalledProcessError as e:
            outbytes = e.output
            code = e.returncode
            LOGGER.info(code)
            LOGGER.info(outbytes)
            LOGGER.info("上传失败" + file)


def mainLoop():
    while True:
        usernum = config["prconfig"]["users"]
        for i in range(1,int(usernum)+1):
            changelist = checkFile(config["user"+str(i)]["upload_path"])
            uploadFile(changelist,config["user"+str(i)]["uid"],config["user"+str(i)]["upload_path"])
        time.sleep(int(config["prconfig"]["checktime"]))
    return

mainLoop()