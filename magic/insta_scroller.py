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
    os.system("magic/bin/adb shell input swipe 300 {} 300 300".format(300 + scrollDistance / 2))
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

snapshotIdx = 0

def findSponsoredNode(node):
    if(node.get('text') == 'Sponsored'):
        print "SPONSORED !!!!"
        return node

    for childNode in node.findall('node'):
        sponsoredNode = findSponsoredNode(childNode)    
        if(sponsoredNode is not None):
            return sponsoredNode
        
    return None


def takeSnapshot(snapshotIdx, imageIdx):
    os.system("magic/bin/adb exec-out screencap -p > snapshots/snapshot_{}_{}.png".format(snapshotIdx, imageIdx, '04d'))

    
    
startInstagram()   

screenHeight = 555;

while True:
    try: 
        root = dump()
    except:
        print "Unable to dump this part of the screen" #which is wierd
        scrollBy(screenHeight)
        continue
    
    if screenHeight == 555:
        screenHeight = getNodeBounds(root.find('node'))[3]
    sponsoredNode = findSponsoredNode(root.find('node'))
    if(sponsoredNode is not None):
        scrollBy(getNodeBounds(sponsoredNode)[1])
        takeSnapshot(snapshotIdx, 1)
        scrollBy(screenHeight / 2)   
        takeSnapshot(snapshotIdx, 2)

        snapshotIdx = snapshotIdx + 1
            
    scrollBy(screenHeight)   
    

