#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
import requests
import time

class Qywechat(object):

    Touser=sys.argv[1]
    Subject=str(sys.argv[2])
    Content=str(sys.argv[3])
            
    def __init__(self,agentid,corpid,corpsecret,path):
        self.AGENTID=agentid
        self.CORPID=corpid
        self.CORPSECRET=corpsecret
        self.PATH=path
    
    def GetTokenFromWechat(self):
        content={'corpid':self.CORPID,
                     'corpsecret':self.CORPSECRET
             }
        gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        token_file=requests.post(gettoken_url,params=content)
            #self.PATH=path
        #print token_file
        token_data=json.loads(token_file.text)
        #print type(Token_file),type(token_json)
        #print token_json['errcode']
        if token_data['errcode'] != 0:
               return False
        else:
            Token = token_data['access_token']
            file = open(self.PATH, 'w')
            file.write(str(token_data))
            file.close()
            return Token
           
    def  SendMSGtoWechat(self,Touser,Subject,Content):
         post_content = {
            "touser":Touser,
            "agentid":self.AGENTID,
            "msgtype":"text",
            "text":{
                    "content":Subject + '\n\n' + Content
              },
            "safe": "0"
            }

         json_content = json.dumps(post_content,ensure_ascii=False)
       
         try:
                file=open(self.PATH,'r')
                Token=json.load(file)['access_token']
                print ("Access_token cache is %s" % Token)
                file.close()
         except:
                Token = self.GetTokenFromWechat()
         i=0
         wcurl="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + Token
         response = requests.post(wcurl,json_content)
         #result=response.read().decode('utf-8')
         res1=response.json()
         res2=json.dumps(res1)
         print (res2)
         while res1['errcode'] != 0 and i < 1:
            time.sleep(2)
            i+=1
            Token2 = self.GetTokenFromWechat()
            if Token:
                Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token2
                response = requests.post(Url,json_content)
                result=response.json()
                res3=json.dumps(result)
                return res3
         
