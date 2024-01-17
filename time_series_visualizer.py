import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import calendar
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col="date", parse_dates=True)

# Clean data
page_view_upper_treshold = df['value'].quantile(0.975)
page_view_lower_treshold = df['value'].quantile(0.025)

df = df[
  (df['value'] > page_view_lower_treshold) &
  (df['value'] < page_view_upper_treshold)
]


def draw_line_plot():
    # Draw line plot
    fig = df.plot(
        kind="line", 
        xlabel="Date", 
        ylabel="Page Views", 
        title="Daily freeCodeCamp Forum Page Views 5/2016-12/2019",
        legend=False,
        figsize=(12,6)
    ).get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.groupby([df.index.year, df.index.month_name()])['value'].mean().unstack()
    df_bar = df_bar[list(calendar.month_name)[1:]]
    df_bar.columns.name = 'Months'

    # Draw bar plot
    fig = df_bar.plot(
        kind="bar", 
        xlabel="Years", 
        ylabel="Average Page Views"
    ).get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    boxplot_1 = sns.boxplot(
    data=df_box,
    x='year',
    y='value',
    ax=axes[0]
    )

    boxplot_1.set(
    xlabel="Year",
    ylabel="Page Views",
    title="Year-wise Box Plot (Trend)",
    ylim=(0, 200000),
    yticks=range(0, 200001, 20000)
    )

    boxplot_2 = sns.boxplot(
    data=df_box,
    x='month',
    y='value',
    order=list(month[:3] for month in calendar.month_name)[1:],
    ax=axes[1]
    )

    boxplot_2.set(
    xlabel='Month',
    ylabel='Page Views',
    title='Month-wise Box Plot (Seasonality)',
    ylim=(0, 200000),
    yticks=range(0, 200001, 20000),
    )

    plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
