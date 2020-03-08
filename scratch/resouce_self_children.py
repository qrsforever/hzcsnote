import resource
from sys import getsizeof

s_s = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
c_s = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024

print(s_s, c_s)

print(getsizeof(object()))

objs = []

for i in range(10*1024**2):
    objs.append(object())

s_e = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
c_e = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024

print(s_e, c_e)
print(s_e - s_s, c_e - c_s)
