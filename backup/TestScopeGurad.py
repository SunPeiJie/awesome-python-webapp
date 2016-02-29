#-*- coding: UTF-8 -*-
import unittest
from ctypes import *
from ScopeGuardh import *
import timestamp_pb2
import tlcv_protocol_pb2
import scope_guard_pb2
import sys
import os
import time
import threading
import gc


# SetRequestGetVersion()
# SetRequestGetProtocolInfo()
# SetRequestGetServerStatus()
# SetRequestGetVideoSourceStatusList()
# SetRequestGetRule()
# SetRequestGetParam()
# SetRequestSetRule()
# SetRequestSetParam()
def ScopeGuradCallbackfun(id,heard,heardSize,userData):
    print "ScopeGuradCallbackfun\n"
    return 0

def protocolToTlcvData(protocol):
    vidStr = protocol.SerializeToString()
    header = protocol.DESCRIPTOR.full_name
    data = TlcvData()
    data.header = header
    data.headerSize = len(header)
    data.body = vidStr
    data.bodySize = len(vidStr)
    return data,header,vidStr

def SetRequestGetVersion():
    getVersion = tlcv_protocol_pb2.GetVersion()
    request = TlcvRequest()
    request.tlcvData = protocolToTlcvData(getVersion)[0]
    return request

def SetRequestGetProtocolInfo():
    getProtocolInfo = tlcv_protocol_pb2.GetProtocolInfo()
    request = TlcvRequest()
    request.tlcvData = protocolToTlcvData(getProtocolInfo)[0]
    return request

def SetRequestGetServerStatus():
    getServerStatus = tlcv_protocol_pb2.GetServerStatus()
    request = TlcvRequest()
    request.tlcvData = protocolToTlcvData(getServerStatus)[0]
    return request

def SetRequestGetVideoSourceStatusList():
    getVideoSourceStatusList = tlcv_protocol_pb2.GetVideoSourceStatusList()
    request = TlcvRequest()
    request.tlcvData = protocolToTlcvData(getVideoSourceStatusList)[0]
    return request

def SetRequestGetRule():
    getRule = scope_guard_pb2.GetRule()
    request = TlcvRequest()
    request.tlcvData = protocolToTlcvData(getRule)[0]
    return request

def SetRequestGetParam():
    getParam = tlcv_protocol_pb2.GetParam()
    request = TlcvRequest()
    request.tlcvData = protocolToTlcvData(getParam)[0]
    return request

def SetRequestSetParam():
    setParam = scope_guard_pb2.SetParam()
    setParam.param.sensitivity = 0
    request = TlcvRequest()
    request.tlcvData,header,body = protocolToTlcvData(setParam)
    return request,header,body

def SetRequestSetRule():
    setRule = scope_guard_pb2.SetRule()
    prule = setRule.rule
    prule.id = "123456789"
    prule.alarm_interval = 0;

    ptf = prule.poly.vertexes.add()
    ptf.point2f.x = 0.2
    ptf.point2f.y = 0.1
    ptf2 = prule.poly.vertexes.add()
    ptf2.point2f.x = 0.7
    ptf2.point2f.y = 0.1
    ptf3 = prule.poly.vertexes.add()
    ptf3.point2f.x = 0.9
    ptf3.point2f.y = 0.9
    ptf4 = prule.poly.vertexes.add()
    ptf4.point2f.x = 0.1
    ptf4.point2f.y = 0.9

    request = TlcvRequest()
    request.tlcvData,header,body = protocolToTlcvData(setRule)
    return request,header,body

def SetRequestDelRule():
    delRule = scope_guard_pb2.DelRule()
    delRule.id = "123456789"

    request = TlcvRequest()
    request.tlcvData,header,body = protocolToTlcvData(delRule)
    return request,header,body

def Getresponse():
    response = TlcvResponse()
    TlcvResponseP = POINTER(TlcvResponse)
    responseP = TlcvResponseP(response)
    return responseP

class TestScopeGuradDll(unittest.TestCase):

    def setUp(self):
        self.ScopeGuarddll = windll.LoadLibrary('E:/CVserver/dll/ScopeGuard.dll')
        self.callbackfun = TlcvDiscaredCallback(ScopeGuradCallbackfun)
        self.initFlag = 1
        self.openFlag = 1
        pass

    def tearDown(self):
        pass

    def test_Tlcv_Init(self):
        param = TlcvServerParam()

        param.workPath = "E:\\CVserver\\dll"
        param.paramPath = "E:\\CVserver\\dll\\Config.json"
        #param.workPath = "E:\\IntrusionDetection_Dll\\IntrusionDetection_Dll"
        #param.paramPath = "E:\\IntrusionDetection_Dll\\IntrusionDetection_Dll\\Config.json"
        param.discaredCb = self.callbackfun
        Flag = self.ScopeGuarddll.TLCV_Init(byref(param),0)
        self.assertEqual(Flag,0)
        if Flag == 0:
            self.initFlag = 1
        pass

    def test_Tlcv_Free(self):
        Flag = self.ScopeGuarddll.TLCV_Free()
        self.assertEqual(Flag,0)
        if Flag == 0:
            self.initFlag = 0
        pass

    def test_Tlcv_OpenVideo(self):
        vs = tlcv_protocol_pb2.VideoSource()
        vs.rtsp_device.rtspUrl = "rtsp://admin:Tolendata@192.168.10.181:554/Streaming/Channels/1?transportmode=unicast&profile=Profile_1"
        vid = protocolToTlcvData(vs)[0]
        Flag = self.ScopeGuarddll.TLCV_OpenVideoSource(byref(vid),0)
        self.assertEqual(Flag,0)
        if Flag == 0:
            self.openFlag = 1
        pass

    def test_Tlcv_CloseVideo(self):
        vs = tlcv_protocol_pb2.VideoSource()
        vs.rtsp_device.rtspUrl = "rtsp://admin:Tolendata@192.168.10.181:554/Streaming/Channels/1?transportmode=unicast&profile=Profile_1"
        vid = protocolToTlcvData(vs)[0]
        Flag = self.ScopeGuarddll.TLCV_CloseVideoSource(byref(vid))
        self.assertEqual(Flag,0)
        if Flag == 0:
            self.openFlag = 0
        pass

    def test_Tlcv_DestoryData(self):
        pass

    def test_Tlcv_UpdateFrame(self):
        pass

    def test_Tlcv_AsyncRequestSetRule(self):
        self.assertEqual(self.ScopeGuarddll.TLCV_AsyncRequest(byref(SetRequestSetRule()[0]),0),0)
        pass
    def test_Tlcv_AsyncRequestDelRule(self):
        self.assertEqual(self.ScopeGuarddll.TLCV_AsyncRequest(byref(SetRequestDelRule()[0]),0),0)
        pass
    def test_Tlcv_AsyncRequestGetRule(self):
        self.assertEqual(self.ScopeGuarddll.TLCV_AsyncRequest(byref(SetRequestGetRule()),0),0)
        pass
    def test_Tlcv_AsyncRequestGetVersion(self):
        self.assertEqual(self.ScopeGuarddll.TLCV_AsyncRequest(byref(SetRequestGetVersion()),0),0)
        pass
    def test_Tlcv_AsyncRequestGetProtocolInfo(self):
        self.assertEqual(self.ScopeGuarddll.TLCV_AsyncRequest(byref(SetRequestGetProtocolInfo()),0),0)
        pass
    def test_Tlcv_AsyncRequestGetServerStatus(self):
        self.assertEqual(self.ScopeGuarddll.TLCV_AsyncRequest(byref(SetRequestGetServerStatus()),0),0)
        pass
    def test_Tlcv_AsyncRequestGetVideoSourceStatusList(self):
        self.assertEqual(self.ScopeGuarddll.TLCV_AsyncRequest(byref(SetRequestGetVideoSourceStatusList()),0),0)
        pass
    def test_Tlcv_AsyncRequestGetParam(self):
        self.assertEqual(self.ScopeGuarddll.TLCV_AsyncRequest(byref(SetRequestGetParam()),0),0)
        pass
    def test_Tlcv_AsyncRequestSetParam(self):
        self.assertEqual(self.ScopeGuarddll.TLCV_AsyncRequest(byref(SetRequestSetParam()[0]),0),0)
        pass


    def test_SyncRequestRule(self):
        responseP = Getresponse()
        request,header,body = SetRequestSetRule()
        self.assertEqual(self.ScopeGuarddll.TLCV_SyncRequest(byref(request),0,byref(responseP)),0)
        self.assertEqual(responseP.contents.tlcvData.header, 'OK')
        print responseP.contents.tlcvData.header
        print responseP.contents.tlcvData.body

        responseP = Getresponse()
        self.assertEqual(self.ScopeGuarddll.TLCV_SyncRequest(byref(SetRequestGetRule()),0,byref(responseP)),0)
        self.assertEqual(responseP.contents.tlcvData.header, 'tlcv_protocol.scope_guard.RuleList')
        self.assertEqual(responseP.contents.tlcvData.body, body)

        print responseP.contents.tlcvData.header
        ruleList = scope_guard_pb2.RuleList()
        ruleList.ParseFromString(responseP.contents.tlcvData.body)
        #print dir(ruleList)
        #print ruleList.RULE_LIST_FIELD_NUMBER
        print ruleList.rule_list
        #print responseP.contents.tlcvData.body



        responseP = Getresponse()
        request = SetRequestDelRule()[0]
        self.assertEqual(self.ScopeGuarddll.TLCV_SyncRequest(byref(request),0,byref(responseP)),0)
        self.assertEqual(responseP.contents.tlcvData.header, 'WARNING')
        print responseP.contents.tlcvData.header
        print responseP.contents.tlcvData.body

        responseP = Getresponse()
        self.assertEqual(self.ScopeGuarddll.TLCV_SyncRequest(byref(SetRequestGetRule()),0,byref(responseP)),0)
        self.assertEqual(responseP.contents.tlcvData.header, 'tlcv_protocol.scope_guard.RuleList')
        self.assertEqual(responseP.contents.tlcvData.body, body)

        print responseP.contents.tlcvData.header
        ruleList = scope_guard_pb2.RuleList()
        ruleList.ParseFromString(responseP.contents.tlcvData.body)
        #print dir(ruleList)
        #print ruleList.RULE_LIST_FIELD_NUMBER
        print ruleList.rule_list
        #print responseP.contents.tlcvData.body

    def test_SyncRequestDelRule(self):
        responseP = Getresponse()
        request = SetRequestDelRule()[0]
        self.assertEqual(self.ScopeGuarddll.TLCV_SyncRequest(byref(request),0,byref(responseP)),0)
        self.assertEqual(responseP.contents.tlcvData.header, 'WARNING')
        print responseP.contents.tlcvData.header
        print responseP.contents.tlcvData.body
        pass

    def test_SyncRequestGetRule(self):
        responseP = Getresponse()
        self.assertEqual(self.ScopeGuarddll.TLCV_SyncRequest(byref(SetRequestGetRule()),0,byref(responseP)),0)
        self.assertEqual(responseP.contents.tlcvData.header, 'tlcv_protocol.scope_guard.RuleList')
        #self.assertEqual(responseP.contents.tlcvData.body, body)

        print responseP.contents.tlcvData.header
        ruleList = scope_guard_pb2.RuleList()
        ruleList.ParseFromString(responseP.contents.tlcvData.body)
        #print dir(ruleList)
        #print ruleList.RULE_LIST_FIELD_NUMBER
        print ruleList.rule_list
        #print responseP.contents.tlcvData.body

    def test_SyncRequestParam(self):
        responseP = Getresponse()
        request,header,body = SetRequestSetParam()
        self.assertEqual(self.ScopeGuarddll.TLCV_SyncRequest(byref(request),0,byref(responseP)),0)
        self.assertEqual(responseP.contents.tlcvData.header, 'OK')
        print responseP.contents.tlcvData.header
        print responseP.contents.tlcvData.body

        responseP = Getresponse()
        self.assertEqual(self.ScopeGuarddll.TLCV_SyncRequest(byref(SetRequestGetParam()),0,byref(responseP)),0)
        self.assertEqual(responseP.contents.tlcvData.header, 'tlcv_protocol.scope_guard.Param')
#        self.assertEqual(responseP.contents.tlcvData.body, body)


        print responseP.contents.tlcvData.header
        param = scope_guard_pb2.Param()
        param.ParseFromString(responseP.contents.tlcvData.body)
        print param.sensitivity
        #print responseP.contents.tlcvData.body

    def test_SyncRequestGetVersion(self):
        responseP = Getresponse()
        self.assertEqual(self.ScopeGuarddll.TLCV_SyncRequest(byref(SetRequestGetVersion()),0,byref(responseP)),0)
        self.assertEqual(responseP.contents.tlcvData.header, 'tlcv_protocol.Version')
        version  =  tlcv_protocol_pb2.Version()
        version.ParseFromString(responseP.contents.tlcvData.body)
        print version.name
        print version.epoch
        print version.major
        print version.minor
        print version.desInfo
        #print responseP.contents.tlcvData.body


    def test_SyncRequestGetServerStatus(self):
        responseP = Getresponse()
        self.assertEqual(self.ScopeGuarddll.TLCV_SyncRequest(byref(SetRequestGetServerStatus()),0,byref(responseP)),0)
        self.assertEqual(responseP.contents.tlcvData.header, "tlcv_protocol.ServerStatus")
        serverStatus = tlcv_protocol_pb2.ServerStatus()
        serverStatus.ParseFromString(responseP.contents.tlcvData.body)
        print serverStatus.status
        #print responseP.contents.tlcvData.body


    def test_SyncRequestGetProtocolInfo(self):
        responseP = Getresponse()
        self.assertEqual(self.ScopeGuarddll.TLCV_SyncRequest(byref(SetRequestGetProtocolInfo()),0,byref(responseP)),0)
        self.assertEqual(responseP.contents.tlcvData.header, "tlcv_protocol.ProtocolInfo")
        protocolInfo = tlcv_protocol_pb2.ProtocolInfo()
        protocolInfo.ParseFromString(responseP.contents.tlcvData.body)
        #print dir(protocolInfo)
        print len(protocolInfo.proto_name_list)
        print protocolInfo.proto_name_list

        #print responseP.contents.tlcvData.body

    def test_Tlcv_SyncRequest(self):
        self.test_SyncRequestParam()
        self.test_SyncRequestRule()
        self.test_SyncRequestGetVersion()
        self.test_SyncRequestGetServerStatus()
        self.test_SyncRequestGetProtocolInfo()
        pass

    def test_Tlcv_GetPushingData(self):

        pass

    def test_TLCV_GetResponseData(self):
        time.sleep(2)
        arr = TlcvArray();
        responseSize = self.ScopeGuarddll.TLCV_GetResponseData(c_int(0),byref(arr))
        self.assertGreaterEqual(responseSize,0)
        TlcvResponseP = POINTER(TlcvResponse)
        print responseSize
        for i in range(responseSize):
            responseP = cast(arr.data[i],TlcvResponseP)
            print responseP.contents.tlcvData.header
            print responseP.contents.tlcvData.body
            self.assertEqual(self.ScopeGuarddll.TLCV_DestoryData(c_void_p(arr.data[i])),0)
        pass



def testfun():
    x =1
    y =2
    return x,y

def SyncRequest():

    testsAsyncRequest =[
        'test_Tlcv_AsyncRequestSetRule',
        'test_Tlcv_AsyncRequestGetRule',
        'test_Tlcv_AsyncRequestGetVersion',
        'test_Tlcv_AsyncRequestGetProtocolInfo',
        'test_Tlcv_AsyncRequestGetServerStatus',
        'test_Tlcv_AsyncRequestGetVideoSourceStatusList',
        'test_Tlcv_AsyncRequestGetParam',
        'test_Tlcv_AsyncRequestSetParam'
    ]

    testSyncrequest =[
        'test_SyncRequestParam',
        'test_SyncRequestRule',
        'test_SyncRequestGetRule',
        'test_SyncRequestDelRule',
        'test_SyncRequestGetVersion',
        'test_SyncRequestGetServerStatus',
        'test_SyncRequestGetProtocolInfo'
    ]

    tests = ['test_Tlcv_SyncRequest']

    tests1 = ['test_Tlcv_Init', 'test_Tlcv_SyncRequest','test_Tlcv_Free']
    tests11 = ['test_Tlcv_Init', 'test_SyncRequestGetRule','test_Tlcv_Free']
    tests2 = ['test_Tlcv_Init', 'test_Tlcv_OpenVideo','test_Tlcv_SyncRequest','test_Tlcv_CloseVideo','test_Tlcv_Free']
    #print tests*2+tests1[1]
    tests3 = ['test_Tlcv_Init', 'test_Tlcv_AsyncRequest','test_Tlcv_Free']
    tests4 = ['test_Tlcv_Init', 'test_Tlcv_OpenVideo','test_Tlcv_AsyncRequest','test_TLCV_GetResponseData','test_Tlcv_CloseVideo','test_Tlcv_Free']

    tests5 = ['test_Tlcv_Init'] + testsAsyncRequest + ['test_Tlcv_Free']
    tests6 = ['test_Tlcv_Init', 'test_Tlcv_OpenVideo'] + testsAsyncRequest + ['test_TLCV_GetResponseData','test_Tlcv_CloseVideo','test_Tlcv_Free']
    tests7 = ['test_Tlcv_Init'] + testSyncrequest + ['test_Tlcv_Free']
    tests8 = ['test_Tlcv_Init', 'test_Tlcv_OpenVideo'] + testSyncrequest + ['test_TLCV_GetResponseData','test_Tlcv_CloseVideo','test_Tlcv_Free']
    return unittest.TestSuite(map(TestScopeGuradDll, tests7))

def AsyncRequestNotOpen():
    tests = ['test_Tlcv_Init', 'test_Tlcv_AsyncRequest','test_Tlcv_Free']
    return unittest.TestSuite(map(TestScopeGuradDll, tests2))

if __name__ =='__main__':
    #x,y= testfun()
    #print y
    unittest.TextTestRunner(verbosity=2).run(SyncRequest())
