import cs50

total = 0
print("O hai! How much change is owed?")
debt = cs50.get_float()

while debt < 0:
    print("How much change is owed?")
    debt = cs50.get_float()
    
cent = debt*100

while cent > 0:
    if cent >= 25:
        cent = cent - 25
        total += 1
    elif cent >= 10:
        cent = cent - 10
        total += 1
    elif cent >= 5:
        cent = cent - 5
        total += 1
    else:
        cent = cent - 1
        total += 1
        
print("{}".format(total))        