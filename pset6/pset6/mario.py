import cs50

height = -1
s = "#"

while height > 23 or height < 0:
    print("Height: ", end="")
    height = cs50.get_int()
    
for i in range(1, height + 1):
    print("{}{}{}{}{}".format(
        (height-i) * " ", i*s, "  ",  #left blocks and two space 
        i*s, (height-i) * " ")        #right blocks
        )

