# -*- coding:UTF-8 -*-

import requests
import json
import re
import csv
class ParseId(object):
    # 设置请求头
    def __init__(self):
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
            "Cookie":"__mta=20871943.1625705574088.1625810520459.1625813097008.16; _lxsdk_cuid=17a839a3528c8-070f1da58fbd21-6373264-144000-17a839a3529c8; ci=1; rvct=1; mtcdn=K; uuid=5226c694e07949bdb828.1625725143.1.0.0; mt_c_token=xR1aknv_B8Yiio_ZWzUmVSFo2koAAAAACw4AAIkyH5SSt867G_XkxBIcCNINlemXinZVHTQDkWGAFQukS3HrBbqc_BktISzd7MhPvw; lsu=; iuuid=C72B4FEF3403F5A0924DEFB4DF9C9FFEC17E5FC35B2B4D6CF55632ABF4817904; isid=xR1aknv_B8Yiio_ZWzUmVSFo2koAAAAACw4AAIkyH5SSt867G_XkxBIcCNINlemXinZVHTQDkWGAFQukS3HrBbqc_BktISzd7MhPvw; logintype=normal; cityname=%E5%8C%97%E4%BA%AC; _lxsdk=C72B4FEF3403F5A0924DEFB4DF9C9FFEC17E5FC35B2B4D6CF55632ABF4817904; webp=1; i_extend=H__a100002__b1; latlng=39.830516,116.290895,1625725257685; __utma=74597006.798321478.1625725258.1625725258.1625725258.1; __utmz=74597006.1625725258.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; lt=fYaN6SmjIjuKuNSbDGgqCDbdjQgAAAAACw4AABKyZyfS3ZbSub8odXTK9CKxaHAOvtIkpz464sfHyJcIfPPYbpw2Vh_Rnd3Mr5B24A; u=583093909; n=%E9%A5%95%E9%A4%AEzzzzz; token2=fYaN6SmjIjuKuNSbDGgqCDbdjQgAAAAACw4AABKyZyfS3ZbSub8odXTK9CKxaHAOvtIkpz464sfHyJcIfPPYbpw2Vh_Rnd3Mr5B24A; unc=%E9%A5%95%E9%A4%AEzzzzz; __mta=20871943.1625705574088.1625810319319.1625810340857.13; firstTime=1625813095796; _lxsdk_s=17a89d8b4fc-08e-6c7-641%7C%7C48"
        }
        self.urls = self.getUrl()
        self.headers = headers
    # 获取这些网页
    def getUrl(self):
        urls = []
        for i in range(1,60):
            urls.append(('https://yt.meituan.com/meishi/c17/pn'+'%s'+"/")%(i))
            print(urls)
        return urls    
    def getId(self):
        id_list = []
        k = 1
        for v in self.urls:
            html = requests.get(v, headers = self.headers)
            # 进行正则匹配，寻求店铺id信息
            re_info = re.compile(r'\"poiId\":(\d{4,})')
            id = re_info.findall(html.text)# 获得的是列表  
            print(id)          
            # 想利用writerows将列表添加到csv文件中
            for v in id:
                id_list.append((k, v))
                k+=1
        # 将店铺ID保存到CSV文件中
        with open('../Related_Files/poId.csv', 'wb') as f:
            writer = csv.writer(f)          
            writer.writerows(id_list) 
            print(id_list)       
        temp_id = []
        for il in id_list:
            temp_id.append(il[1])
        return temp_id

############ 测试 ################
a = ParseId()
print(a.getId())