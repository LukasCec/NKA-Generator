import turtle


def kmen():
    pero.pensize(20)
    pero.pencolor("brown")
    #pero.left(90)
    pero.forward(80)


def koruna1():
    pero.fillcolor("green")
    pero.begin_fill()
    pero.pensize(20)
    pero.pencolor("green")
    pero.right(90)
    pero.forward(-50)
    pero.forward(100)
    pero.left(120)
    pero.forward(100)
    pero.left(120)
    pero.forward(100)
    pero.left(120)
    pero.end_fill()


def koruna2():
    pero.fillcolor("green")
    pero.begin_fill()
    pero.pensize(20)
    pero.pencolor("green")
    pero.forward(40)
    pero.dot(114)



def strom1():
    pero.pendown()
    kmen()
    koruna1()
    pero.penup()
    pero.forward(50)
    pero.right(90)
    pero.forward(80)
    pero.right(180)


def strom2():
    pero.pendown()
    kmen()
    koruna2()
    pero.penup()
    pero.right(180)
    pero.forward(121)
    pero.right(180)


def krok():
    pero.right(90)
    pero.forward(140)
    pero.left(90)

def strecha():
    pero.fillcolor("orange")
    pero.begin_fill()
    pero.pensize(10)
    pero.pencolor("orange")
    pero.right(90)
    pero.forward(100)
    pero.left(120)
    pero.forward(100)
    pero.left(120)
    pero.forward(100)
    pero.left(120)
    pero.end_fill()

def budova():
    pero.fillcolor("blue")
    pero.begin_fill()
    pero.pensize(4)
    pero.pencolor("blue")
    pero.forward(100)
    pero.right(90)
    pero.forward(100)
    pero.right(90)
    pero.forward(100)
    pero.right(90)
    pero.forward(100)
    pero.right(90)
    pero.forward(100)
    pero.end_fill()

def dom():
    pero.forward(140)
    pero.right(90)
    pero.forward(100)
    pero.right(180)
    budova()
    strecha()

tabula = turtle.Screen()
pero = turtle.Turtle()


pero.left(90)
strom1()
krok()

strom1()
krok()

strom1()
krok()

strom2()
krok()

strom2()
krok()

strom2()

pero.left(90)
pero.forward(700)
pero.left(90)
pero.forward(250)

pero.left(180)
pero.pendown()
budova()
strecha()
pero.penup()

dom()

dom()



pero.fillcolor("yellow")


tabula.mainloop()