#!/bin/sh
echo "  =====关闭原服务======"
PROCESS=`ps -ef |grep python |grep -v grep|grep app.py|awk '{print $2}'`
for i in $PROCESS
do
  echo "Kill the $1 process [ $i ]"
  sudo kill -9 $i
done

echo "  =====启动服务======"
nohup /path/to/your/venv/python app.py >/dev/null 2>&1 &
echo "  =====光电控制服务已启动======"