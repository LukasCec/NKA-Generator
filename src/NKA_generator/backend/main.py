import turtle

# Vytvaranie vlastnej funkcie
def vzor():
    pero.dot(50,'black')
    pero.forward(50)
    pero.dot(50,'lightgray')
    pero.forward(50)

def vzor2():
    pero.dot(50, 'black')
    pero.dot(25, 'lightgray')
    pero.forward(50)
    pero.dot(50, 'lightgray')
    pero.dot(25, 'black')
    pero.forward(50)

def obrazok():
    pero.fillcolor('yellow') # nastavuje farbu vyplne
    pero.begin_fill() #vsetky nasledujuce prikazy budu mat vypln
    pero.forward(100)
    pero.left(120)
    pero.forward(50)
    pero.left(60)
    pero.forward(50)
    pero.left(60)
    pero.forward(50)
    pero.left(120)
    pero.end_fill() # ukoncenie vyplnovania

def obrazok2():
    pero.fillcolor('yellow') # nastavuje farbu vyplne
    pero.begin_fill() #vsetky nasledujuce prikazy budu mat vypln
    pero.forward(100)
    pero.right(120)
    pero.forward(50)
    pero.right(60)
    pero.forward(50)
    pero.right(60)
    pero.forward(50)
    pero.right(120)
    pero.end_fill() # ukoncenie vyplnovania

tabula = turtle.Screen()
pero = turtle.Turtle()
pero.penup()

vzor() # Použitie vytvorenej funkcie
vzor() # Použitie vytvorenej funkcie
pero.right(90)
vzor() # Použitie vytvorenej funkcie



pero.right(90)
pero.forward(200)
pero.right(90)
pero.right(90)

# A
vzor2()
vzor2()

#presun
pero.right(180)
pero.forward(200)
pero.left(90)
pero.forward(100)
pero.left(90)


# B
vzor2()
pero.left(180)
pero.forward(50)
pero.left(180)
pero.right(90)
pero.forward(50)
pero.right(90)
vzor2()



#C
pero.left(90)
pero.forward(100)
pero.left(90)
vzor2()
pero.left(180)
pero.forward(150)
pero.left(90)
pero.forward(50)
pero.left(90)
pero.forward(50)
vzor2()



obrazok()
obrazok2()

tabula.mainloop()



 # b) def vzor je definícia funkcie a vzor() je už volanie(spustenie) danej funkcie
 # c) je potrebné znova zavolať funkciu vzor() (riadok č. 16)

 #VYSVETLENIE
# 1) použitim funckie sa vyhneme zbytočnému opakovanie rovnakého kódu a program bude kratší
# 2) ----
# 3) Vytvárame ju raz, v našom pripade ju používame 3 krát ale môže byť použita koľko chceme krát
# 4) def meno_funkcie():
#    def - dava programu vedieť že sa jedná o definíciu funkice
#    meno_funkcie - musi byť unikátne
# 5) končí príkazom   pero.forward(50) riadok č. 8
# 6) program ignoruje komentáre, zbehne normalne
# 7) rychlejšia orientacia v kode, kod pochopi aj cudzi človek




