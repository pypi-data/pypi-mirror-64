import sys
import json
import enum
import datetime
import logging
import urllib
from . import httphelper
from . import runtime

class OAuthToken:
    def __init__(self, initData):
        self.token_type = None
        self.scope = None
        self.expires_in = None
        self.access_token = None
        if isinstance(initData, dict):
            for key in initData:
                setattr(self, key, initData[key])

def getMicrosoftGraphOAuthToken() -> OAuthToken:
    resultDict = runtime.OperationMethodUtility.invoke(runtime.OperationMethods.getMicrosoftGraphOAuthToken)
    ret = OAuthToken(resultDict)
    return ret

def getImplicitGrantFlowOAuthToken(authEndpoint: str, clientId: str, scope: str) -> OAuthToken:
    resultDict = runtime.OperationMethodUtility.invoke(runtime.OperationMethods.getImplicitGrantFlowOAuthToken, { "authEndpoint": authEndpoint, "clientId": clientId, "scope": scope} )
    ret = OAuthToken(resultDict)
    return ret

def getAuthorizationCode(authEndpoint: str, clientId: str, scope: str) -> str:
    result = runtime.OperationMethodUtility.invoke(runtime.OperationMethods.getAuthorizationCode, { "authEndpoint": authEndpoint, "clientId": clientId, "scope": scope} )
    ret = result
    return ret

def testGetMicrosoftGraphOAuthToken() -> None:
    oauthToken = getMicrosoftGraphOAuthToken()
    testGetFiles(oauthToken)

def testGetImplicitGrantFlowOAuthToken() -> None:
    oauthToken = getImplicitGrantFlowOAuthToken("https://login.microsoftonline.com/common/oauth2/v2.0/authorize", "9ee7f99d-c5b3-4f5f-810a-708848a1c566", "https://graph.microsoft.com/Files.ReadWrite")
    testGetFiles(oauthToken)

def testGetAuthorizationCode() -> None:
    code = getAuthorizationCode("https://login.microsoftonline.com/common/oauth2/v2.0/authorize", "9ee7f99d-c5b3-4f5f-810a-708848a1c566", "https://graph.microsoft.com/Files.ReadWrite")
    print(code)

def testGetFiles(oauthToken: OAuthToken) -> str:
    requestInfo = httphelper.RequestInfo()
    requestInfo.method = "GET"
    requestInfo.url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    requestInfo.headers["Content-Type"] = "application/json"
    requestInfo.headers["Accept"] = "application/json"
    requestInfo.headers["Authorization"] = "Bearer " + oauthToken.access_token
    responseInfo = httphelper.HttpUtility.invoke(requestInfo)
    print(responseInfo.body)


if __name__ == "__main__":
    request = runtime.OperationMethodUtility.buildInputChannelRequestMessage(runtime.OperationMethods.getMicrosoftGraphOAuthToken)
    response = runtime.OperationMethodUtility.buildInputChannelResponseMessage({"token_type": "Bearer", "access_token": "Foo"})
    runtime.Utility.setInputChannelMock(request, response)
    oauthToken = getMicrosoftGraphOAuthToken()
    print(oauthToken.access_token)
