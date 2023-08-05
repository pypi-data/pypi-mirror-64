# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from swat_em import datamodel





wdg = datamodel()

#  wdg.genwdg(Q=12, P=10, m=3, w=1, layers=2) # passt
#  wdg.genwdg(Q=12, P=10, m=3, w=1, layers=1) # passt


#  wdg.genwdg(Q=6, P=2, m=3, w=-1, layers=1)
#  wdg.genwdg(Q=12, P=2, m=3, w=-1, layers=1)
#  wdg.genwdg(Q=12, P=2, m=3, w=6, layers=2)
#  wdg.genwdg(Q=12, P=2, m=3, w=5, layers=2)

#  wdg.genwdg(Q=12, P=4, m=3, w=-1, layers=1)

wdg.genwdg(Q=9, P=2, m=3, w=-1, layers=2)



#  S = [[1, 2, -7, -8], [5, 6, -11, -12], [-3, -4, 9, 10]]
#  wdg.set_machinedata(Q=12, p=1, m=3)
#  wdg.set_phases(S)








def flatten(l):
    return [item for sublist in l for item in sublist]



def create_wdg_overhang(S, Q, num_layers, w = None, optimize_wdg_overhang = False):
    '''
    Generate the winding overhang (connection of the coil sides).

    Parameters
    ----------
    S :                     list of lists
                            winding layout
    Q :                     integer
                            number of slots
    mum_layers :            integer
                            number winding layers
                 
    optimize_wdg_overhang : Boolean
                            number of phases
             
    Returns
    -------
    return : list 
             Winding connections for all phases, len = num_phases,
             format: [[(from_slot, to_slot, stepwidth, direction), ()], [(), ()], ...]
             from_slot: slot with positive coil side of the coil
             to_slot:   slot with negative coil side of the coil
             stepwidth: distance between from_slot to to_slot
             direction: winding direction (1: from left to right, -1: from right to left)
    '''
    head = []
    for ph_ in S:
        head.append([])

        ph = flatten(ph_)
        pos = []
        neg = []
        for p in ph:
            if p>0:
                pos.append(p)
            else:
                neg.append(-p)
        if len(pos) != len(neg):
            raise Exception('Number of positive and negative coils sides must be equal')

        for kpos in range(len(pos)):
            
            diff = []
            direct_ = []
            for kneg in range(len(neg)):
                diff1 = abs(pos[kpos] - neg[kneg])
                diff2 = abs( abs(pos[kpos] - neg[kneg]) -Q )
                diff_tmp = diff1 if diff1<diff2 else diff2
                diff.append(diff_tmp)
            
            if w is None or optimize_wdg_overhang:
                index_min = min(range(len(diff)), key=diff.__getitem__)
            else:
                index_min = diff.index(w)

            if neg[index_min] - pos[kpos] == diff[index_min]: # forward, no overflow
                direct = 1
            elif neg[index_min] - pos[kpos] + Q == diff[index_min]: # forward, no overflow
                direct = 1
            else:
                direct = -1

            head[-1].append((pos[kpos], neg.pop(index_min), diff[index_min], direct))
    return head


S = wdg.get_phases()
Q = wdg.get_num_slots()
w = wdg.get_windingstep()
num_layers = wdg.get_num_layers()
head = create_wdg_overhang(S, Q, num_layers, w = w, optimize_wdg_overhang = False)


print('head:', head)
# head[from_slot, to_slot, windingstep, direction]




import matplotlib.pyplot as plt
try: # Interactive plotting
    __IPYTHON__
    plt.ion()
except NameError:
    pass







def gen_coil_lines(w, h1 = 0.75, h2 = 1.5, db1 = 0.1, Np1 = 21):
    '''
    Create lines of a coil for plotting.

    Parameters
    ----------
    w :  integer
         width of the coil in slots
    h1:  float
         height of the coil side in the slot
    h2:  float
         max height of the winding overhang
    db1: float
         distance of the coil side to the middle of the slot;
         should be 0..0.2
    Np1: integer
         number of plotting points in the line of the winding overhang

    Returns
    -------
    x : list 
        x values of the coil for plotting
    y : list
        y values of the coil for plotting
    '''
    x1, y1 = db1, h1
    x2, y2 = w/2, h2
    x3, y3 = w-db1, h1
    x4, y4 = x3, -y3
    x5, y5 = x2, -x2
    x6, y6 = x1, -y1

    x = []
    y = []
    x_ = np.linspace(x1, x3, Np1)
    y_ = np.interp(x_, [x1,x2,x4], [y1,y2,y3])
    x += x_.tolist()
    y += y_.tolist()

    x += x_[::-1].tolist()
    y += (-1*y_[::-1]).tolist()
    x.append(x[0])
    y.append(y[0])
    return x, y


def gen_slot_lines(Q, bz, hz):
    '''
    Create lines of a slot for plotting.

    Parameters
    ----------
    q :  integer
         number of slots
    bz:  float
         width of the tooth -> Slot width = 1 - bz
         so bz should be around 0.5
    hz:  float
         height of the slots

    Returns
    -------
    x : list 
        x values of the slots for plotting
    y : list
        y values of the slots for plotting
    '''
    x = []
    y = []
    for k in range(Q+1):
        x1 = k-0.5
        if k == 0:
            x += [x1, x1, x1+bz/2, x1+bz/2, x1, np.nan]
        elif k == Q:
            x += [x1-bz/2, x1-bz/2, x1, x1, x1-bz/2, np.nan]
        else:
            x += [x1-bz/2, x1-bz/2, x1+bz/2, x1+bz/2, x1-bz/2, np.nan]
        y += [-hz, hz, hz, -hz, -hz, np.nan]
    return x, y



plt.figure(1)
plt.clf()

x, y = gen_slot_lines(Q, bz = 0.5, hz = 0.5)
plt.plot(x, y, 'grey')


i = 1
for phase in head:
    x = []
    y = []
    for coil in phase:
        w = coil[2]
        x_, y_ = gen_coil_lines(coil[2], h1 = 0.5, h2=0.5+w/6)
        x_, y_ = np.array(x_), np.array(y_)
        
        direct = coil[3]
        if direct > 0:
            x_ += coil[0]
        else:
            x_ += coil[1]

        # split coil on right border
        x_2 = x_.copy()
        y_2 = y_.copy()
        x_2[x_<Q-0.5] = np.nan
        x_2 -= Q
        y_2[x_<Q-0.5] = np.nan
        
        y_[x_>Q-0.5] = np.nan
        x_[x_>Q-0.5] = np.nan
        
        x += x_.tolist()
        y += y_.tolist()
        
        x += [np.nan]
        y += [np.nan]
        
        x += x_2.tolist()
        y += y_2.tolist()
            
        x += [np.nan]
        y += [np.nan]


    plt.plot(x, y, label='phase '+str(i))
    i += 1



plt.legend()
