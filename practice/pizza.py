INGS = ['T', 'M']

class Cell:
    def __init__(self, col, row, ing):
        self.row = row 
        self.col = col 
        self.ing = ing 
        self.taken = False
        self.slice = (0,0)


    def __repr__(self):
        return '(%d,%d): %s %s at %s \n' % (self.col, self.row, self.ing, self.taken, self.slice)

class Slice:
    def __init__(self, cell, pizza):
        self.pizza = pizza
        self.cells = [cell]
        cell.taken = True
        self.rows = 1
        self.cols = 1
        self.i = cell.col 
        self.j = cell.row 
        self.k = cell.col 
        self.l = cell.row
        self.pizza.slices.append(self)
        self.shape()
    
    def numberCells(self):
        return (self.k - self.i + 1)*(self.l - self.j + 1)

    #Gives a slice it's minimum valid shape (minimum ingredients and minimum area)
    def shape(self):
        shapes = []
        for i in range(self.pizza.MAXH):
            for j in range(self.pizza.MAXH):
                if i*j <= self.pizza.MAXH:
                    if (self.i + i <= self.pizza.cols) and (self.j + j <= self.pizza.rows):
                        if self.pizza.notTaken(self.i, self.j, self.i + i - 1, self.j + j - 1):
                            if self.pizza.enoughIngredients(self.i, self.j, self.i + i - 1, self.j + j - 1):
                                shapes.append((i,j))

        
        if len(shapes) == 0:
            self.pizza.slices.remove(self)
            self.cells[0].taken = False
            return
        
        min = 1000000
        for (i,j) in shapes:
            if i*j < min:
                min = i*j
                current = (i,j)
        
        self.cols = current[0]
        self.rows = current[1]
        self.k = self.i + self.cols - 1
        self.l = self.j + self.rows - 1
        for x in range(self.i, self.k + 1):
            for y in range(self.j, self.l + 1):
                self.cells.append(self.pizza.cells[y][x])
                self.pizza.cells[y][x].taken = True
                self.pizza.cells[y][x].slice = (self.i, self.j)

    #Checks if slice has minimum number of ingredients
    def hasIngs(self):
        return self.pizza.enoughIngredients(self.i, self.j, self.k, self.l)

    #Maxes out slice size 
    def maxSize(self):
        flag = True
        if self.l + 1 < self.pizza.rows and self.cols + self.numberCells() <= self.pizza.MAXH:
            for x in range(self.i, self.k + 1):
                if self.pizza.cells[self.l + 1][x].taken:
                    flag = False
        else:
            flag = False

        if flag:
            self.l = self.l + 1
            self.rows = self.rows + 1
            for x in range(self.i, self.k + 1):
                self.cells.append(self.pizza.cells[self.l][x])
                self.pizza.cells[self.l][x].taken = True
                self.pizza.cells[self.l][x].slice = (self.i, self.j)
            self.maxSize()
            return 

        flag = True
        if self.k + 1 < self.pizza.cols and self.rows + self.numberCells() <= self.pizza.MAXH: 
            for y in range(self.j, self.l + 1):
                if self.pizza.cells[y][self.k + 1].taken:
                    flag = False
        else:
            flag = False

        if flag:
            self.k = self.k + 1
            self.cols = self.cols + 1
            for y in range(self.j, self.l + 1):
                self.cells.append(self.pizza.cells[y][self.k])
                self.pizza.cells[y][self.k].taken = True
                self.pizza.cells[y][self.k].slice = (self.i, self.j)
            self.maxSize()
            return 



    def __repr__(self):
        return '%d %d %d %d\n' % (self.i, self.j, self.k, self.l)




class Pizza:
    def __init__(self, rows, cols, ingredients, MINL, MAXH):
        self.MAXH = MAXH
        self.MINL = MINL
        self.slices = []
        self.rows = rows
        self.cols = cols
        self.ingredients = [[ingredients[x][y] for x in range(self.cols)] for y in range(self.rows)]
        self.cells = [[Cell(x,y, ingredients[x][y]) for x in range(self.cols)] for y in range(self.rows)]
        
     #Returns amount of a certain ingredient in a pizza area
    def howMuchIng(self, ing, i, j, k, l):
        res = 0
        for x in range(i,k + 1):
            #print(x)
            for y in range(j,l + 1):
                if self.ingredients[y][x] == ing:
                    res = res + 1
        return res 
        

    #Checks if there are enough ingredients in a pizza area
    def enoughIngredients(self, i, j, k, l):
        for ing in INGS:
            if self.howMuchIng(ing, i, j, k, l) < self.MINL:
                return False
        return True

    #Checks if a bunch of cells is already in a slice
    def notTaken(self, i, j, k, l):
        for x in range(i, k + 1):
            for y in range(j, l + 1):
                if (not x == i) or (not y == j): 
                    if self.cells[y][x].taken:
                        return False
        
        return True
