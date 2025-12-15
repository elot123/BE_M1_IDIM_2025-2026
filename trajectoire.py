import numpy as np
import matplotlib.pyplot as plt

# paremètres géométriques
L1 = 0.06
L2 = 1.00
L3 = 1.20
L4 = 1.40

d1 = 0.025   # écart plaques DEV1
d2 = 0.05    # écart plaques DEV2

# ZONE 1 
def traj_dev1(x0, y0, vy0, V1, Vacc, z_sur_m, N=2000):
    vx = np.sqrt(2*Vacc*z_sur_m)   # vitesse horizontale
    a  = z_sur_m*(V1/d1)           # acceleration verticale
    x = np.linspace(x0, L1, N)
    t = (x - x0)/vx
    y = y0 + vy0*t + 0.5*a*t*t
    vy = vy0 + a*t
    return x, y, x[-1], y[-1], vy[-1]


# ZONE 2 
def traj_drift1(x0, y0, vy0, Vacc, z_sur_m, N=2000):
    vx = np.sqrt(2*Vacc*z_sur_m)
    x = np.linspace(x0, L2, N)
    t = (x - x0)/vx
    y = y0 + vy0*t
    return x, y, x[-1], y[-1], vy0

# ZONE 3 
def traj_dev2(x0, y0, vy0, V2, Vacc, z_sur_m, N=2000):
    vx = np.sqrt(2*Vacc*z_sur_m)
    a  = z_sur_m*(V2/d2)
    x = np.linspace(x0, L3, N)
    t = (x - x0)/vx
    y = y0 + vy0*t + 0.5*a*t*t
    vy = vy0 + a*t
    return x, y, x[-1], y[-1], vy[-1]

# ZONE 4  
def traj_drift2(x0, y0, vy0, Vacc, z_sur_m, N=2000):
    vx = np.sqrt(2*Vacc*z_sur_m)
    x = np.linspace(x0, L4, N)
    t = (x - x0)/vx
    y = y0 + vy0*t
    return x, y, x[-1], y[-1], vy0

#PLOT GLOBAL 
def plot_4zones(Vacc, V1, DEV2_ON=True, V2=10000, z_sur_m=1.602e-19/1.66054e-27):
    if not DEV2_ON:
        V2 = 0

    plt.clf()

    x0=0; y0=0; vy0=0

    x1,y1,x0,y0,vy0 = traj_dev1(x0,y0,vy0,V1,Vacc,z_sur_m)
    x2,y2,x0,y0,vy0 = traj_drift1(x0,y0,vy0,Vacc,z_sur_m)
    x3,y3,x0,y0,vy0 = traj_dev2(x0,y0,vy0,V2,Vacc,z_sur_m)
    x4,y4,x0,y0,vy0 = traj_drift2(x0,y0,vy0,Vacc,z_sur_m)

    print("deviation finale y =", y0*100, "cm")
    

    plt.plot(x1,y1,'b')
    plt.plot(x2,y2,'b')
    plt.plot(x3,y3,'b')
    plt.plot(x4,y4,'b')
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
    plt.grid()
    plt.xlim(0, 1.45)
    plt.ylim(-0.06, +0.06)

    plt.title(f"Trajectoire de l\'ion V1={V1}V Vacc={Vacc}V DEV2={V2}V")

    plt.hlines(d1/2, xmin=0, xmax=L1, color='black')
    plt.hlines(-d1/2, xmin=0, xmax=L1, color='black')

    plt.hlines(d2/2, xmin=L2, xmax=L3, color='black')
    plt.hlines(-d2/2, xmin=L2, xmax=L3, color='black')

    plt.vlines(L4, ymin=0.001, ymax=0.2, color='black')
    plt.vlines(L4, ymin=-0.2, ymax=-0.001, color='black')

    #plt.show()


#plot_4zones(Vacc=1000, V1=15, DEV2_ON=False)




