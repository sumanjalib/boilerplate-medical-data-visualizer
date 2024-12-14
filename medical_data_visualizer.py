import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = pd.Series(map(lambda x: 1 if x == True else 0, (df['weight'] / np.square(df['height']/100) > 25)))

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df.loc[:,'cholesterol'].replace(to_replace=[1,2,3], value=[0,1,1], inplace=True)
df.loc[:,'gluc'].replace(to_replace=[1,2,3], value=[0,1,1], inplace=True)

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat_grouped = df_cat.groupby(['cardio', 'variable', 'value'], as_index = False).size().rename(columns ={'size' : 'total'})

    # Draw the catplot with 'sns.catplot()'

    fig = sns.catplot(x='variable', y='total', data=df_cat_grouped, hue='value', kind='bar', col='cardio').fig
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones((corr.shape[0],corr.shape[0])), k=0)



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(24,12))

    # Draw the heatmap with 'sns.heatmap()'

    sns.heatmap(corr, mask = mask, annot=True, fmt='.1f', square=True, vmin=0.08, vmax=0.24)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
