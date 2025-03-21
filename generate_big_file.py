with(open("bigfiletest2.txt", 'w')) as f:
    for i in range(289232):
        pseudotokens = [i] * 800000
        f.write(str(pseudotokens)+ "\n")