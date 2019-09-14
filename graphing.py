# Final graphing results
import matplotlib.pyplot as plt
import user_input as usin

def graph_prelim(data, labels, colors, title):
    fig = plt.figure()
    # Create figure
    ax = fig.add_subplot(1, 1, 1)

    for data, color, label in zip(data, colors, labels):
        x, y = data
        ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=30, label=label)

    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Get and add title
    plt.title(title)

    # Save graph
    plt.savefig('{}.png'.format(title))

def graph_rpt(data, labels, colors, title):
    fig = plt.figure()

    for data, color, label  in zip(data, colors, labels):
        x, y, xerr, yerr = data
        plt.errorbar(x, y, xerr=xerr, yerr=yerr, color=color, label=label)

    # Create figure
    ax = fig.add_subplot(1, 1, 1)
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.75, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title(title)
    
    # Save graph
    plt.savefig('{}.png'.format(title))
