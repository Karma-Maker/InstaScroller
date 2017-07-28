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

vc = ViewClient(device=device, serialno=serialno)

content_list = vc.findViewByIdOrRaise("android:id/list")

snapshotIdx = 0

while True:
    content_list.uiScrollable.flingForward()

    # vc = ViewClient(device=device, serialno=serialno)
    vc.dump(content_list.getId())

    subtitle = vc.findViewWithText("Sponsored")

    if subtitle is not None:
        os.system("adb exec-out screencap -p > my_snapshot_{}.png".format(snapshotIdx))
        snapshotIdx = snapshotIdx + 1
