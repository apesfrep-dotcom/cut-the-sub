import json
W={1:'one',2:'two',3:'three',4:'four',5:'five',6:'six',7:'seven',8:'eight',12:'twelve',18:'eighteen',9:'nine',15:'fifteen',16:'sixteen',20:'twenty',21:'twenty-one',10:'ten',14:'fourteen',24:'twenty-four'}
D1={2:'half',3:'third',4:'fourth',6:'sixth',8:'eighth'}; DP={2:'halves',3:'thirds',4:'fourths',6:'sixths',8:'eighths'}
def say(n,d): return 'one half' if (n,d)==(1,2) else f"{W[n]} {D1[d] if n==1 else DP[d]}"
L={}
L['chef_try']="Not quite. Let's try that one again. This time you get the boxes and the cut marks to help you."
L['chef_color_miss']="Not quite. Check your boxes. Start at box one, and count carefully."
L['chef_color_show']="Here it is. Look at the colored boxes."
L['chef_cutnow']="Great coloring! Now cut right at the end of your color."
L['chef_cutsplit']="Great! Now cut at the end of your gold piece, and at every dark mark after it."
L['chef_same_hint']="Look at the yellow line. Pick the pieces that reach it."
for d in (2,3,4,6,8):
    L[f'chef_unit_{d}']=f"Color one {D1[d]} first. One {D1[d]} is {W[24//d]} boxes, starting at box one."
    L[f'chef_x_split_{d}']=f"Each piece should be one {D1[d]}. That's {W[24//d]} boxes. Look at the green lines."
for d in (3,4,6,8):
    for n in range(2,d):
        L[f'chef_more_{n}_{d}']=f"Keep going. {say(n,d).capitalize()} is {W[n]} pieces of one {D1[d]}. Color until you reach {W[n*24//d]} boxes."
for d in (2,3,4,6,8):
    for n in range(1,d):
        hops = 'one hop' if n==1 else f'{W[n]} hops'
        L[f'chef_f_{n}_{d}']=f"{say(n,d).capitalize()} is {W[n*24//d]} boxes from zero. That's {hops} of one {D1[d]}."
for d in (2,3,4):
    for n in range(d+1,2*d):
        r=n-d; L[f'chef_f_{n}_{d}']=f"One and {say(r,d)} is one whole sub, plus {say(r,d)} of the next sub. That's {W[n]} hops of one {D1[d]}."
L['chef_x_fair']="Both subs are the same size. Look how far each cut reaches from zero. The one that reaches farther is more."
L['chef_x_left']="The whole sub is all twenty-four boxes. Take away the part that was eaten, and count what's left."
L['chef_x_name']="Count the spaces from zero, not the lines."
L['chef_x_fix']="Check the rookie's cut. Count the boxes from zero."
L['chef_x_two']="Cut the first piece starting at zero. Then measure the second piece starting where the first one ends."
L['chef_x_same']="Look at the yellow line. That's where the fraction ends. Count the pieces that fit before it."
L['chef_ready']="Before we open the shop, get your fraction ladder ready! Grab side A of your fraction sleeve and a marker. The helper ladder tells you how many boxes one piece is."
json.dump(L,open('chef_lines.json','w'),indent=1); print(len(L))
