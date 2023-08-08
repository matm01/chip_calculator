import streamlit as st
import numpy as np


def get_chip_list(players, chips,  goal, max_chip):

    final = [0 for _ in range(6)]
    values = list(chips.keys())
    max_num = np.array(list(map(lambda x:x//players, chips.values())))
    max_num = np.clip(max_num, 0, max_chip)
    max_val = max_num * np.array(list(chips.keys()))
    lim = max_val[0] + max_val[1] + max_val[2]
    rest = lim%100

    not_include_0, not_include_1, not_include_2 = 0, 0, 0

    while rest!=0:
        not_include_2 = rest//values[2]
        rest = rest-(not_include_2*values[2])
        not_include_1 = rest//values[1]
        rest = rest-(not_include_1*values[1])
        not_include_0 = rest//values[0]
        rest = rest-(not_include_0*values[0])
    not_include = np.append(np.array([not_include_0, not_include_1, not_include_2]), [0,0,0])

    final = [0 for _ in range(len(chips))]

    for i, val in enumerate(max_num[:3]-not_include[:3]):
        final[i] = val
    
    rest = 0

    for i, val in enumerate(final[:3]):
        rest += final[i]*values[i]

    rest = goal - rest
    out_500 = 0

    if rest/100 <= max_num[3]:
        final[3] = int(rest/100)
    else:
        for i in range(int(rest//500)):
            test_val = (rest - (500)*(i+1))/100
            if test_val <= max_num[3]:
                final[3] = int(test_val)
                rest = rest - (test_val*100)
                out_500 = int(rest//500)
                break

    if out_500 > max_num[4]:
        for i in range(int(rest//1000)):
            test_val = (rest - (1000)*(i+1))/500
            if test_val <= max_num[4]:
                final[4] = int(test_val)
                rest = rest - (test_val*500)
                final[5] = int(rest//1000)
                break
    
    else: final[4] = out_500

    return final


ceramic = {5: 50, 10: 49, 25: 79, 100: 70, 500: 25, 1000: 25}
plastic = {0:0, 25:100, 50:50, 100:150, 500:50, 1000:50}


st.markdown('# This is **:red[ChipCalc]**! Your handy poker chip calculator :spades: :hearts: :diamonds: :clubs:')

num_of_players = []
gear = st.radio('Select your chips', ('ceramic', 'plastic'))
chips = ceramic if gear == 'ceramic' else plastic
    
players = st.select_slider('No. of player:', options=[i for i in range(4,11)], value = 8)
if gear == 'ceramic':
    goal = st.number_input('Sum of chips', min_value=500, max_value=4000, step=500, value=1000)
else:
    goal = st.number_input('Sum of chips', min_value=5000, max_value=10000, step=1000, value=5000)
max_chip = st.select_slider('Max. number of chips:', options=[i for i in range(6,13)], value=10)
final = get_chip_list(players, chips, goal, max_chip)
c5, c10, c25, c100, c500, c1000 = st.columns([1,1,1,1,1,1])

test_sum = 0
not_enough_chips = False
max_num = np.array(list(map(lambda x:x//players, chips.values())))

for i, val in enumerate(final):
    test_sum += val*list(chips.keys())[i]
    if final[i] > max_num[i]:
        not_enough_chips = True


if test_sum != goal:
    st.markdown(f'# OOPs something went wrong')


elif not_enough_chips: 
    st.markdown(f'# not enough chips')

else:
    if gear == 'ceramic':
        c5, c10, c25, c100, c500, c1000 = st.columns([1,1,1,1,1,1])
        c5.image(image='pics/5.png')
        c5.markdown(f'# x{final[0]}')
        c10.image(image='pics/10.png')
        c10.markdown(f'# x{final[1]}')
        c25.image(image='pics/25.png')
        c25.markdown(f'# x{final[2]}')
        c100.image(image='pics/100.png')
        c100.markdown(f'# x{final[3]}')
        c500.image(image='pics/500.png')
        c500.markdown(f'# x{final[4]}')
        c1000.image(image='pics/1000.png')
        c1000.markdown(f'# x{final[5]}')
    
    else:
        c5, c10, c25, c100, c500 = st.columns([1,1,1,1,1])
        c5.image(image='pics/p25.png')
        c5.markdown(f'# x{final[1]}')
        c10.image(image='pics/p50.png')
        c10.markdown(f'# x{final[2]}')
        c25.image(image='pics/p100.png')
        c25.markdown(f'# x{final[3]}')
        c100.image(image='pics/p500.png')
        c100.markdown(f'# x{final[4]}')
        c500.image(image='pics/p1000.png')
        c500.markdown(f'# x{final[5]}')



