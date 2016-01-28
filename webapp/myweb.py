#-*- coding:utf-8 -*-
import web
import csv
import json
import logging
import os
# 配置日志信息
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='myapp.log',
                    filemode='w')
                    
# 定义一个Handler打印INFO及以上级别的日志到sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# 设置日志打印格式
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
# 将定义好的console日志handler添加到root logger
logging.getLogger('').addHandler(console)

g_log = logging.getLogger("common")
g_logE = logging.getLogger("exception")
g_logD = logging.getLogger("detail")
# logger1.debug('debug')
# logger1.info('info')
# logger2.warning('warning')
# logger2.error('error')

urls = ('/dyncfg', 'dyncfg',
        '/check_update', 'check_update',
        '/download', 'download',
       )
       

E_CHANNEL_MINE      = 1
E_CHANNEL_IOS       = 2
E_CHANNEL_AliPay    = 16
E_CHANNEL_LENOVO    = 8
E_CHANNEL_XIAOMI    = 10
E_CHANNEL_HUAWEI    = 12
E_CHANNEL_WDJ       = 13
E_CHANNEL_QIHU360   = 22
E_CHANNEL_KUPAI     = 23

CUR_RELEASE_IOS_VERSION = '1.2.9'
CUR_VERIFY_IOS_VERSION = '1.3.0'

#通用错误
E_NOLOGINNED = -101
ES_NOLOGINNED = "no loginned"
E_EXCEPTION = -102
ES_EXCEPTION = "internal exception"
E_BADURL = -103
ES_BADURL = "bad url"
E_DATANOTFOUND = -104
ES_DATANOTFOUND = "data not found"
E_INVALIDCHAR = -105
ES_INVALIDCHAR = "invalid char"
E_NOTSUPPORT = 106
ES_NOTSUPPORT = "not support"

#返回错误字符串JSON格式
def ErrResult(nErr, strMsg):
    print("error code:"+str(nErr)+",msg:"+strMsg)
    return json.dumps({"code":nErr,"reason":strMsg}, ensure_ascii=False)
#正确的
def OKResult():
    return json.dumps({"code":0}, ensure_ascii=False)

class dyncfg(object):
  def GET(self):
    try:
        d = web.data()
        print(d)
        data = web.input(channelId="",ver="")
        print(dict(data))
        strChannelId = data.channelId
        strVersion = data.ver
        print("Channel:" + strChannelId)
        print("Version:" + strVersion)
        
        csvfile = file('dyncfg.csv', 'rb')
        reader = csv.reader(csvfile)
        
        strJson = ""
        for row in reader:
            parameterStr = ','.join(row)
            parameters  = parameterStr.split(',')
            channelName = parameters[0]
            channelId   = parameters[1]
            if "#" in channelName or "ChannelId" in channelId:
                continue
            version     = parameters[2]
            noticeUrl   = parameters[3]
            updateVersionUrl = parameters[4]
            updateUrl   = parameters[5]
            svrId       = parameters[6]
            isThirdLogin = parameters[7]
            if strChannelId == channelId and cmp(strVersion,version) <= 0:
                f = file("dyncfg.json")
                s = json.load(f)
                f.close
                loginSeedUrl = s["hostinfo"]["loginseedhost"]
                loginGameUrl = s["hostinfo"]["logingamehost"]
                registerUrl = s["hostinfo"]["registerhost"]
                serverstate = s["serverstate"]
                strJson = json.dumps({"code":0,
                                      "NoticeUrl":noticeUrl,
                                      "UpdateVersionUrl":updateVersionUrl,
                                      "UpdateUrl":updateUrl,
                                      "SvrId":svrId,
                                      "IsThirdLogin":isThirdLogin,
                                      "LoginSeedUrl":loginSeedUrl,
                                      "LoginGameUrl":loginGameUrl,
                                      "RegisterUrl":registerUrl,
                                      "ServerState":serverstate})
                print(strJson)
                break
            # else:
            #     strJson = json.dumps({"code":-1})
        csvfile.close() 
        if strJson == "":
          logging.info('not found dyncfg info')
          # g_log.debug('not found dyncfg info')
          strJson = json.dumps({"code":-1})
        else:
          logging.info('get dyncfg success!')
          # g_log.debug('get dyncfg success!')
        return strJson
    except Exception, e:
      logging.info(e)
      return ErrResult(E_EXCEPTION, ES_EXCEPTION)

class check_update(object):
  def GET(self):
    try:
      data = web.input(app_version="",script_version="",channel="")
      print(dict(data))
      strAppVersion = data.app_version
      strScriptVersion = data.script_version
      strChannel = data.channel

      strJson = json.dumps({"IsNeedUpdate":1,
                            "IsAllUpdate":1,
                            "FileListUrl":"http://www.baidu.com",
                            "AppVersion":2,
                            "ScriptVersion":'1.0.1'})
      return strJson
    except Exception, e:
      logging.info(e)
      return ErrResult(E_EXCEPTION, ES_EXCEPTION)


# 下载文件
BUF_SIZE = 262144
class download(object):
  def GET(self):
    data = web.input(filename="")
    print(dict(data))
    file_name = data.filename
    file_path = os.path.join('./',file_name)
    print("Path:" + file_path)
    f = None

    try:
      f = open(file_path,"rb")
      web.header('Content-Type','application/octet-stream')
      web.header('Content-disposition', 'attachment; filename=%s' % file_name)
      while True:
        c = f.read(BUF_SIZE)
        if c:
          yield c
        else:
          break
    except Exception, e:
      print e
      yield 'Error'
    finally:
      if f:
        f.close()


if __name__ == "__main__":
  app = web.application(urls, globals())
  app.run()