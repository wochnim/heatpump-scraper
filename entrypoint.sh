#!/bin/bash
mkdir -p /data/.android
ln -sfn /data/.android /root/.android
adb kill-server
adb start-server
exec "$@"
