import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import prettierplot.style as style
import prettierplot.util as util


class PrettierPlot:
    """
    Documentation:
        Description:
            PrettierPlot creates high_quality data visualizations quickly and easily.
            initialization of this class creates a plotting object of a chosen size and
            orientation. once the figure is initialized, the method make_canvas can be
            called to create the figure axis or chosen number of axes. multiple axes can
            be plotted on a single figure, or the position variable can be utilized to
            create a subplot arrangement.
    """

    from .cat import (
        bar_v,
        bar_h,
        box_plot_v,
        box_plot_h,
        stacked_bar_h,
        tree_map,
    )
    from .data import titanic
    from .eval import (
        prob_plot,
        corr_heatmap,
        corr_heatmap_target,
        roc_curve_plot,
        decision_region,
        # residual_plot,
    )
    from .facet import (
        facet_cat,
        facet_two_cat_bar,
        facet_cat_num_hist,
        facet_two_cat_point,
        facet_cat_num_scatter,
    )
    from .line import line, multi_line
    from .num import (
        scatter_2d,
        scatter_2d_hue,
        dist_plot,
        kde_plot,
        reg_plot,
        pair_plot,
        pair_plot_custom,
        hist,
    )

    # foundation
    def __init__(self, chart_scale=15, plot_orientation=None):
        """
        Documentation:
            Description:
                initialize PrettierPlot and dynamically set chart size.
            Parameters:
                chart_scale : float or int, default=15
                    chart proportionality control. determines relative size of figure size, axis labels,
                    chart title, tick labels, tick marks.
                plot_orientation : string, default=None
                    default value produces a plot that is wider than it is tall. specifying 'tall' will
                    produce a taller, less wide plot. 'square' produces a square plot. 'wide' produces a
                    plot that is much wide than it is tall.
        """
        self.chart_scale = chart_scale
        self.plot_orientation = plot_orientation
        self.fig = plt.figure(facecolor="white")

        # set graphic style
        # plt.rcParams['figure.facecolor'] = 'white'
        sns.set(rc=style.rc_grey)

        # dynamically set chart width and height parameters
        if plot_orientation == "tall":
            chart_width = self.chart_scale * 0.7
            chart_height = self.chart_scale * 1.2
        elif plot_orientation == "square":
            chart_width = self.chart_scale
            chart_height = self.chart_scale * 0.8
        elif plot_orientation == "wide_narrow":
            chart_width = self.chart_scale * 2.0
            chart_height = self.chart_scale * 0.42
        elif plot_orientation == "wide_standard":
            chart_width = self.chart_scale * 1.6
            chart_height = self.chart_scale * 0.75
        else:
            chart_width = self.chart_scale
            chart_height = self.chart_scale * 0.5
        self.fig.set_figheight(chart_height)
        self.fig.set_figwidth(chart_width)

    def make_canvas(self, title="", x_label="", x_shift=0.0, y_label="", y_shift=0.8, position=111, nrows=None,
                    ncols=None, index=None, sharex=None, sharey=None, title_scale=1.0):
        """
        Documentation:
            Description:
                create axes object. add descriptive attributes such as titles and axis labels,
                set font size and font color. remove grid. remove top and right spine.
            Parameters:
                title : string, default='' (blank)
                    the title for the chart.
                x_label : string, default='' (blank)
                    x_axis label.
                x_shift : float, default=0.8
                    controls position of x_axis label. higher values move label right along axis.
                    intent is to align with left of axis.
                y_label : string, default='' (blank)
                    y_axis label.
                y_shift : float, default=0.8
                    controls position of y_axis label. higher values move label higher along axis.
                    intent is to align with top of axis.
                position : int (nrows, ncols, index), default=111
                    determine subplot position of plot.
                nrows : int, default=None
                    number of rows in subplot grid.
                ncols : int, default=None
                    number of columns in subplot grid.
                sharex : bool or none, default=None
                    conditional controlling whether to share x_axis across all subplots in a column.
                sharey : bool or none, default=None
                    conditional controlling whether to share y_axis across all subplots in a row.
                title_scale : float, default=1.0
                    controls the scaling up (higher value) and scaling down (lower value) of the size of
                    the main chart title, the x_axis title and the y_axis title.
            returns
                ax : axes object
                    contain figure elements
        """
        # # set graphic style
        # plt.rcParams['figure.facecolor'] = 'white'
        # sns.set(rc = style.rc_grey)

        # add subplot
        if index is not None:
            ax = self.fig.add_subplot(nrows, ncols, index, sharex=sharex, sharey=sharey)
        else:
            ax = self.fig.add_subplot(position)

        ## add title
        # dynamically determine font size based on string length
        # scale by title_scale
        if len(title) >= 45:
            font_adjust = 1.0 * title_scale
        elif len(title) >= 30 and len(title) < 45:
            font_adjust = 1.25 * title_scale
        elif len(title) >= 20 and len(title) < 30:
            font_adjust = 1.5 * title_scale
        else:
            font_adjust = 1.75 * title_scale

        # set title
        ax.set_title(
            title,
            fontsize=(2.0 * self.chart_scale) * title_scale
            if position == 111
            else font_adjust * self.chart_scale,
            color=style.style_grey,
            loc="left",
            pad=0.4 * self.chart_scale,
        )

        # remove grid line and right/top spines
        ax.grid(False)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

        # add axis labels
        plt.xlabel(
            x_label,
            fontsize=1.667 * self.chart_scale * title_scale,
            labelpad=1.667 * self.chart_scale,
            position=(x_shift, 0.5),
            horizontalalignment="left",
        )
        plt.ylabel(
            y_label,
            fontsize=1.667 * self.chart_scale * title_scale,
            labelpad=1.667 * self.chart_scale,
            position=(1.0, y_shift),
            horizontalalignment="left",
        )

        return ax
