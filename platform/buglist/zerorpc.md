# During handling of the above exception, another exception occurred

```
2019-12-04 23:10:15,038 - ERROR - zerorpc.channel - zerorpc.ChannelMultiplexer ignoring error on recv
Traceback (most recent call last):
  File "/usr/local/lib/python3.6/site-packages/zerorpc/events.py", line 218, in unpack
    (header, name, args) = unpacked_msg
TypeError: 'int' object is not iterable

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.6/site-packages/zerorpc/channel.py", line 78, in _channel_dispatcher
    event = self._events.recv()
  File "/usr/local/lib/python3.6/site-packages/zerorpc/events.py", line 365, in recv
    event = Event.unpack(get_pyzmq_frame_buffer(blob))
  File "/usr/local/lib/python3.6/site-packages/zerorpc/events.py", line 221, in unpack
    unpacked_msg, e))
Exception: invalid msg format "105": 'int' object is not iterable
2019-12-05 00:54:48,941 - ERROR - zerorpc.channel - zerorpc.ChannelMultiplexer ignoring error on recv
Traceback (most recent call last):
  File "/usr/local/lib/python3.6/site-packages/zerorpc/events.py", line 218, in unpack
    (header, name, args) = unpacked_msg
TypeError: 'int' object is not iterable
```

**未解决**