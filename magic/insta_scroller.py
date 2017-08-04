# -*- coding: utf-8 -*-

import time

import re
import sys
import os
import xml.etree.ElementTree



def startAdbServer():
    os.system("magic/bin/adb start-server")
    time.sleep(1)

#device, serialno = ViewClient.connectToDeviceOrExit()

def startInstagram():
    os.system("magic/bin/adb shell am start -n com.instagram.android/.activity.MainTabActivity")
    time.sleep(0.5)
    
#vc = ViewClient(device=device, serialno=serialno)

def scrollBy(scrollDistance):
    os.system("magic/bin/adb shell input swipe 300 {} 300 0".format(scrollDistance))
    time.sleep(0.5)

def dump():
    os.system("magic/bin/adb shell uiautomator dump")
    os.system("magic/bin/adb pull /sdcard/window_dump.xml magic/window_dump.xml")
    dumpRoot = xml.etree.ElementTree.parse('magic/window_dump.xml').getroot()
    return dumpRoot;

def getNodeBounds(node):
    boundsStr = node.get("bounds")
    boundsArray = boundsStr.replace("][", ",").replace("]", "").replace("[", "").split(",")
    left = int(boundsArray[0])
    top = int(boundsArray[1])
    right = int(boundsArray[2])
    bottom = int(boundsArray[3])
    
    return [left, top, right, bottom] 

sponsoredNode = ""
snapshotIdx = 0

def findSponsoredNode(node):
    print node.get('Text')
    if(node.get('Text') == 'natgeo'):
        sponsoredNode = node
        
        return True

    for childNode in node.findall('node'):
        if(findSponsoredNode(childNode)):
            return True
        
    return False


def takeSnapshot(snapshotIdx):
    os.system("magic/bin/adb exec-out screencap -p > snapshots/my_snapshot_{}.png".format(snapshotIdx, '04d'))
    

#while True:
#    vc.dump(content_list.getId())
#    sponsored_item = vc.findViewWithText("Sponsored")
#    if sponsored_item is not None:
#        content_list.uiScrollable.flingForwardBy(sponsored_item.getBounds()[0][1])
#        time.sleep(0.1)
#        
#        
#
#    content_list.uiScrollable.flingForwardBy(content_list.getBounds()[1][1] - content_list.getBounds()[0][1] * 4)
    
startInstagram()                    
screenHeight = 0.5 * getNodeBounds(dump().find('node'))[3]

while True:
    scrollBy(screenHeight)
    sponsoredNode = ""
    if(findSponsoredNode(dump().find('node'))):
        scrollBy(getNodeBounds(sponsoredNode)[1])
        takeSnapshot(snapshotIdx)
        snapshotIdx = snapshotIdx + 1
        
        
    

