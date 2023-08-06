#!/bin/sh

sed -i 's/ s3api//' /etc/swift/proxy-server.conf
sed -i '/user = swift/a cors_allow_origin = http://localhost:9000' /etc/swift/proxy-server.conf