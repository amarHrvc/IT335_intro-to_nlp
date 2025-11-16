"""
Generic helper functions for converting pandas data to markdown tables.
Makes it easy to create tables for your research paper!
"""

import pandas as pd
from IPython.display import display, Markdown
import matplotlib.pyplot as plt


def value_counts_to_markdown(df, column_name, show_index=True, sort=True):
    """
    Count values in a column and convert to markdown table.
    
    Think of it like: "Count how many of each thing, then make a nice table"
    
    Parameters:
    -----------
    df : pandas DataFrame
        Your data (like train_df, validation_df, test_df)
    column_name : str
        Which column to count (like 'people_number', 'days', 'level')
    show_index : bool
        True = show the value names (default: True)
        False = hide the value names
    sort : bool
        True = sort by value (3, 5, 7 instead of random order)
        False = keep original order
    
    Returns:
    --------
    str : Markdown formatted table
    
    Example:
    --------
    # Count how many trips have 1, 2, 3, etc. people
    table = value_counts_to_markdown(validation_df, 'people_number')
    print(table)
    """
    
    # Count the values
    counts = df[column_name].value_counts()
    
    # Sort if requested
    if sort:
        counts = counts.sort_index()
    
    # Convert to markdown
    markdown_table = counts.to_markdown(index=show_index)
    
    return markdown_table


def distribution_to_markdown(df, column_name, show_index=True, sort=True, 
                            add_percentage=False, rename_columns=None):
    """
    Create a distribution table with counts (and optionally percentages).
    
    Think of it like: "Show me how many of each thing, and maybe show % too"
    
    Parameters:
    -----------
    df : pandas DataFrame
        Your data
    column_name : str
        Which column to analyze
    show_index : bool
        Show the category names (default: True)
    sort : bool
        Sort by category (default: True)
    add_percentage : bool
        Add a percentage column (default: False)
    rename_columns : dict or None
        Rename columns, e.g., {'count': 'Number of Trips'}
    
    Returns:
    --------
    str : Markdown formatted table
    
    Example:
    --------
    # Show trip duration with percentages
    table = distribution_to_markdown(
        validation_df, 
        'days',
        add_percentage=True,
        rename_columns={'count': 'Number of Trips', 'percentage': 'Percentage'}
    )
    print(table)
    """
    
    # Count values
    counts = df[column_name].value_counts()
    
    if sort:
        counts = counts.sort_index()
    
    # Create DataFrame for better control
    result_df = pd.DataFrame({'count': counts})
    
    # Add percentage if requested
    if add_percentage:
        result_df['percentage'] = (counts / counts.sum() * 100).round(2)
    
    # Rename columns if requested
    if rename_columns:
        result_df = result_df.rename(columns=rename_columns)
    
    # Convert to markdown
    markdown_table = result_df.to_markdown(index=show_index)
    
    return markdown_table


def compare_distributions_markdown(dfs_dict, column_name, show_index=True, sort=True):
    """
    Compare the same column across multiple datasets side-by-side.
    
    Think of it like: "Show Train, Validation, and Test counts next to each other"
    
    Parameters:
    -----------
    dfs_dict : dict
        Dictionary of DataFrames, e.g., 
        {'Train': train_df, 'Validation': validation_df, 'Test': test_df}
    column_name : str
        Which column to compare
    show_index : bool
        Show the category names
    sort : bool
        Sort by category
    
    Returns:
    --------
    str : Markdown formatted comparison table
    
    Example:
    --------
    # Compare trip durations across all three datasets
    datasets = {
        'Train': train_df,
        'Validation': validation_df,
        'Test': test_df
    }
    table = compare_distributions_markdown(datasets, 'days')
    print(table)
    """
    
    # Create a dictionary to store counts from each dataset
    all_counts = {}
    
    for dataset_name, df in dfs_dict.items():
        counts = df[column_name].value_counts()
        if sort:
            counts = counts.sort_index()
        all_counts[dataset_name] = counts
    
    # Combine into one DataFrame
    result_df = pd.DataFrame(all_counts)
    
    # Fill missing values with 0
    result_df = result_df.fillna(0).astype(int)
    
    # Convert to markdown
    markdown_table = result_df.to_markdown(index=show_index)
    
    return markdown_table


def summary_stats_to_markdown(df, column_name, show_index=True):
    """
    Calculate summary statistics (mean, median, min, max, std) and convert to markdown.
    
    Think of it like: "Give me all the important numbers about this column"
    
    Parameters:
    -----------
    df : pandas DataFrame
        Your data
    column_name : str
        Which numeric column to summarize
    show_index : bool
        Show the statistic names
    
    Returns:
    --------
    str : Markdown formatted statistics table
    
    Example:
    --------
    # Get statistics about query lengths
    stats = summary_stats_to_markdown(validation_df, 'query_length_words')
    print(stats)
    """
    
    # Calculate statistics
    stats_dict = {
        'Count': df[column_name].count(),
        'Mean': df[column_name].mean().round(2),
        'Median': df[column_name].median(),
        'Min': df[column_name].min(),
        'Max': df[column_name].max(),
        'Std Dev': df[column_name].std().round(2)
    }
    
    # Convert to DataFrame
    stats_df = pd.DataFrame(stats_dict, index=[column_name])
    
    # Transpose to show stats as rows
    stats_df = stats_df.T
    stats_df.columns = ['Value']
    
    # Convert to markdown
    markdown_table = stats_df.to_markdown(index=show_index)
    
    return markdown_table


def dataframe_to_markdown(df, show_index=True, max_rows=None, display_table=False):
    """
    Convert any DataFrame to markdown (most generic function).
    
    Think of it like: "Turn this whole table into markdown format"
    
    Parameters:
    -----------
    df : pandas DataFrame
        Any DataFrame you want to convert
    show_index : bool
        Show row numbers/names
    max_rows : int or None
        Limit number of rows (None = show all)
    display_table : bool
        If True, displays the table directly in Jupyter (default: False)
        If False, returns markdown string for printing
    
    Returns:
    --------
    str : Markdown formatted table (or displays it if display_table=True)
    
    Example:
    --------
    # Show first 10 rows as a rendered table
    dataframe_to_markdown(train_df.head(10), display_table=True)
    
    # Or get the markdown string to print
    table = dataframe_to_markdown(train_df.head(10))
    print(table)
    """
    
    # Limit rows if requested
    if max_rows is not None:
        df = df.head(max_rows)
    
    # Convert to markdown
    markdown_table = df.to_markdown(index=show_index)
    
    # Display or return
    if display_table:
        display(Markdown(markdown_table))
        return None
    else:
        return markdown_table


# ==============================================================================
# EASY-TO-USE WRAPPER FUNCTIONS (Even simpler!)
# ==============================================================================

def quick_count(df, column, show_names=True):
    """
    Super simple: count values and make markdown table.
    
    Example:
    --------
    print(quick_count(validation_df, 'people_number'))
    """
    return value_counts_to_markdown(df, column, show_index=show_names, sort=True)


def quick_compare(train_df, validation_df, test_df, column):
    """
    Super simple: compare column across all three datasets.
    
    Example:
    --------
    print(quick_compare(train_df, validation_df, test_df, 'days'))
    """
    datasets = {
        'Train': train_df,
        'Validation': validation_df,
        'Test': test_df
    }
    return compare_distributions_markdown(datasets, column)


def quick_stats(df, column):
    """
    Super simple: get statistics for a numeric column.
    
    Example:
    --------
    print(quick_stats(validation_df, 'query_length_words'))
    """
    return summary_stats_to_markdown(df, column)


# ==============================================================================
# PLOTTING FUNCTIONS
# ==============================================================================

def plot_value_distribution(df, column_name, title=None, xlabel=None, ylabel='Number of Trips',
                           figsize=(10, 6), color='skyblue', save_path=None, dpi=300):
    """
    Create a bar plot showing the distribution of values in a column.
    
    Parameters:
    -----------
    df : pandas DataFrame
        Your data
    column_name : str
        Which column to plot
    title : str or None
        Plot title (auto-generated if None)
    xlabel : str or None
        X-axis label (uses column_name if None)
    ylabel : str
        Y-axis label (default: 'Number of Trips')
    figsize : tuple
        Figure size (width, height) in inches
    color : str
        Bar color (default: 'skyblue')
    save_path : str or None
        Path to save the plot (e.g., 'results/plot.png')
    dpi : int
        Resolution for saved image (default: 300)
    
    Returns:
    --------
    fig, ax : matplotlib figure and axes objects
    
    Example:
    --------
    # Simple usage
    plot_value_distribution(validation_df, 'days', 
                           title='Trip Duration Distribution',
                           save_path='results/trip_duration.png')
    
    # Compare across datasets by calling multiple times
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    plot_value_distribution(train_df, 'days', title='Train Set')
    plot_value_distribution(validation_df, 'days', title='Validation Set')
    plot_value_distribution(test_df, 'days', title='Test Set')
    """
    
    # Auto-generate labels if not provided
    if title is None:
        title = f'{column_name.replace("_", " ").title()} Distribution'
    if xlabel is None:
        xlabel = column_name.replace('_', ' ').title()
    
    # Create plot
    fig, ax = plt.subplots(figsize=figsize)
    df[column_name].value_counts().sort_index().plot(
        kind='bar', ax=ax, color=color, edgecolor='black'
    )
    
    # Customize appearance
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    
    plt.show()
    
    return fig, ax


def plot_pie_chart(df, column_name, title=None, figsize=(8, 8), colors=None,
                   explode=None, show_percentages=True, save_path=None, dpi=300):
    """
    Create a pie chart showing the distribution of values in a column.
    
    Parameters:
    -----------
    df : pandas DataFrame
        Your data
    column_name : str
        Which column to plot
    title : str or None
        Plot title (auto-generated if None)
    figsize : tuple
        Figure size (width, height) in inches
    colors : list or None
        List of colors for slices (auto-generated if None)
    explode : list or None
        List of floats to "explode" slices (e.g., [0, 0.1, 0] explodes 2nd slice)
    show_percentages : bool
        Show percentages on slices (default: True)
    save_path : str or None
        Path to save the plot
    dpi : int
        Resolution for saved image (default: 300)
    
    Returns:
    --------
    fig, ax : matplotlib figure and axes objects
    
    Example:
    --------
    # Simple usage
    plot_pie_chart(validation_df, 'people_number',
                   title='Distribution of Group Sizes',
                   save_path='results/group_sizes_pie.png')
    
    # With custom colors and exploded slice
    plot_pie_chart(validation_df, 'days',
                   colors=['#ff9999', '#66b3ff', '#99ff99'],
                   explode=[0, 0.1, 0],  # Explode the 2nd slice
                   save_path='results/trip_duration_pie.png')
    """
    
    # Auto-generate title if not provided
    if title is None:
        title = f'{column_name.replace("_", " ").title()} Distribution'
    
    # Get value counts
    data = df[column_name].value_counts().sort_index()
    
    # Create plot
    fig, ax = plt.subplots(figsize=figsize)
    
    # Configure autopct (percentage display)
    autopct = '%1.1f%%' if show_percentages else None
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        data.values,
        labels=data.index,
        autopct=autopct,
        colors=colors,
        explode=explode,
        startangle=90,
        textprops={'fontsize': 12}
    )
    
    # Make percentage text bold
    if show_percentages:
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
    
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    
    # Save if path provided
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    
    plt.show()
    
    return fig, ax


# ==============================================================================
# USAGE EXAMPLES
# ==============================================================================

if __name__ == "__main__":
    """
    Example usage - uncomment and run to see how it works!
    """
    
    print("="*70)
    print("MARKDOWN HELPER FUNCTIONS - EXAMPLES")
    print("="*70)
    
    # You would load your data here
    # import pandas as pd
    # train_df = pd.read_csv('TravelPlanner/train.csv')
    # validation_df = pd.read_csv('TravelPlanner/validation.csv')
    # test_df = pd.read_csv('TravelPlanner/test.csv')
    
    print("\n📋 Example 1: Simple value counts")
    print("-" * 70)
    print("Code: value_counts_to_markdown(validation_df, 'people_number')")
    print("\nOutput would look like:")
    print("""
|   people_number |   count |
|----------------:|--------:|
|               1 |      45 |
|               2 |      60 |
|               3 |      35 |
|               4 |      25 |
    """)
    
    print("\n📋 Example 2: Value counts WITHOUT index")
    print("-" * 70)
    print("Code: value_counts_to_markdown(validation_df, 'people_number', show_index=False)")
    print("\nOutput would look like:")
    print("""
|   count |
|--------:|
|      45 |
|      60 |
|      35 |
|      25 |
    """)
    
    print("\n📋 Example 3: Distribution with percentages")
    print("-" * 70)
    print("Code:")
    print("""
distribution_to_markdown(
    validation_df, 
    'days',
    add_percentage=True,
    rename_columns={'count': 'Number of Trips', 'percentage': '%'}
)
    """)
    print("\nOutput would look like:")
    print("""
|   days |   Number of Trips |     % |
|-------:|------------------:|------:|
|      3 |                60 | 33.33 |
|      5 |                60 | 33.33 |
|      7 |                60 | 33.33 |
    """)
    
    print("\n📋 Example 4: Compare across datasets")
    print("-" * 70)
    print("Code: quick_compare(train_df, validation_df, test_df, 'days')")
    print("\nOutput would look like:")
    print("""
|   days |   Train |   Validation |   Test |
|-------:|--------:|-------------:|-------:|
|      3 |      15 |           60 |    308 |
|      5 |      15 |           60 |    351 |
|      7 |      15 |           60 |    341 |
    """)
    
    print("\n📋 Example 5: Summary statistics")
    print("-" * 70)
    print("Code: quick_stats(validation_df, 'query_length_words')")
    print("\nOutput would look like:")
    print("""
|          |   Value |
|:---------|--------:|
| Count    |  180.00 |
| Mean     |   65.42 |
| Median   |   64.00 |
| Min      |   25.00 |
| Max      |  108.00 |
| Std Dev  |   18.35 |
    """)
    
    print("\n" + "="*70)
    print("💡 TIP: Copy any of these functions into your Jupyter notebook!")
    print("="*70)
