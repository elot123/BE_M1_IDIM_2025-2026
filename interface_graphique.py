# interface.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons, Button

import trajectoire as q1  

def compute_trajectory(Vacc, V1, V2, dev2_on, z_sur_m, N=2000):
    if not dev2_on:
        V2 = 0.0

    x0 = 0.0
    y0 = 0.0
    vy0 = 0.0

    x1, y1, x0, y0, vy0 = q1.traj_dev1(x0, y0, vy0, V1, Vacc, z_sur_m, N=N)
    x2, y2, x0, y0, vy0 = q1.traj_drift1(x0, y0, vy0, Vacc, z_sur_m, N=N)
    x3, y3, x0, y0, vy0 = q1.traj_dev2(x0, y0, vy0, V2, Vacc, z_sur_m, N=N)
    x4, y4, x0, y0, vy0 = q1.traj_drift2(x0, y0, vy0, Vacc, z_sur_m, N=N)

    x = np.concatenate([x1, x2, x3, x4])
    y = np.concatenate([y1, y2, y3, y4])

    y_final = y0  # à x = L4

    vx = np.sqrt(2.0 * Vacc * z_sur_m)  # [m/s]
    t_flight = q1.L4 / vx               # [s]

    return x, y, y_final, V2, t_flight


def main():
    # paramètres init
    Vacc0 = 1000.0
    V10 = 15.0
    V20 = 10000.0
    dev2_on0 = False

    # slider m/z (en u/e)
    mz0 = 1.0  # 1 = proton 
    e_over_amu = 1.602e-19 / 1.66054e-27  # (C/kg) pour 1e sur 1u
    z_sur_m_default = e_over_amu / mz0     # q/m = (e/amu) / (m/z)

    # raccourcis depuis question1.py
    L1, L2, L3, L4 = q1.L1, q1.L2, q1.L3, q1.L4
    d1, d2 = q1.d1, q1.d2

    # diaphragme: ouverture +- 1 mm 
    y_aperture = 0.001  # [m]

    fig, ax = plt.subplots(figsize=(10, 5))
    plt.subplots_adjust(left=0.08, right=0.78, bottom=0.32, top=0.90)

    ax.set_xlabel("x [m]")
    ax.set_ylabel("y [m]")
    ax.grid(True)
    ax.set_xlim(0, 1.45)
    ax.set_ylim(-0.06, +0.06)

    # plaques + diaphragme
    ax.hlines([+d1/2, -d1/2], xmin=0, xmax=L1, color="black")
    ax.hlines([+d2/2, -d2/2], xmin=L2, xmax=L3, color="black")
    ax.vlines(L4, ymin=+y_aperture, ymax=0.2, color="black")
    ax.vlines(L4, ymin=-0.2, ymax=-y_aperture, color="black")

    # tracé initial
    x, y, y_final, V2_used, t_flight = compute_trajectory(Vacc0, V10, V20, dev2_on0, z_sur_m_default)
    (line,) = ax.plot(x, y, lw=2)
    diaphragm_pt, = ax.plot([L4], [y_final], marker="o", markersize=8)

    passed = abs(y_final) <= y_aperture
    line.set_color("green" if passed else "red")
    diaphragm_pt.set_color("green" if passed else "red")

    title = ax.set_title(
        f"Trajectoire — V1={V10:.1f}V | Vacc={Vacc0:.0f}V | m/z={mz0:.2f} u/e | DEV2={'ON' if dev2_on0 else 'OFF'} (V2={V2_used:.0f}V)"
    )
    txt = ax.text(
    0.02, 0.95,
    f"Déviation finale (x=L4) : {y_final*1000:.2f} mm | Temps de vol : {t_flight*1e6:.2f} µs",
    transform=ax.transAxes, va="top"
    )


    # sliders (4 sliders empilés)
    ax_v1 = plt.axes([0.08, 0.22, 0.62, 0.03])
    s_v1 = Slider(ax_v1, "V1 [V]", -200, 200, valinit=V10, valstep=0.5)

    ax_v2 = plt.axes([0.08, 0.17, 0.62, 0.03])
    s_v2 = Slider(ax_v2, "V2 [V]", -20000, 20000, valinit=V20, valstep=50)

    ax_vacc = plt.axes([0.08, 0.12, 0.62, 0.03])
    s_vacc = Slider(ax_vacc, "Vacc [V]", 100, 5000, valinit=Vacc0, valstep=10)

    ax_mz = plt.axes([0.08, 0.07, 0.62, 0.03])
    s_mz = Slider(ax_mz, "m/z [u/e]", 0.2, 200.0, valinit=mz0, valstep=0.1)

    # Activation ou non de DEV2
    ax_check = plt.axes([0.82, 0.62, 0.15, 0.15])
    check = CheckButtons(ax_check, ["DEV2 ON"], [dev2_on0])

    # reset
    ax_btn = plt.axes([0.82, 0.52, 0.15, 0.06])
    btn_reset = Button(ax_btn, "Reset")

    def update(_=None):
        Vacc = float(s_vacc.val)
        V1 = float(s_v1.val)
        V2 = float(s_v2.val)
        mz = float(s_mz.val)
        dev2_on = bool(check.get_status()[0])

        z_sur_m = e_over_amu / mz  # q/m = (e/amu)/(m/z)

        x_new, y_new, y_final_new, V2_used_new, t_flight_new = compute_trajectory(
        Vacc, V1, V2, dev2_on, z_sur_m
        )


        passed_new = abs(y_final_new) <= y_aperture

        line.set_data(x_new, y_new)
        diaphragm_pt.set_data([L4], [y_final_new])

        line.set_color("green" if passed_new else "red")
        diaphragm_pt.set_color("green" if passed_new else "red")

        txt.set_text(
            f"Déviation finale (x=L4) : {y_final_new*1000:.2f} mm | Temps de vol : {t_flight_new*1e6:.2f} µs"
        )

        title.set_text(
            f"Trajectoire — V1={V1:.1f}V | Vacc={Vacc:.0f}V | m/z={mz:.2f} u/e | DEV2={'ON' if dev2_on else 'OFF'} (V2={V2_used_new:.0f}V)"
        )
        fig.canvas.draw_idle()

    def reset(_event):
        s_v1.reset()
        s_v2.reset()
        s_vacc.reset()
        s_mz.reset()
        if check.get_status()[0] != dev2_on0:
            check.set_active(0)
        update()

    s_v1.on_changed(update)
    s_v2.on_changed(update)
    s_vacc.on_changed(update)
    s_mz.on_changed(update)
    check.on_clicked(update)
    btn_reset.on_clicked(reset)

    plt.show()


if __name__ == "__main__":
    main()
