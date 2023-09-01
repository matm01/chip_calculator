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

    # calculate chips to remove from pool
    to_remove = [0, 0, 0]
    if rest != 0:
        for i in range(2,-1,-1):
            to_remove[i] = rest//values[i]
            rest = rest-(to_remove[i]*values[i])
            if rest == 0: break

    final = [0 for _ in range(len(chips))]
    for i, val in enumerate(max_num[:3]-to_remove):
        final[i] = val
    
    spend = 0
    for i in range(3):
        spend += final[i]*values[i]

    rest = goal - spend

    for i in range(3):
        if rest == 0: break
        for j in range(max_num[i+3]):
            test_val = rest - values[i+3] * (max_num[i+3]-j)
            if test_val == 0 or [False if (i > 1) else (test_val%values[i+4] == 0 and test_val>0)][0]:
                final[i+3] = max_num[i+3] - j
                rest = test_val
                break
    
    if rest / (max_num[5]*values[5]) > 1:
        missing = rest-(max_num[5]*values[5])
        final[5] = max_num[5]
        st.markdown(f'# not enough chips! {missing} missing')
    elif rest != 0: 
        st.markdown(f'# OOPs something went wrong! error:{rest}')



    return final


ceramic = {5: 75, 10: 49, 25: 79, 100: 70, 500: 25, 1000: 25}
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