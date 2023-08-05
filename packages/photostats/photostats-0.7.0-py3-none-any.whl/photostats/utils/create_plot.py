"""Create a plot and save to disk."""

import matplotlib.pyplot as plt  # type: ignore


def create_plot(group_names: list, group_data: list, x_label: str = "", y_label: str = "", title: str = "",
                graph_path: str = "", graph_filename: str = ""):
    plt.style.use('fivethirtyeight')
    plt.rcParams.update({'figure.autolayout': True})
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.bar(group_names, group_data)
    x_labels = ax.get_xticklabels()
    plt.setp(x_labels, rotation=30, horizontalalignment='right')
    ax.set(xlabel=x_label, ylabel=y_label, title=title)
    ax.title.set(y=1.05)
    fig.savefig(f"{graph_path}/{graph_filename}", transparent=False, dpi=80, bbox_inches="tight")
    # plt.show()
