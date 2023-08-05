#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import sys
import urllib,urllib2
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
	    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=' + self.CORPID + '&corpsecret=' + self.CORPSECRET
            token_file=urllib2.urlopen(gettoken_url)
            #self.PATH=path
        #print token_file
            token_data=token_file.read().decode('utf-8')
        #print token_data    
            token_json=json.loads(token_data)
            Token_file=json.dumps(token_json)
        #print type(Token_file),type(token_json)
        #print token_json['errcode']
            if token_json['errcode'] != 0:
               return False
            else:
           	Token = token_json['access_token']
           	file = open(self.PATH, 'w')
           	file.write(Token_file)
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

       	     json_content = json.dumps(post_content)
	   
	     try:
          	file=open(self.PATH,'r')
                Token=json.load(file)['access_token']
                #print "Access_token cache is %s" % Token
                file.close()
       	     except:
		Token = self.GetTokenFromWechat()
       #Token = GetTokenFromWechat(Corpid,Corpsecret)
       #print "API Access_token is %s" % Token
       	     i=0
       	     wcurl="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+ Token
       #print json_content
	     response = urllib2.urlopen(wcurl,json_content)
	     result=response.read().decode('utf-8')
	     res1=json.loads(result)
	     res2=json.dumps(res1)
	     print (res2)
	     while res1['errcode'] != 0 and i < 1:
			time.sleep(2)
			i+=1
			Token2 = self.GetTokenFromWechat()
			if Token:
				Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token2
				response = urllib2.urlopen(Url,json_content)
				result=response.read().decode('utf-8')
				return result
	     
