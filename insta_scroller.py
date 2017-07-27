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

print [method for method in dir(content_list.uiScrollable) if callable(getattr(content_list.uiScrollable, method))]


while False:
    content_list.uiScrollable

    # vc = ViewClient(device=device, serialno=serialno)
    vc.dump(content_list.getId())

    subtitle = vc.findViewWithText("Sponsored")

    if subtitle is not None:
        os.system("adb exec-out screencap -p > my_snapshot_{}.png".format(snapshotIdx))
        snapshotIdx = snapshotIdx + 1
