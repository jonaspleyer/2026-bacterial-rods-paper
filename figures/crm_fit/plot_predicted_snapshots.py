import matplotlib.pyplot as plt
import string

if __name__ == "__main__":
    img1 = plt.imread("figures/crm_fit/morse_partial/snapshots/predicted-006562.png")
    img2 = plt.imread("figures/crm_fit/morse_partial/celldiffs/diff-006667.png")

    width = 24
    height = width / (img1.shape[1] / img1.shape[0] + img2.shape[1] / img2.shape[0])
    print(width, height)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(width * 1.01, height))

    ax1.imshow(img1)
    ax2.imshow(1 - img2, cmap="Grays")

    ax1.set_axis_off()
    ax2.set_axis_off()

    for i, ax in enumerate([ax1, ax2]):
        ax.text(
            0.03,
            0.97,
            string.ascii_uppercase[i],
            fontsize=40,
            fontweight="semibold",
            fontfamily="serif",
            va="top",
            horizontalalignment="left",
            transform=ax.transAxes,
            color="white",
        )

    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=0.02)
    fig.savefig("figures/crm_fit/morse_partial/predicted-snapshots.pdf")
