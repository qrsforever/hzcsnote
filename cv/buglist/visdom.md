# j_spring_security_check

```
2019-12-05T01:52:32.047681267Z Learning rate = [0.0004, 0.0004]	Loss = 7.66732836 (ave = 7.57923882)
2019-12-05T01:52:32.047689344Z 
2019-12-05T01:52:32.690810595Z 116.85.34.108 - - [05/Dec/2019 01:52:32] "POST /j_spring_security_check HTTP/1.1" 404 -
2019-12-05T01:52:59.247846638Z ERROR:tornado.application:Uncaught exception POST /j_spring_security_check (116.85.43.69)
2019-12-05T01:52:59.247927675Z HTTPServerRequest(protocol='http', host='116.85.47.250:8140', method='POST', uri='/j_spring_security_check', version='HTTP/1.1', remote_ip='116.85.43.69')
2019-12-05T01:52:59.247945985Z Traceback (most recent call last):
2019-12-05T01:52:59.247953140Z   File "/usr/local/lib/python3.6/dist-packages/tornado/web.py", line 1697, in _execute
2019-12-05T01:52:59.247961145Z     result = method(*self.path_args, **self.path_kwargs)
2019-12-05T01:52:59.247968063Z   File "/usr/local/lib/python3.6/dist-packages/visdom/server.py", line 1085, in post
2019-12-05T01:52:59.247975617Z     json_obj = tornado.escape.json_decode(self.request.body)
2019-12-05T01:52:59.247982508Z   File "/usr/local/lib/python3.6/dist-packages/tornado/escape.py", line 83, in json_decode
2019-12-05T01:52:59.247989657Z     return json.loads(to_basestring(value))
2019-12-05T01:52:59.247997204Z   File "/usr/lib/python3.6/json/__init__.py", line 354, in loads
2019-12-05T01:52:59.248004945Z     return _default_decoder.decode(s)
2019-12-05T01:52:59.248011555Z   File "/usr/lib/python3.6/json/decoder.py", line 339, in decode
2019-12-05T01:52:59.248018532Z     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
2019-12-05T01:52:59.248025084Z   File "/usr/lib/python3.6/json/decoder.py", line 357, in raw_decode
2019-12-05T01:52:59.248031945Z     raise JSONDecodeError("Expecting value", s, err.value) from None
2019-12-05T01:52:59.248054655Z json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
2019-12-05T01:52:59.248060568Z ERROR:root:ERROR: 500: {'exc_info': (<class 'json.decoder.JSONDecodeError'>, JSONDecodeError('Expecting value: line 1 column 1 (char 0)',), <traceback object at 0x7f5cc30dee48>)}
2019-12-05T01:52:59.248317968Z ERROR:tornado.access:500 POST /j_spring_security_check (116.85.43.69) 1.66ms
```

**未解决**