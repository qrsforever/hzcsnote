pid=`ps -eo pid,args | grep "http.server 9091" | grep -v grep | cut -d\  -f 2`
if [[ x$pid != x ]]
then
    echo "kill -9 $pid"
    kill -9 $pid
fi
nohup python3 -m http.server 9091 2>&1 > /tmp/9091.log &
