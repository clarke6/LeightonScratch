from numpy import zeros, savetxt, loadtxt

file = 'WH_Data_3-14-2018.csv'
data = open(file, 'r').read()
derp = data.split('\n')
for eachline in derp:
    if len(eachline)>1:
        eachline = eachline.split(',')

x = zeros((5,5))
savetxt('derp.csv',x,delimiter=',',newline='\n',fmt='%f')

z = loadtxt('derp.csv',delimiter=',')
