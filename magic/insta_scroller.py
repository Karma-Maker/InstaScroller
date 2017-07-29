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
    firstRow = vc.findViewById("com.instagram.android:id/row_feed_profile_header")
    if firstRow is not None:
        content_list.uiScrollable.flingForwardBy(firstRow.getBounds()[0][1] - content_list.getBounds()[0][1] - 200)
        subtitle = vc.findViewWithText("Sponsored")

        if subtitle is not None:
            os.system("magic/bin/adb exec-out screencap -p > snapshots/my_snapshot_{}.png".format(snapshotIdx))
            snapshotIdx = snapshotIdx + 1

    content_list.uiScrollable.flingForwardBy(content_list.getBounds()[1][1] - content_list.getBounds()[0][1] - 200)
