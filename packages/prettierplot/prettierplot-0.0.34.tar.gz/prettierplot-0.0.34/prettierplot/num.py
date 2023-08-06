import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

from scipy.stats import linregress

import prettierplot.style as style
import prettierplot.util as util

import textwrap


def scatter_2d(self, x, y, df=None, x_units="f", x_ticks=None, y_units="f", y_ticks=None, plot_buffer=True,
                        size=5, axis_limits=True, color=style.style_grey, facecolor="w", alpha=0.8,
                        x_rotate=None, ax=None):
    """
    Documentation:
        Description:
            create 2_dimensional scatter plot.
        Parameters:
            x : array or string
                either 1_dimensional array of values or a column name in a Pandas DataFrame.
            y : array or string
                either 1_dimensional array of values or a column name in a Pandas DataFrame.
            df : Pandas DataFrame, default=None
                dataset containing data to be plotted. can be any size - plotted columns will be
                chosen by columns names specified in x, y.
            x_units : string, default='f'
                determines units of x_axis tick labels. 'f' displays float. 'p' displays percentages,
                'd' displays dollars. repeat character (e.g 'ff' or 'ddd') for additional decimal places.
            x_ticks : array, default=None
                specify custom x_tick labels.
            y_units : string, default='f'
                determines units of x_axis tick labels. 'f' displays float. 'p' displays percentages,
                'd' displays dollars. repeat character (e.g 'ff' or 'ddd') for additional decimal places.
            y_ticks : array, default=None
                specify custom y_tick labels.
            plot_buffer : bool, default=True
                switch for determining whether dynamic plot buffer function is executed.
            size : int or float, default=5
                determines scatter dot size.
            axis_limits : bool, default=True
                switch for determining whether dynamic axis limit setting function is executed.
            color : string (color code of some sort), default=style.style_grey
                determine color of scatter dots
            facecolor : string (color code of some sort), default='w'
                determine face color of scatter dots.
            alpha : float, default=0.8
                controls transparency of objects. accepts value between 0.0 and 1.0.
            x_rotate : int, default=None
                rotates x_axis tick mark labels x degrees.
            ax : axes object, default=None
                axis on which to place visual.
    """
    # if a Pandas DataFrame is passed to function, create x, y arrays using columns names passed into function.
    if df is not None:
        x = df[x].values.reshape(-1, 1)
        y = df[y].values.reshape(-1, 1)
    # else reshape arrays.
    else:
        x = x.reshape(-1, 1)
        y = y.reshape(-1, 1)

    # generate color

    # plot 2_d scatter.
    plt.scatter(
        x=x,
        y=y * 100 if "p" in y_units else y,
        color=color,
        s=size * self.chart_scale,
        alpha=alpha,
        facecolor=facecolor,
        linewidth=0.167 * self.chart_scale,
    )

    # dynamically set axis lower / upper limits.
    if axis_limits:
        x_min, x_max, y_min, y_max = util.util_set_axes(x=x, y=y)
        plt.axis([x_min, x_max, y_min, y_max])

    # vreate smaller buffer around plot area to prevent cutting off elements.
    if plot_buffer:
        util.util_plot_buffer(ax=ax, x=0.02, y=0.02)

    # tick label control
    if x_ticks is not None:
        ax.set_xticks(x_ticks)

    if y_ticks is not None:
        ax.set_yticks(y_ticks)

    # format x and y ticklabels
    ax.set_yticklabels(
        ax.get_yticklabels() * 100 if "p" in y_units else ax.get_yticklabels(),
        rotation=0,
        fontsize=1.0 * self.chart_scale,
        color=style.style_grey,
    )

    ax.set_xticklabels(
        ax.get_xticklabels() * 100 if "p" in y_units else ax.get_xticklabels(),
        rotation=0,
        fontsize=1.0 * self.chart_scale,
        color=style.style_grey,
    )

    # use label formatter utility function to customize chart labels
    util.util_label_formatter(ax=ax, x_units=x_units, y_units=y_units, x_rotate=x_rotate)

def scatter_2d_hue(self, x, y, target, label, df=None, x_units="f", x_ticks=None, y_units="f", y_ticks=None,
                        plot_buffer=True, size=10, axis_limits=True, color=style.style_grey, facecolor="w",
                        bbox=(1.2, 0.9), color_map="viridis", alpha=0.8, x_rotate=None, ax=None):
    """
    Documentation:
        Description:
            create 2_dimensional scatter plot with a third dimension represented as a color hue in the
            scatter dots.
        Parameters:
            x : array or string
                either 1_dimensional array of values or a column name in a Pandas DataFrame.
            y : array or string
                either 1_dimensional array of values or a column name in a Pandas DataFrame.
            target : array or string
                either 1_dimensional array of values or a column name in a Pandas DataFrame.
            label : list
                list of labels describing hue.
            df : Pandas DataFrame, default=None
                dataset containing data to be plotted. can be any size - plotted columns will be
                chosen by columns names specified in x, y.
            x_units : string, default='d'
                determines units of x_axis tick labels. 'f' displays float. 'p' displays percentages,
                'd' displays dollars. repeat character (e.g 'ff' or 'ddd') for additional decimal places.
            x_ticks : array, default=None
                specify custom x_tick labels.
            y_units : string, default='d'
                determines units of x_axis tick labels. 'f' displays float. 'p' displays percentages,
                'd' displays dollars. repeat character (e.g 'ff' or 'ddd') for additional decimal places.
            y_ticks : array, default=None
                specify custom y_tick labels.
            plot_buffer : bool, default=True
                switch for determining whether dynamic plot buffer function is executed.
            size : int or float, default=10
                determines scatter dot size.
            axis_limits : bool, default=True
                switch for determining whether dynamic axis limit setting function is executed.
            color : string (color code of some sort), default=style.style_grey
                determine color of scatter dots.
            facecolor : string (color code of some sort), default='w'
                determine face color of scatter dots.
            bbox : tuple of floats, default=(1.2, 0.9)
                coordinates for determining legend position.
            color_map : string specifying built_in matplotlib colormap, default="viridis"
                colormap from which to draw plot colors.
            alpha : float, default=0.8
                controls transparency of objects. accepts value between 0.0 and 1.0.
            x_rotate : int, default=None
                rotates x_axis tick mark labels x degrees.
            ax : axes object, default=None
                axis on which to place visual.
    """
    # if a Pandas DataFrame is passed to function, create x, y and target arrays using columns names
    # passed into function. also create x, which is a matrix containing the x, y and target columns.
    if df is not None:
        x = df[[x, y, target]].values
        x = df[x].values
        y = df[y].values
        target = df[target].values
    # concatenate the x, y and target arrays.
    else:
        x = np.c_[x, y, target]

    # unique target values.
    target_ids = np.unique(x[:, 2])

    # generate color list
    color_list = style.color_gen(name=color_map, num=len(target_ids))

    # loop through sets of target values, labels and colors to create 2_d scatter with hue.
    for target_id, target_name, color in zip(target_ids, label, color_list):
        plt.scatter(
            x=x[x[:, 2] == target_id][:, 0],
            y=x[x[:, 2] == target_id][:, 1],
            color=color,
            label=target_name,
            s=size * self.chart_scale,
            alpha=alpha,
            facecolor="w",
            linewidth=0.234 * self.chart_scale,
        )

    # add legend to figure.
    if label is not None:
        plt.legend(
            loc="upper right",
            bbox_to_anchor=bbox,
            ncol=1,
            frameon=True,
            fontsize=1.1 * self.chart_scale,
        )

    # dynamically set axis lower / upper limits.
    if axis_limits:
        x_min, x_max, y_min, y_max = util.util_set_axes(x=x, y=y)
        plt.axis([x_min, x_max, y_min, y_max])

    # create smaller buffer around plot area to prevent cutting off elements.
    if plot_buffer:
        util.util_plot_buffer(ax=ax, x=0.02, y=0.02)

    # tick label control
    if x_ticks is not None:
        ax.set_xticks(x_ticks)

    if y_ticks is not None:
        ax.set_yticks(y_ticks)

    # format x and y ticklabels
    ax.set_yticklabels(
        ax.get_yticklabels() * 100 if "p" in y_units else ax.get_yticklabels(),
        rotation=0,
        fontsize=1.0 * self.chart_scale,
        color=style.style_grey,
    )

    ax.set_xticklabels(
        ax.get_xticklabels() * 100 if "p" in y_units else ax.get_xticklabels(),
        rotation=0,
        fontsize=1.0 * self.chart_scale,
        color=style.style_grey,
    )

    # use label formatter utility function to customize chart labels
    util.util_label_formatter(ax=ax, x_units=x_units, y_units=y_units, x_rotate=x_rotate)

def dist_plot(self, x, color, x_units="f", y_units="f", fit=None, kde=False, x_rotate=None, alpha=0.8,
                    bbox=(1.2, 0.9), legend_labels=None, color_map="viridis", ax=None):
    """
    Documentation:
        Description:
            creates distribution plot for number variables, showing counts of a single
            variable. also overlays a kernel density estimation curve.
        Parameters:
            x : array
                data to be plotted.
            color : string (some sort of color code)
                determines color of bars, kde lines.
            x_units : string, default='f'
                determines units of x_axis tick labels. 'f' displays float. 'p' displays percentages,
                'd' displays dollars. repeat character (e.g 'ff' or 'ddd') for additional decimal places.
            y_units : string, default='f'
                determines units of x_axis tick labels. 'f' displays float. 'p' displays percentages,
                'd' displays dollars. repeat character (e.g 'ff' or 'ddd') for additional decimal places.
            fit : random variabe object, default=None
                allows for the addition of another curve. utilizing 'norm' overlays a normal distribution
                over the distribution bar chart. useful for seeing how well, or not, the distribution tracks
                with a normal distrbution.
            kde : boolean, default=False
                plot kernel density over plot.
            x_rotate : int, default=None
                rotates x_axis tick mark labels x degrees.
            bbox : tuple of floats, default=(1.2, 0.9)
                coordinates for determining legend position.
            legend_labels : list, default=None
                custom legend labels.
            color_map : string specifying built_in matplotlib colormap, default="viridis"
                colormap from which to draw plot colors.
            ax : axes object, default=None
                axis on which to place visual.
    """
    # create distribution plot with an optional fit curve
    g = sns.distplot(
        a=x,
        kde=kde,
        color=color,
        axlabel=False,
        fit=fit,
        kde_kws={"lw": 0.2 * self.chart_scale},
        hist_kws={"alpha": alpha},
        ax=ax,
    )

    # tick label font size
    ax.tick_params(axis="both", colors=style.style_grey, labelsize=1.2 * self.chart_scale)

    # format x and y ticklabels
    ax.set_yticklabels(
        ax.get_yticklabels() * 100 if "p" in y_units else ax.get_yticklabels(),
        rotation=0,
        fontsize=1.1 * self.chart_scale,
        color=style.style_grey,
    )

    ax.set_xticklabels(
        ax.get_xticklabels() * 100 if "p" in y_units else ax.get_xticklabels(),
        rotation=0,
        fontsize=1.1 * self.chart_scale,
        color=style.style_grey,
    )

    # use label formatter utility function to customize chart labels
    util.util_label_formatter(
        ax=ax, x_units=x_units, y_units=y_units, x_rotate=x_rotate
    )


    ## create custom legend
    if legend_labels is None:
        legend_labels = legend_labels
    else:
        legend_labels = np.array(legend_labels)

        # generate colors
        color_list = style.color_gen(color_map, num=len(legend_labels))

        label_color = {}
        for ix, i in enumerate(legend_labels):
            label_color[i] = color_list[ix]

        # create patches
        patches = [Patch(color=v, label=k, alpha=alpha) for k, v in label_color.items()]

        # draw legend
        leg = plt.legend(
            handles=patches,
            fontsize=1.0 * self.chart_scale,
            loc="upper right",
            markerscale=0.5 * self.chart_scale,
            ncol=1,
            bbox_to_anchor=bbox,
        )

        # label font color
        for text in leg.get_texts():
            plt.setp(text, color="grey")

def kde_plot(self, x, color, y_units="f", x_units="f", shade=False, line_width=0.25, bw=1.0, ax=None):
    """
    Documentation:
        Description:
            create kernel density curve for a feature.
        Parameters:
            x : array
                data to be plotted.
            color : string (some sort of color code)
                determines color of kde lines.
            x_units : string, default='f'
                determines units of x_axis tick labels. 'f' displays float. 'p' displays percentages,
                'd' displays dollars. repeat character (e.g 'ff' or 'ddd') for additional decimal places.
            y_units : string, default='f'
                determines units of x_axis tick labels. 'f' displays float. 'p' displays percentages,
                'd' displays dollars. repeat character (e.g 'ff' or 'ddd') for additional decimal places.
            shade : boolean, default=True
                shade area under KDe curve
            line_width : float or int, default= 0.5
                controls thickness of kde lines
            bw : float, default=1.0
                scaling factor for the KDE curve
            ax : axes object, default=None
                axis on which to place visual.
    """
    # create kernel density estimation line
    g = sns.kdeplot(
        data=x,
        shade=shade,
        color=color,
        legend=None,
        linewidth=self.chart_scale * line_width,
        ax=ax
    )

    # format x and y ticklabels
    ax.set_yticklabels(
        ax.get_yticklabels() * 100 if "p" in y_units else ax.get_yticklabels(),
        rotation=0,
        fontsize=1.1 * self.chart_scale,
        color=style.style_grey,
    )

    ax.set_xticklabels(
        ax.get_xticklabels() * 100 if "p" in y_units else ax.get_xticklabels(),
        rotation=0,
        fontsize=1.1 * self.chart_scale,
        color=style.style_grey,
    )
    # use label formatter utility function to customize chart labels
    util.util_label_formatter(ax=ax, x_units=x_units, y_units=y_units)

def reg_plot(self, x, y, data, dot_color=style.style_grey, dot_size=2.0, line_color=style.style_blue, line_width = 0.3,
            x_jitter=None, x_units="f", y_units="f", x_rotate=None, alpha=0.3, ax=None):
    """
    Documentation:
        Description:
            create scatter plot with regression line.
        Parameters:
            x : string
                name of independent variable in dataframe. represents a category
            y : string
                name of number target variable.
            data : Pandas DataFrame
                Pandas DataFrame including both indepedent variable and target variable.
            dot_color : string
                determines color of dots.
            dot_size : float or int
                determines size of dots
            line_color : string
                determines color of regression line.
            line_width : float or int
                determines width of regression line.
            x_jitter : float, default=None
                optional paramter for randomly displacing dots along the x_axis to enable easier visibility
                of dots.
            label_rotate : float or int, default=45
                degrees by which the xtick labels are rotated.
            x_units : string, default='f'
                determines units of x_axis tick labels. 'f' displays float. 'p' displays percentages,
                'd' displays dollars. repeat character (e.g 'ff' or 'ddd') for additional decimal places.
            y_units : string, default='f'
                determines units of y_axis tick labels. 'f' displays float. 'p' displays percentages,
                'd' displays dollars. repeat character (e.g 'ff' or 'ddd') for additional decimal places.
            x_rotate : int, default=None
                rotates x_axis tick mark labels x degrees.
            alpha : float, default=0.3
                controls transparency of objects. accepts value between 0.0 and 1.0.
            ax : axes object, default=None
                axis on which to place visual.
    """
    # create regression plot.
    g = sns.regplot(
        x=x,
        y=y,
        data=data,
        x_jitter=x_jitter,
        scatter_kws={
            "alpha": alpha,
            "color": dot_color,
            "s": dot_size * self.chart_scale,
            },
        line_kws={
            "color": line_color,
            "linewidth": self.chart_scale * line_width,
            },
        ax=ax,
    ).set(xlabel=None, ylabel=None)

    # format x and y ticklabels
    ax.set_yticklabels(
        ax.get_yticklabels() * 100 if "p" in y_units else ax.get_yticklabels(),
        rotation=0,
        fontsize=1.1 * self.chart_scale,
        color=style.style_grey,
    )

    ax.set_xticklabels(
        ax.get_xticklabels() * 100 if "p" in y_units else ax.get_xticklabels(),
        rotation=0,
        fontsize=1.1 * self.chart_scale,
        color=style.style_grey,
    )

    # use label formatter utility function to customize chart labels
    util.util_label_formatter(
        ax=ax, x_units=x_units, y_units=y_units, x_rotate=x_rotate
    )

def pair_plot_custom(self, df, columns=None, color=style.style_blue, gradient_col=None):
    """
    Documentation:
        Description:
            create pair plot that produces a grid of scatter plots for all unique pairs of
            number features and a series of kde or histogram plots along the diagonal.
        Parameters:
            df : Pandas DataFrame
                Pandas DataFrame containing data of interest.
            columns : list, default=None
                list of strings describing columns in Pandas DataFrame to be visualized.
            color : string, default=style.style_blue
                color to serve as high end of gradient when gradient_col is specified.
            gradient_col : string, default=None
                introduce third dimension to scatter plots through a color hue that differentiates
                dots based on the target's value.
            diag_kind : string, default='auto.
                type of plot created along diagonal.
    """
    # custom plot formatting settings for this particular chart.
    with plt.rc_context(
        {
            "axes.titlesize": 3.5 * self.chart_scale,
            "axes.labelsize": 0.9 * self.chart_scale,  # axis title font size
            "xtick.labelsize": 0.8 * self.chart_scale,
            "xtick.major.size": 0.5 * self.chart_scale,
            "xtick.major.width": 0.05 * self.chart_scale,
            "xtick.color": style.style_grey,
            "ytick.labelsize": 0.8 * self.chart_scale,
            "ytick.major.size": 0.5 * self.chart_scale,
            "ytick.major.width": 0.05 * self.chart_scale,
            "ytick.color": style.style_grey,
            "figure.facecolor": style.style_white,
            "axes.facecolor": style.style_white,
            "axes.spines.left": False,
            "axes.spines.bottom": False,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": style.style_grey,
            "axes.grid": False,
        }
    ):

        # limit to columns of interest if provided
        if columns is not None:
            df = df[columns]

        df = util.number_coerce(df, columns=columns)

        # create figure and axes
        fig, axes = plt.subplots(
            ncols=len(df.columns),
            nrows=len(df.columns),
            constrained_layout=True,
            figsize=(1.2 * self.chart_scale, 0.9 * self.chart_scale),
        )

        # unpack axes
        for (i, j), ax in np.ndenumerate(axes):
            # turn of axes on upper triangle
            # if i < j:
            #     plt.setp(ax.get_xticklabels(), visible=False)
            #     plt.setp(ax.get_yticklabels(), visible=False)
            # set diagonal plots as kde plots
            if i == j:
                sns.kdeplot(df.iloc[:, i], ax=ax, legend=False, shade=True, color=color)
            # set lower triangle plots as scatter plots
            else:
                sns.scatterplot(
                    x=df.iloc[:, j],
                    y=df.iloc[:, i],
                    hue=gradient_col if gradient_col is None else df[gradient_col],
                    data=df,
                    palette=LinearSegmentedColormap.from_list(
                        name="", colors=["white", color]
                    ),
                    legend=False,
                    ax=ax,
                )
        plt.show()

def pair_plot(self, df, columns=None, target=None, diag_kind="auto", legend_labels=None, drop_na=True,
                    bbox=(2.0, 1.0), alpha=0.7, color_map="viridis"):
    """
    Documentation:
        Description:
            create pair plot that produces a grid of scatter plots for all unique pairs of
            number features and a series of kde or histogram plots along the diagonal.
        Parameters:
            df : Pandas DataFrame
                Pandas DataFrame containing data of interest.
            columns : list, default=None
                list of strings describing columns in Pandas DataFrame to be visualized.
            target : Pandas Series, default=None
                introduce third dimension to scatter plots through a color hue that differentiates
                dots based on the target's value.
            diag_kind : string, default='auto.
                type of plot created along diagonal.
            drop_na : boolean, default=True
                drop rows containing null values.
            legend_labels : list, default=None
                list containing strings of custom labels to display in legend.
            bbox : tuple of floats, default=None
                coordinates for determining legend position.
            alpha : float, default=0.7
                controls transparency of objects. accepts value between 0.0 and 1.0.
            color_map : string specifying built_in matplotlib colormap, default="viridis"
                colormap from which to draw plot colors.
    """
    # custom plot formatting settings for this particular chart.
    with plt.rc_context(
        {
            "axes.titlesize": 3.5 * self.chart_scale,
            "axes.labelsize": 1.5 * self.chart_scale,  # axis title font size
            "xtick.labelsize": 1.2 * self.chart_scale,
            "xtick.major.size": 0.5 * self.chart_scale,
            "xtick.major.width": 0.05 * self.chart_scale,
            "xtick.color": style.style_grey,
            "ytick.labelsize": 1.2 * self.chart_scale,
            "ytick.major.size": 0.5 * self.chart_scale,
            "ytick.major.width": 0.05 * self.chart_scale,
            "ytick.color": style.style_grey,
            "figure.facecolor": style.style_white,
            "axes.facecolor": style.style_white,
            "axes.spines.left": False,
            "axes.spines.bottom": False,
            "axes.edgecolor": style.style_grey,
            "axes.grid": False,
        }
    ):
        # # remove object columns
        # df = df.select_dtypes(exclude=[object])

        if drop_na:
            df = df.dropna()

        # limit to columns of interest if provided
        if columns is not None:
            df = df[columns]

        # merge df with target if target is provided
        if target is not None:
            df = df.merge(target, left_index=True, right_index=True)

        # create pair plot.
        g = sns.pairplot(
            data=df if target is None else df.dropna(),
            vars=df.columns
            if target is None
            else [x for x in df.columns if x is not target.name],
            hue=target if target is None else target.name,
            diag_kind=diag_kind,
            height=0.2 * self.chart_scale,
            plot_kws={
                "s": 2.0 * self.chart_scale,
                "edgecolor": None,
                "linewidth": 1,
                "alpha": alpha,
                "marker": "o",
                "facecolor": style.style_grey if target is None else None,
            },
            diag_kws={"facecolor": style.style_grey if target is None else None},
            palette=None
            if target is None
            else sns.color_palette(
                style.color_gen(color_map, num=len(np.unique(target)))
            ),
        )

        # plot formatting
        for ax in g.axes.flat:

            _ = ax.set_xlabel(
                    "\n".join(textwrap.wrap(str(ax.get_xlabel()).replace("_", " "), 12))
                , rotation=40, ha="right")
            _ = ax.set_ylabel(
                    "\n".join(textwrap.wrap(str(ax.get_ylabel()).replace("_", " "), 12))
                , rotation=40, ha="right")
            _ = ax.xaxis.labelpad = 20
            _ = ax.yaxis.labelpad = 40
            _ = ax.xaxis.label.set_color(style.style_grey)
            _ = ax.yaxis.label.set_color(style.style_grey)


            plt.xlabel(
                # 0,
                [
                    "\n".join(textwrap.wrap(str(i).replace("_", " "), 12))
                    for i in ax.get_xlabel()
                ],
                # ha="center",
            )
            plt.ylabel(
                # 0,
                [
                    "\n".join(textwrap.wrap(str(i).replace("_", " "), 12))
                    for i in ax.get_xlabel()
                ],
                # va="center_baseline",
            )



        plt.subplots_adjust(hspace=0.0, wspace=0.0)

        # add custom legend describing hue labels
        if target is not None:
            g._legend.remove()

            ## create custom legend
            # create labels
            if legend_labels is None:
                legend_labels = np.unique(df[df[target.name].notnull()][target.name])
            else:
                legend_labels = np.array(legend_labels)

            # generate colors
            color_list = style.color_gen("viridis", num=len(legend_labels))

            label_color = {}
            for ix, i in enumerate(legend_labels):
                label_color[i] = color_list[ix]

            # create patches
            patches = [Patch(color=v, label=k, alpha=alpha) for k, v in label_color.items()]

            # draw legend
            leg = plt.legend(
                handles=patches,
                fontsize=0.6 * self.chart_scale * np.log1p(len(g.axes.flat)),
                loc="upper right",
                markerscale=0.15 * self.chart_scale * np.log1p(len(g.axes.flat)),
                ncol=1,
                bbox_to_anchor=bbox,
            )

            # label font color
            for text in leg.get_texts():
                plt.setp(text, color="grey")

def hist(self, x, color, label, alpha=0.8):
    """
    Documentation:
        Description:
            create histogram of number variable. simple function capable of easy
            iteration through several groupings of a number variable that is
            separated out based on a object label. this results in several overlapping
            histograms and can reveal differences in distributions.
        Parameters:
            x : array
                1_dimensional array of values to be plotted on x_axis.
            color : string (some sort of color code)
                determines color of histogram.
            label : string
                category value label.
            alpha : float, default=0.8
                controls transparency of bars. accepts value between 0.0 and 1.0.
    """
    # create histogram.
    plt.hist(x=x, color=color, label=label, alpha=alpha)

