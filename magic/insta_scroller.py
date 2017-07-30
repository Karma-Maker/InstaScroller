# -*- coding: utf-8 -*-

import time

import re
import sys
import os

from viewclient import ViewClient

os.system("magic/bin/adb start-server")

time.sleep(1)

device, serialno = ViewClient.connectToDeviceOrExit()


package = 'com.instagram.android'
activity = 'activity.MainTabActivity'
component = package + "/." + activity

device.startActivity(component=component)

vc = ViewClient(device=device, serialno=serialno)

content_list = vc.findViewByIdOrRaise("android:id/list")

snapshotIdx = 0

while True:
    vc.dump(content_list.getId())
    sponsored_item = vc.findViewWithText("Sponsored")
    if sponsored_item is not None:
        content_list.uiScrollable.flingForwardBy(sponsored_item.getBounds()[0][1] - content_list.getBounds()[0][1] * 3)
        time.sleep(0.1)
        os.system("magic/bin/adb exec-out screencap -p > snapshots/my_snapshot_{}.png".format(snapshotIdx))
        snapshotIdx = snapshotIdx + 1

    content_list.uiScrollable.flingForwardBy(content_list.getBounds()[1][1] - content_list.getBounds()[0][1] * 3)
