#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# self.py: functions to help produce plots of metrics from runs
import math
import time
import numpy as np
import pandas as pd

from xtlib import errors
from xtlib import console
from xtlib import run_helper

class PlotBuilder():
    def __init__(self, run_names, col_names, x_col, layout, break_on, title, colors, show_legend, plot_titles,
            legend_titles, smoothing_factor, plot_type, marker_size, marker_shape, alpha, edge_color, timeout,
            aggregate, range_type, range_alpha, run_log_records, style, show_toolbar):
        
        self.run_names = run_names
        self.col_names = col_names
        self.x_col = x_col
        self.layout = layout
        self.break_on = break_on
        self.title = title
        self.colors = colors
        self.show_legend = show_legend
        self.plot_titles = plot_titles
        self.legend_titles = legend_titles
        self.smoothing_factor = smoothing_factor
        self.plot_type = plot_type
        self.marker_size = marker_size
        self.marker_shape = marker_shape
        self.alpha = alpha
        self.edge_color = edge_color
        self.timeout = timeout
        self.aggregate = aggregate
        self.range_type = range_type
        self.range_alpha = range_alpha
        self.run_log_records = run_log_records
        self.style = style
        self.show_toolbar = show_toolbar

    def build(self):
        data_frames = self.pre_process_data()
        self.plot_data_frames(data_frames)

    def pre_process_data(self):
        '''
        1. for each run, collected the reported metrics into 1 or more pandas DataFrame objects

        2. merge DataFrames from all runs

        2. apply pre-processing operations:
            - optionally smooth the Y-axis cols
            - optionally create aggregated Y-axis cols, by runs
            - optionally create aggregated range Y-axi cols, by runs
        '''

        # build "data_frames"
        data_frames = []

        for record in self.run_log_records:
            # extract metrics for this run
            run_name = record["_id"]
            log_records = record["log_records"]

            metric_sets = run_helper.build_metrics_sets(log_records)
            if not metric_sets:
                console.print("note: run currently has no logged metrics: {}".format(run_name))
                self.run_names.remove(run_name)
                continue

            if not self.col_names:
                # not specified by user, so build defaults
                self.col_names, self.x_col = self.get_default_metric_column(metric_sets)

            # merge metric sets into data_frames
            for metric_set in metric_sets:

                # create a pandas DataFrame
                df = pd.DataFrame(metric_set["records"])
                
                # add run_name column
                df["run_name"] = [run_name] * df.shape[0]
                self.merge_data_frames(data_frames, df)

        # do we need to transform data?
        if self.aggregate != "none" or self.range_type != "none" or self.smoothing_factor:

            if self.smoothing_factor:

                # SMOOTH each column of values
                for run_name, data_frames in run_data_frames.items():
                    for data_frame in data_frames:
                        for col in data_frame.keys():

                            if col == self.x_col:
                                continue

                            self.apply_smooth_factor(data_frame, col, self.smoothing_factor)

            if self.aggregate != "none":
                # specifying an aggregate hides the the other runs' values (for now)
                self.run_names = [self.aggregate]   

                agg_values = self.aggregate_runs(data_frame, col, self.aggregate)
                runs_dict[self.aggregate] = agg_values

            if self.range_type != "none":
                self.run_names.append(self.range_type)

                min_values, max_values = self.range_runs(runs_dict, self.range_type)
                runs_dict[self.range_type] = (min_values, max_values)

        return data_frames

    
    def merge_data_frames(self, data_frames, df_add):
        found = False
        df_add_list = list(df_add.columns)
        df_add_list.sort()

        for i, df in enumerate(data_frames):
            df_list = list(df.columns)
            df_list.sort()

            if df_list == df_add_list:
                df_new = df.append(df_add)
                data_frames[i] = df_new
                found = True

        if not found:
            data_frames.append(df_add)

    def apply_smooth_factor(self, data_frame, col, weight):

        presmooth_values = [dd[col] for dd in data_frame[col]]
        smooth_values = self.apply_smooth_factor_core(presmooth_values, weight)

        data_frame[col] = smooth_values
        data_frame["_presmooth_." + col] = presmooth_values

    def apply_smooth_factor_core(self, values, weight):
        smooth_values = []

        if values:
            prev = values[0] 
            for value in values:
                smooth = weight*prev + (1-weight)*value
                smooth_values.append(smooth)                       
                prev = smooth                                 

        return smooth_values

    def calc_actual_layout(self, count, layout):
        if not "x" in layout:
            errors.syntax_error("layout string must be of form RxC (R=# rows, C=# cols)")

        r,c = layout.split("x", 1)

        if r:
            r = int(r)
            c = int(c) if c else math.ceil(count // r)
        elif c:
            c = int(c)
            r = int(r) if r else math.ceil(count // c)

        full_count = r*c
        if full_count < count:
            errors.syntax_error("too many plots ({}) for layout cells ({})".format(count, full_count))

        return r, c

    def get_xy_values(self, data_frames, run_name, y_col, x_col):
        values = None

        for df in data_frames:
            if x_col:
                if y_col in df.columns and x_col in df.columns:
                    df_run = df.loc[ df['run_name'] == run_name]
                    values = [ df_run[x_col].values, df_run[y_col].values, df_run ]
                    break
            else:
                if y_col in df.columns:
                    df_run = df.loc[ df['run_name'] == run_name]
                    values = [ None, df_run[y_col].values, df_run ]
                    break

        if not values:
            if x_col:
                errors.internal_error("specified columns (x={}, y={}) not found in any datasets".format(x_col, y_col))
            else:
                errors.store_error("specified column (y={}) not found in any datasets".format(y_col))

        return values

    def plot_data_frames(self, data_frames):

        # on-demand import for faster XT loading
        import seaborn as sns
        import matplotlib.pyplot as plt
        import matplotlib as mpl
        import pylab

        if not self.show_toolbar:
            # hide the ugly toolbar at bottom left of plot window
            mpl.rcParams['toolbar'] = 'None' 

        # apply seaborn styling
        if self.style and self.style != "none":
            sns.set_style(self.style)

        # decide how layout, titles, etc. will be set
        run_count = len(self.run_names)
        col_count = len(self.col_names)

        break_on_runs = self.break_on and "run" in self.break_on
        break_on_cols = self.break_on and "col" in self.break_on

        if break_on_runs and break_on_cols:
            plot_count = run_count*col_count
        elif break_on_runs:
            plot_count = run_count
        elif break_on_cols:
            plot_count = col_count
        else:
            plot_count = 1

        # calc true layout 
        if self.layout:
            plot_rows, plot_cols = self.calc_actual_layout(plot_count, self.layout) 
        else:
            plot_cols = plot_count
            plot_rows = 1

        runs_per_plot = 1 if break_on_runs else run_count
        cols_per_plot = 1 if break_on_cols else col_count
        
        if runs_per_plot == 1:
            plot_title = "$run"
            legend_text = "$col"
        elif cols_per_plot == 1:
            plot_title = "$col"
            legend_text = "$run"
        else:
            plot_title = None
            legend_text = "$col ($run)"

        if not self.plot_titles and plot_title:
            self.plot_titles = [plot_title]

        if not self.legend_titles:
            self.legend_titles = [legend_text]

        if not self.colors:
            self.colors = ["blue", "red", "green", "orange"]

        # configure matplotlib for our subplots
        sharex = True
        sharey = True

        #plt.close()
        window_size = (14, 6)

        fig, plots = plt.subplots(plot_rows, plot_cols, figsize=window_size, sharex=sharex, sharey=sharey, constrained_layout=True)
        if plot_count == 1:
            # make it consistent with plot_count > 1 plots
            plots = [plots]
        elif plot_rows > 1:
            plots = plots.flatten()

        fig.suptitle(self.title, fontsize=16)

        if self.timeout:
            # build a thread to close our plot window after specified time
            from threading import Thread

            def set_timer(timeout):
                console.print("set_timer called: timeout=", self.timeout)
                time.sleep(self.timeout)
                console.diag("timer triggered!")

                plt.close("all")
                print("closed all plots and the fig")

            thread = Thread(target=set_timer, args=[self.timeout])
            thread.daemon = True    # mark as background thread
            thread.start()

        line_index = 0
        plot_index = 0

        if self.aggregate != "none" or (break_on_cols and not break_on_runs):
            # columns needs to be the outer loop
            for c, col in enumerate(self.col_names):

                if c and break_on_cols:
                    plot_index += 1
                    line_index = 0

                for r, run_name in enumerate(self.run_names):

                    if r and break_on_runs:
                        plot_index += 1
                        line_index = 0

                    # PLOT_INNER
                    ax = plots[plot_index]
                    x_values, y_values, df = self.get_xy_values(data_frames, run_name, col, self.x_col)

                    self.plot_inner(ax, y_values, run_name, col, self.x_col, x_values, line_index, data_frame=df)
                    line_index += 1
        else:
            # run will work as the outer loop
            for r, run_name in enumerate(self.run_names):

                if r and break_on_runs:
                    plot_index += 1
                    line_index = 0

                for c, col in enumerate(self.col_names):

                    if c and break_on_cols:
                        plot_index += 1
                        line_index = 0

                    # PLOT_INNER
                    ax = plots[plot_index]
                    x_values, y_values, df = self.get_xy_values(data_frames, run_name, col, self.x_col)

                    self.plot_inner(ax, y_values, run_name, col, self.x_col, x_values, line_index, data_frame=df)
                    line_index += 1

        pylab.show()

    def get_seaborn_color_map(self, name, n_colors=5):
        '''
        name: muted, xxx
        '''
        import seaborn as sns
        from matplotlib.colors import ListedColormap

        # Construct the colormap
        current_palette = sns.color_palette(name, n_colors=n_colors)
        cmap = ListedColormap(sns.color_palette(current_palette).as_hex())
        return cmap

    def plot_inner(self, ax, y_values, run_name, col, x_col, x_values, line_index, data_frame):

        import seaborn as sns
        from matplotlib.ticker import MaxNLocator

        if x_values is not None:
            x_values = [float(x) for x in x_values]
            ax.set_xlabel(x_col)

        if isinstance(y_values, tuple):
            # its the 2-tuple of (low, high) values
            y_low, y_high = y_values

            y_low = [float(y) for y in y_low]
            y_high = [float(y) for y in y_high]

            if not x_values:
                x_values = range(len(y_low))
        else:
            # normal list of values
            y_low, y_high = None, None
            y_values = [float(y) for y in y_values]
            if not x_values:
                x_values = range(len(y_values))
        
        console.diag("x_values=", x_values)
        console.diag("y_values=", y_values)

        num_y_ticks = 10
        ax.yaxis.set_major_locator(MaxNLocator(num_y_ticks))
        color = self.colors[line_index % len(self.colors)]

        line_title = self.legend_titles[line_index % len(self.legend_titles)]
        line_title = self.fixup_text(line_title, run_name, col)

        cmap = self.get_seaborn_color_map("muted")
        if self.plot_type == "line":

            # LINE or RANGE PLOT
            if y_low:
                ax.fill_between(x_values, y_low, y_high, color=color, label=line_title, alpha=self.range_alpha)
            elif x_values:
                # ax.plot(x_values, y_values, '-', ms=self.marker_size, markerfacecolor=color, markeredgecolor=self.edge_color, 
                #     color=color, markeredgewidth=1, marker=self.marker_shape, 
                #     label=line_title, alpha=self.alpha)

                #ax.plot(x_values, y_values, label=line_title, marker=self.marker_shape, color=color)
                ax.plot(x_values, y_values, label=line_title, marker=self.marker_shape)

            #     markers = True if self.marker_shape else False
            #     sns.lineplot(x_values, y_values, label=line_title, ax=ax, markers=markers)
            else:
                ax.plot(y_values, '-', ms=self.marker_size, markerfacecolor=color, markeredgecolor=self.edge_color, 
                    color=color, markeredgewidth=1, label=line_title, alpha=self.alpha)

            #sns.relplot(x=x_col, y=col, kind="line", data=data_frame)
                    
        elif self.plot_type == "scatter":

            # SCATTER PLOT
            if not x_values:
                errors.combo_error("must specify x_col for scatterplots")

            ax.scatter(x_values, y_values, color=color,  label=line_title, s=self.marker_size, alpha=self.alpha)
            # '-', ms=3, markerfacecolor=color, markeredgecolor=color, 
            #     color=color, markeredgewidth=1,

        elif self.plot_type == "histogram":

            # HISTOGRAM
            ax.hist(y_values, color=color, label=line_title)
            
        else:
            errors.syntax_error("unknown plot type={}".format(self.plot_type))

        if self.plot_titles:
            plot_title = self.plot_titles[line_index % len(self.plot_titles)]
            plot_title = self.fixup_text(plot_title, run_name, col)

            ax.set_title(plot_title)

        if self.show_legend:
            ax.legend()

    def fixup_text(self, text, run_name, col):
        text = text.replace("$run", run_name)
        text = text.replace("$col", col)
        return text

    def get_default_metric_column(self, metric_sets):
        # remove x-col names from y_cols
        x_names = ["epoch", "step", "iter", "epochs", "steps", "iters"]
        x_col = None
        keys = None

        for ms in metric_sets:
            keys = ms["keys"]
            if len(keys) == 1 and keys[0].lower() == "epoch":
                # skip isolated epoch reporting
                continue

            for xn in x_names:
                if xn in keys:
                    if not x_col:
                        x_col = xn
                    keys.remove(xn)
                    break

            break

        return keys, x_col

    def aggregate_runs(self, runs_dict, aggregate):
        runs = list(runs_dict.values())

        if aggregate == "mean":
            values = np.mean(runs, axis=0)
        else:
            errors.syntax_error("unrecognized aggregate value: {}".format(aggregate))

        return values

    def range_runs(self, runs_dict, range):
        runs = list(runs_dict.values())

        if range == "minmax":
            min_values = np.min(runs, axis=0)
            max_values = np.max(runs, axis=0)
        elif range == "std":
            means = np.mean(runs, axis=0)
            max_values = means + np.std(runs, axis=0)
            min_values = means - np.std(runs, axis=0)
        elif range == "error":
            from scipy import stats

            means = np.mean(runs, axis=0)
            max_values = means + stats.sem(runs, axis=0)
            min_values = means - stats.sem(runs, axis=0)
        else:
            errors.syntax_error("unrecognized range value: {}".format(range))

        return min_values, max_values

    def get_values_by_run(self, col, run_log_records):
        runs_dict = {}

        for rr in run_log_records:
            run_name = rr["_id"]
            value_recs = rr["metrics"]["records"]
            new_values = [vr[col] for vr in value_recs]

            runs_dict[run_name] = new_values

        return runs_dict

    