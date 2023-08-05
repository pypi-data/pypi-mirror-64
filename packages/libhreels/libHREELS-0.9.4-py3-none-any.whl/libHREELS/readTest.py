file = 'readTest'
file = "/mnt/d/Data/Python/HREELS/expHREELS/data/I2L02.gph"

with open(file, 'r', encoding='iso-8859-15') as f:
    line = f.readline()
    print('>>>',line)
    code=f.readline().split()
    if code != "DELTA":
        print ("Data file has wrong format!",code)
    for line in f:
        print('>>>',line)
