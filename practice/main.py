from pizza import Pizza, Slice

##Reading file and collecting first line of data

EXAMPLE_DATA    = 'data/a_example.in'
SMALL_DATA      = 'data/b_small.in'
MEDIUM_DATA     = 'data/c_medium.in'
BIG_DATA        = 'data/d_big.in'

FILES = [EXAMPLE_DATA, SMALL_DATA, MEDIUM_DATA, BIG_DATA]

for data in FILES:
    print('%s:' % data)
    f = open(data, 'r')
    
    frow = tuple(f.readline().split(' '))
    
    ROWS = int(frow[0])
    COLS = int(frow[1])
    MINL = int(frow[2])
    MAXH = int(frow[3])
    
    ingredients = [['0' for x in range(ROWS)] for y in range(COLS)]
    for i in range(ROWS):
        st = tuple(f.readline())
        for j in range(COLS):
            ingredients[j][i] = st[j]
    
    pizza = Pizza(ROWS, COLS, ingredients, MINL, MAXH)
    
    for l in pizza.cells:
        for c in l:
            if not c.taken:
                s = Slice(c, pizza)
    size_sum = 0
    for s in pizza.slices:
        s.maxSize()
        size_sum += s.numberCells() 
    
    print('%d points out of %d\n' % (size_sum, ROWS*COLS))


    f = open('solutions/output%s' % data[5], 'w')

    f.write('%d\n' % len(pizza.slices))
    for s in pizza.slices:
        f.write(str(s))

