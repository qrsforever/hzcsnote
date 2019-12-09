## TypeError: 'int' object is not iterable

```
2019-12-07 11:17:35,572 - ERROR - zerorpc.channel - zerorpc.ChannelMultiplexer ignoring error on recv
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
Exception: invalid msg format "44": 'int' object is not iterable
2019-12-07 11:17:35,574 - ERROR - zerorpc.channel - zerorpc.ChannelMultiplexer ignoring error on recv
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
Exception: invalid msg format "16": 'int' object is not iterable
2019-12-07 11:17:35,575 - ERROR - zerorpc.channel - zerorpc.ChannelMultiplexer ignoring error on recv
Traceback (most recent call last):
  File "/usr/local/lib/python3.6/site-packages/zerorpc/events.py", line 218, in unpack
    (header, name, args) = unpacked_msg
TypeError: 'int' object is not iterable
```

**未查明**