#! /usr/bin/env python
'''
Copyright (C) 2012  Diego Torres Milano
Created on Oct 1, 2012
@author: diego
'''
import time

import re
import sys
import os

try:
    sys.path.append(os.path.join(os.environ['ANDROID_VIEW_CLIENT_HOME'], 'src'))
except:
    pass

from com.dtmilano.android.viewclient import ViewClient, TextView, EditText

device, serialno = ViewClient.connectToDeviceOrExit()


package = 'com.instagram.android'
activity = 'activity.MainTabActivity'
component = package + "/." + activity

device.startActivity(component=component)

time.sleep(1)

vc = ViewClient(device=device, serialno=serialno)

content_list = vc.findViewByIdOrRaise("android:id/list")
print content_list

snapshotIdx = 0

while True:
    content_list.uiScrollable.flingForward()

    vc = ViewClient(device=device, serialno=serialno)
    subtitle = vc.findViewById("com.instagram.android:id/row_feed_photo_subtitle")

    if subtitle is not None:
        vc = ViewClient(device=device, serialno=serialno)
        print subtitle.getText()
        if "Sponsored" in subtitle.getText():
            device.takeSnapshot().save('my_snapshot_{}.png'.format(snapshotIdx), 'PNG')
            snapshotIdx += 1
