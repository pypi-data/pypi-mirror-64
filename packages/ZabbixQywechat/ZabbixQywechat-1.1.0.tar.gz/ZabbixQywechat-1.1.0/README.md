This is a package for sending messages to enterprise WeChat applications in zabbix. You can use [Github](https://github.com/mikecui426/ZabbixQywechat)

### View at:

<code>
https://pypi.org/project/ZabbixQywechat/1.1.0/
</code>


### pip install ZabbixQywechat


### Demo test

vim test.py

<pre><code>
from ZabbixQywechat import Qywechat

import sys

Agentid="1000002"
Corpid="1111"
Corpsecret="2222"
PATH="/tmp/test.json"

if __name__ == '__main__':
    Touser=sys.argv[1]
    Subject=str(sys.argv[2])
    Content=str(sys.argv[3])
    Result=Qywechat(Agentid,Corpid,Corpsecret,PATH)
    Result.SendMSGtoWechat(Touser,Subject,Content)
</code></pre>

python test.py WechatAccount title content
