import matplotlib.pyplot as plt
import string

if __name__ == "__main__":
    img1 = plt.imread("figures/crm_divide/masks_diff/000000.png")
    img2 = plt.imread("figures/crm_divide/masks_diff/000010.png")
    img3 = plt.imread("figures/crm_divide/masks_diff/000020.png")

    s = 0.01
    width = 24
    height = width / (img1.shape[1] / img1.shape[0]) / 3
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(width * (1 + 2 * s), height))

    ax1.imshow(1 - img1, cmap="Grays")
    ax2.imshow(1 - img2, cmap="Grays")
    ax3.imshow(1 - img3, cmap="Grays")

    ax1.set_axis_off()
    ax2.set_axis_off()
    ax3.set_axis_off()

    for i, ax in enumerate([ax1, ax2, ax3]):
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

    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=2 * s)
    fig.savefig("figures/crm_divide/masks-diff-progression.pdf")
