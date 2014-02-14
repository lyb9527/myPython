import functools

print('lambda')
func = lambda x,y:x+y
print(func(3,4))

print('\n函数作为参数传递')
def test(f,a,b):
    print('test')
    print(f(a,b))
test(func,4,5)

print('\n 改变函数')
test((lambda x,y:x**2+y),9,16)

print('\n map()')
re = map((lambda x:x+3),[1,3,5,6])
for i in re:
    print(i)
print('\n')
re2=map((lambda x,y:x+y),[1,2,3],[4,5,6])
for i in re2:
    print(i)

print('\n filter()')
def func(a):
    if a>100:
        return True
    else:
        return False
re3=filter(func,[10,51,101,191])
for i in re3:
    print(i)

print('\n reduce()')
print(functools.reduce((lambda x,y:x+y),[1,2,5,7,9]))