import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import cr_mech_coli as crm
from cr_mech_coli.plotting import COLOR2, COLOR3, COLOR4, COLOR5
import scipy as sp
from pathlib import Path
from glob import glob
import string


def delayed_growth(t, x0, growth_rate):
    x = np.array(t < 0.0)
    return x * x0 + ~x * x0 * np.exp(t * growth_rate)


if __name__ == "__main__":
    filenames = list(sorted(glob("cr_mech_coli/data/crm_fit/mie_all/masks/*.csv")))

    pixel_per_micron = (15.0,)
    minutes_per_frame = (20 / 8,)

    out_path = Path("figures/crm_estimate_params/")
    out_path.mkdir(parents=True, exist_ok=True)

    n_vertices = 12

    masks = [np.loadtxt(f, delimiter=",", converters=float) for f in filenames]
    results = [crm.extract_positions(m, n_vertices) for m in masks]
    inds = [r[3] for r in results]
    rod_lengths = np.array([r[1][np.argsort(i)] for r, i in zip(results, inds)])

    t = [int(f.split("/")[-1].split(".csv")[0].split("-")[0]) for f in filenames]
    t = np.array(t, dtype=float) - np.min(t).astype(float)
    y = np.mean(rod_lengths, axis=1)
    yerr = np.std(rod_lengths, axis=1)

    if pixel_per_micron is not None:
        y /= pixel_per_micron
        yerr /= pixel_per_micron
    if minutes_per_frame is not None:
        t *= minutes_per_frame

    # Prepare Figure
    crm.plotting.set_mpl_rc_params()
    fig = plt.figure(figsize=(24, 16))

    gs0 = mpl.gridspec.GridSpec(
        2,
        1,
        left=0,
        right=1,
        bottom=0,
        top=1,
    )
    fig1 = fig.add_subfigure(gs0[0])
    fig2 = fig.add_subfigure(gs0[1])

    gs_lower = mpl.gridspec.GridSpec(
        1,
        2,
        left=0,
        right=1,
        bottom=0,
        top=1,
        wspace=0.0,
        width_ratios=(0.28, 0.36 * 2),
    )
    fig3 = fig2.add_subfigure(gs_lower[0])
    fig4 = fig2.add_subfigure(gs_lower[1])

    gs1 = mpl.gridspec.GridSpec(1, 2, left=0, right=1, bottom=0.03, top=1, wspace=0.015)
    gs2 = mpl.gridspec.GridSpec(
        1,
        2,
        left=0.06,
        right=0.94,
        bottom=0.1,
        top=0.91,
        wspace=0.20,
        hspace=0.03,
    )

    # Load original image and plot
    ax11 = fig1.add_subplot(gs1[0])

    fname = filenames[0]
    img_name = fname.replace("masks", "images")
    img_name = img_name.replace("-markers.csv", ".png")
    img1 = plt.imread(img_name)
    ax11.imshow(img1, aspect="auto")
    ax11.set_axis_off()

    ax12 = fig1.add_subplot(gs1[1])
    m = masks[0].astype(int)
    counters = np.unique(m)
    counters = counters[counters != 0]
    color_mapping = {i: crm.counter_to_color(i) for i in counters}
    new_mask = np.zeros((*m.shape, 3), dtype=np.uint8)

    for counter, color in color_mapping.items():
        new_mask[m == counter] = color

    ax12.imshow(new_mask, aspect="auto")
    ax12.set_axis_off()

    ax21 = fig3.add_subplot()
    fig3.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax21.set_axis_off()
    img = plt.imread("figures/crm_fit-data-progression.png")
    ax21.imshow(img, aspect="auto")

    # TODO plot overview figure here

    growth_curve = delayed_growth
    p0 = (y[0], np.log(y[-1] / y[0]))

    ax22 = fig4.add_subplot(gs2[0])
    crm.plotting.configure_ax(ax22)

    parameters = []
    covariances = []
    crm.plotting.configure_ax(ax22)
    for i in range(rod_lengths.shape[1]):
        yi = rod_lengths[:, i]
        if pixel_per_micron is not None:
            yi /= pixel_per_micron
        p0 = (yi[0], np.log(yi[-1] / yi[0]))

        popt, pcov = sp.optimize.curve_fit(
            growth_curve,
            t,
            yi,
            p0=p0,
        )
        parameters.append(popt)
        covariances.append(pcov)
        ax22.plot(t, yi, color=COLOR3, label="Data")
        ax22.plot(
            t,
            growth_curve(t, *popt),
            label="Fit",
            color=COLOR5,
            linestyle="--",
        )

    ax22.set_xlabel("Time [min]")

    handles, labels = ax22.get_legend_handles_labels()
    ax22.legend(
        handles[:2],
        labels[:2],
        loc="upper center",
        bbox_to_anchor=(0.5, 1.10),
        ncol=2,
        frameon=False,
    )

    growth_rates = [p[1] for p in parameters]
    growth_rates_uncert = [p[1][1] ** 0.5 for p in covariances]

    ax23 = fig4.add_subplot(gs2[1])
    crm.plotting.configure_ax(ax23)

    ax23.hist(growth_rates, facecolor=COLOR3, edgecolor=COLOR2)
    xmin = np.min(growth_rates)
    xmax23 = np.max(growth_rates)
    middle = (xmin + xmax23) / 2
    dx = xmax23 - xmin
    xticks = [xmin + 0.05 * dx, middle, xmax23 - 0.05 * dx]
    ax23.set_xticks(xticks, labels=[f"{x:f}" for x in xticks])
    ax23.set_xlabel("Growth Rate [1/min]")
    ax23.set_ylabel("Count")

    np.savetxt(out_path / "growth_rates.csv", growth_rates, delimiter=",")

    yticks = ax23.get_yticks()
    yticks = list(filter(lambda x: int(x) == x, yticks))
    ax23.set_yticks(yticks, minor=False)

    for i, ax in enumerate([ax11, ax12, ax21, ax22, ax23]):
        ax.text(
            0.03 if i < 3 else 0.02 if i == 3 else 0.49,
            0.97,
            string.ascii_uppercase[i],
            fontsize=40,
            fontweight="semibold",
            fontfamily="serif",
            va="top",
            horizontalalignment="left",
            transform=ax.transAxes if i < 3 else fig4.transSubfigure,
            color="white" if i < 3 else "k",
        )

    fig.savefig(out_path / "combined.pdf")
