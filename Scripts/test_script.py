#Here we can do some coding
a=['test','test2']
print(a)
b={'hallo':'test3','hallo2':'test4'}
c={'a':{'hallo':'test3','hallo2':'test4'},'b':{'test':'testx'}}
a.extend([key for key,value in c['b'].items()])
print(a)