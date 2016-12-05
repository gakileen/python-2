fr = open('/Users/acmac/xxx/qq_channel.txt', 'r+')
fw = open('/Users/acmac/xxx/qq_channel_1.txt', 'w+')

line = ''
for line in fr:
    i1 = line.index('[')
    i2 = line.index(']')
    name = line[0:i1]
    code = line[i1+1:i2]
    s = '{ "_id" : "%s", "name" : "%s", "channel_code" : "" }\n' % (code, name)
    fw.write(s)


fw.flush()
fw.close()
fr.close()
