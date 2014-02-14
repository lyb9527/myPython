#Generator
def gen():
    for i in range(4):
        yield i
print(gen())

print('Generator Expression')
G=(x for x in range(4))
for z in G:
    print(z)
    
print('List Comprehension 表推导')
L=[x**2 for x in range(10)]

for i in L:
    print(i)

print('test')
x1=[1,3,5]
y1=[9,12,13]
K=[x**2 for (x,y) in zip(x1,y1) if y>10]
for i in K:
    print(i)