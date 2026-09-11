import matplotlib.pyplot as plt
import string

if __name__ == "__main__":
    s = 0.03
    aspect = 1.056
    fig, axs = plt.subplots(2, 3, figsize=(24, 16 * aspect * (1 + s) / (1 + 2 * s)))

    imgs = [
        "figures/crm_amir/progressions/step4-000010.png",
        "figures/crm_amir/progressions/step4-000017.png",
        "figures/crm_amir/progressions/step4-000034.png",
        "figures/crm_amir/result-full/0000000000.png",
        "figures/crm_amir/result-full/0000000001.png",
        "figures/crm_amir/result-full/0000000002.png",
    ]

    for i, ax, label, img in zip(range(6), axs.flatten(), string.ascii_uppercase, imgs):
        ax.text(
            0.03,
            0.03 if i < 3 else 0.97,
            label,
            fontsize=40,
            fontweight="semibold",
            fontfamily="serif",
            va="bottom" if i < 3 else "top",
            horizontalalignment="left",
            transform=ax.transAxes,
            color="white" if i < 3 else "k",
        )
        ax.set_axis_off()
        img = plt.imread(img)
        ax.imshow(img, aspect="auto")

    fig.subplots_adjust(left=0, right=1, bottom=0, top=1, wspace=s, hspace=s)
    fig.savefig("figures/crm_amir/progression.pdf")
