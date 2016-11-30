#!/usr/bin/env bash

TARGET="/opt/agocontrol/bin/"
chown root *.py
chgrp root *.py
chmod +x *.py
mv *.py  $TARGET
mv *.conf   $TARGET

