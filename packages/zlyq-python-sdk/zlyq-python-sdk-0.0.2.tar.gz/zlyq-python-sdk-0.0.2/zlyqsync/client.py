from dataclasses import dataclass, asdict

import requests
import sys
import json
import os, sys

sys.path.append("..")
from zlyqauth import sign as signAuth, appToken as appTokenAuth

@dataclass
class SyncClient():
    appKey:str
    appSecret:str
    appId:int
    address:int

    def __buildHeader(self, params):
        header = {}
        sign, urlParam = signAuth.addSign(params, self.appId, self.appSecret)
        appToken = appTokenAuth.addAppToken(self.appKey, self.appSecret)
        header['Content-Type']: 'application/json'
        header['X-Sign'] = sign
        header['X-App-Token'] = appToken

        return header, urlParam

    def __httpPost(self, address, apiUrl, params, body):
        params = params if params else {}
        header, urlParams = self.__buildHeader(params)
        urlStr = address + apiUrl + "?" + urlParams

        datas = json.dumps(body)
        resp = requests.post(urlStr, data=datas, headers=header)

        return resp.text

    def userInfoSynchronize(self, userInfo):
        body = asdict(userInfo)
        return self.__httpPost(self.address, "/api/v1/synchronize/userInfo", None, body)

    def historySynchronize(self, trackInfo):
        body = asdict(trackInfo)
        return self.__httpPost(self.address, "/trace", None, body)
