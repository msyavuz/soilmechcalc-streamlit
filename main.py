import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title('Soil Mechanics Calculators')


#Liquid Limit Calculator Part
st.header("Liquid Limit Calculator")

col1,col2 = st.columns(2)

col1.write("Number of Blows")
nob1 = col1.number_input("",key="nob1",step=1)
nob2 = col1.number_input("",key="nob2",step=1)
nob3 = col1.number_input("",key="nob3",step=1)
nob4 = col1.number_input("",key="nob4",step=1)

col2.write("Moisture Content")
mc1 = col2.number_input("",key="mc1")
mc2 = col2.number_input("",key="mc2")
mc3 = col2.number_input("",key="mc3")
mc4 = col2.number_input("",key="mc4")

col1,col2,col3 = st.columns(3)
llcbutton = col2.button("Plot and calculate", key="llcbutton")

fig_size = (10, 5)
f = plt.figure(figsize=fig_size)

def llccalc(nob1,nob2,nob3,nob4,mc1, mc2,mc3,mc4):
    dt = np.array([
        [nob1, mc1],
        [nob2, mc2],
        [nob3, mc3],
        [nob4, mc4]
    ])
    x = dt[:, 0]
    y = dt[:, 1]

    theta = np.polyfit(x, y, 1)

    fig = plt.figure()


    y_line = theta[1] + theta[0] * x
    plt.scatter(x, y)
    val = theta[1] + theta[0] * 25
    plt.scatter(25, val)
    plt.plot(x, y_line, 'r')
    plt.title('Best fit line')
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')
    return fig, val

if llcbutton:
    fig,val = llccalc(nob1,nob2,nob3,nob4,mc1, mc2,mc3,mc4)
    st.pyplot(fig)
    st.write(str(val))


#Soil Classification System Part

st.header("Soil Classification System")

col1,col2 = st.columns(2)

col1.write("Gravel Percentage")
gp = col1.number_input("",key="gp",step=1)
col1.write("Sand Percentage")
sp = col1.number_input("",key="sp",step=1)
col1.write("Fines Percentage")
fp = col1.number_input("",key="fp",step=1)
col1.write("Liquid Limit")
ll = col1.number_input("",key="ll")
col2.write("Plasticity Index")
pi = col2.number_input("",key="pi")
col2.write("D10")
d10 = col2.number_input("",key="d10")
col2.write("D30")
d30 = col2.number_input("",key="d30")
col2.write("D60")
d60 = col2.number_input("",key="d0")

col1,col2,col3 = st.columns(3)

scsbutton = col2.button("Calculate")


def scscalc(gp,sp,fp,ll,pi,d10,d30,d60):
    if d10 == 0 or d60 == 0 or d30 == 0:
        cu = 0
        cc = 0
    else:
        cu = d60 / d10
        cc = (d30 ** 2) / (d60 * d10)
    if gp > sp and gp > fp:
        if 0 <= fp <= 5:
            if cu > 4.0 and 1.0 < cc < 3.0:
                return 'GW'
            else:
                return 'GP'
        elif fp >= 12:
            if (ll - 20) * 0.73 > pi or pi < 4:
                return 'GM'
            elif (ll - 20) * 0.73 < pi and pi > 7:
                return 'GC'
    if sp > gp and sp > fp:
        if 0 <= fp <= 5:
            if cu > 6 and 1 < cc < 3:
                return 'SW'
            else:
                return 'SP'
        elif fp >= 12:
            if (ll - 20) * 0.73 > pi or pi < 4:
                return 'SM'
            elif (ll - 20) * 0.73 < pi and pi > 7:
                return 'SC'
    if fp > gp and fp > sp:
        if (ll - 20) * 0.73 < pi:
            if ll < 50:
                return 'CL/OL'
            elif ll > 50:
                return 'CH/OH'
        elif (ll - 20) * 0.73 > pi:
            if ll < 50:
                return 'ML/OL'
            elif ll > 50:
                return 'MH/OH'
if scsbutton:
    st.write(scscalc(gp,sp,fp,ll,pi,d10,d30,d60))

#Water Content Calculator Part

st.header("Water Content Calculator")

st.write("Mass of Water")
mw = st.number_input("",key="mw")
st.write("Mass of Solids")
ms = st.number_input("",key="ms")
col1,col2,col3 = st.columns(3)
wcbutton = col2.button("Calculate",key ="wcbutton")

if wcbutton:
    st.write(str(mw/ms))

#Degree of Saturation Calculator Part

st.header("Void Ratio and Degree of Saturation Calculator")

st.write("Bulk Density")
bd = st.number_input("",key="bd",step=1)
st.write("Water Content")
wc = st.number_input("",key="wc")
st.write("Specific Gravity")
gs = st.number_input("",key="sg")
col1,col2 = st.columns(2)
srbutton = col1.button("Calculate Degree of Saturation",key ="srbutton")
vrbutton = col2.button("Calculate Void Ratio",key ="vrbutton")

def srcalc(bd,wc,gs):
    pw = 1000
    res1 = ((wc*gs*pw+(gs*pw))/bd)-1
    res = wc*gs/res1
    return res

def vrcalc(bd,wc,gs):
    pw = 1000
    res = ((wc*gs*pw+(gs*pw))/bd)-1
    return res

if srbutton:
    st.write(str(srcalc(bd,wc,gs)))

if vrbutton:
    st.write(str(vrcalc(bd,wc,gs)))
    