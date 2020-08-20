"""
Ruofeng Tang, Jin Ning Huang
This is the codes for Task 1 and Task 3.
It takes three datasets:
SPD Crime data from 2008 to present,
Police Use of Force data, and Police beats data.
It creates multiple graphs to compare.
"""


import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import seaborn as sns


def problem1ab(df):
    """
    takes the SPD crime data from 2008 to present and
    selects information about offense start time and
    offense type. Extracts detailed time information
    like year, month, year and month combined, hour.
    Then goes on to produces different graphs in submethods.
    solves research question 1a, 1b.
    """
    df = df[['Offense Start DateTime', 'Offense Parent Group']].copy()
    df['Year'] = df['Offense Start DateTime'].str[0:4].dropna().astype(int)
    df = df[(df['Year'] > 2007) & (df['Year'] < 2020)]
    new = df['Offense Start DateTime'].str.split(expand=True)
    df['Hour'] = new[1].str[0:2].astype(int)
    new1 = df['Offense Start DateTime'].str.split(pat='-', expand=True)
    df['Year and Month'] = new1[0].str[2:4] + new1[1]
    df['Month'] = new1[1]

    problem1a(df)
    problem1b1(df)
    problem1b2(df)


def problem1a(df):
    """
    takes the SPD crime data and produces five different graphs.
    The first graph is produced in this method, while other four is
    produced in submethods.
    This method separates crimes by year, and round up the time by hours.
    produces a bar chart: x-axis is the time period in a day,
    y-axis is the number of crimes, and in each time period,
    there are multiple bars representing each year from 2008 to 2019.
    solves research question 1a.
    """
    crimes = df.groupby(['Year', 'Hour']).size()
    df1 = crimes.index.to_frame()
    df1['Crime Number'] = crimes
    g = sns.catplot(x="Hour", y="Crime Number", hue="Year",
                    data=df1, kind='bar', height=6, aspect=5)
    plt.title('Crime numbers per hour by year')
    g.savefig('1a1.png')

    problem1a_helper(df, 'Year')
    problem1a_helper(df, 'Hour')
    problem1a_helper(df, 'Month')
    print(df.groupby('Month').size())
    problem1a_helper(df, 'Year and Month')


def problem1a_helper(df, x_axis):
    """
    takes the SPD crime data and a parameter for
    the x-axis of the graph.
    produces a line chart: x-axis is the passed parameter,
    one from 'Year', 'Hour', 'Month', 'Year and Month',
    y-axis is the crime number.
    """
    plt.figure(figsize=(5, 5))
    crimes = df.groupby([x_axis]).size()
    df1 = crimes.index.to_frame()
    df1['Crime Number'] = crimes
    g = sns.lineplot(x=x_axis, y="Crime Number", data=df1)
    g.set_title('Crime numbers per year')
    fig1 = g.get_figure()
    fig1.savefig('1a' + x_axis + '.png')


def problem1b1(df):
    """
    takes the SPD crime data and selects the ten crimes with the largest
    crime numbers. Plots a line chart: x-axis is the year,
    y-axis is the crime numbers, each line represents one crime.
    The 'Larceny-Theft' type is too large for the rest, so an adjusted
    plot with 'Larceny-Theft' removed is also provided.
    Tries to solve research question 1b.
    """
    top_crimes = df.groupby(['Offense Parent Group']).size()
    top_crimes = top_crimes.nlargest(10, keep='all').index

    crimes = df.groupby(['Year', 'Offense Parent Group']).size()
    df = crimes.index.to_frame()
    df['Crime Number'] = crimes
    df = df[df['Offense Parent Group'].isin(top_crimes)]

    plt.figure(figsize=(10, 10))
    g = sns.lineplot(x="Year", y="Crime Number",
                     hue="Offense Parent Group", data=df)
    g.set_title('Crime numbers per year by type')
    fig = g.get_figure()
    fig.savefig('1b11.png')

    df = df[df['Offense Parent Group'] != 'LARCENY-THEFT']
    plt.figure(figsize=(10, 10))
    g = sns.lineplot(x="Year", y="Crime Number",
                     hue="Offense Parent Group", data=df)
    g.set_title('Crime numbers per year by type adjusted')
    fig = g.get_figure()
    fig.savefig('1b12.png')


def problem1b2(df):
    """
    takes the SPD crime data and selects the ten crimes with the largest
    crime numbers. Plots a line chart: x-axis is the year and month,
    y-axis is the crime numbers, each line represents one crime.
    The 'Larceny-Theft' type is too large for the rest, so an adjusted
    plot with 'Larceny-Theft' removed is also provided.

    this is the response to a disadvantage in problem1b1 graphs: there are
    not enough data points to see a trend. Using 'Year and Month', the plots
    have more data points and therefore more accurate.
    Solves research question 1b.
    """
    top_crimes = df.groupby(['Offense Parent Group']).size()
    top_crimes = top_crimes.nlargest(10, keep='all').index
    crimes = df.groupby(['Year and Month', 'Offense Parent Group']).size()
    df = crimes.index.to_frame()
    df['Crime Number'] = crimes
    df = df[df['Offense Parent Group'].isin(top_crimes)]

    plt.figure(figsize=(10, 10))
    g = sns.lineplot(x="Year and Month", y="Crime Number",
                     hue="Offense Parent Group", data=df)
    g.set_title('Crime numbers per year and month by type')
    fig = g.get_figure()
    fig.savefig('1b21.png')

    df = df[df['Offense Parent Group'] != 'LARCENY-THEFT']
    plt.figure(figsize=(10, 10))
    g = sns.lineplot(x="Year and Month", y="Crime Number",
                     hue="Offense Parent Group", data=df)
    g.set_title('Crime numbers per year and month by type adjusted')
    fig = g.get_figure()
    fig.savefig('1b22.png')


def problem1c(df):
    """
    takes the SPD crime data and reads police beats spatial data,
    and plots a map of crime numbers over years combined based on police beats.
    solves research question1c.
    """
    df['Sum'] = 1
    df = df[['Beat', 'Sum']].copy()
    df = df.groupby(['Beat'])['Sum'].sum()
    beats = gpd.read_file('/project/SPD_BEATS_WGS84/SPD_BEATS_WGS84.shp')
    fig, ax = plt.subplots(1)
    beats.plot(color="#EEEEEE", ax=ax)
    merged = beats.merge(df, left_on='BEAT', right_on='Beat', how='inner')
    merged.plot(column='Sum', legend=True, ax=ax)
    fig.savefig('1c.png')


def problem3a(force):
    """
    takes the SPD use of force data and produces 4 graphs. The first three
    graphs are produced in submethods,
    and the last graph is produced in this method.
    Extracts time information from dataset and creates
    dummy variables for furture uses.
    The first three graphs use the following ratio:
    percentage of the given group's level 2,3 cases in a given year
    to percentage of the given group's level 1 cases in a given year.
    For example, the ratio for women in 2015 is:
    (2015 women level 2,3 cases / 2015 level 2,3 cases)
    / (2015 women level 1 cases / 2015 level 1 cases)
    Supposedly, an umbiased result is that all the ratios are near 1.
    prints the length of dataset and the number of
    cases where 'gender' is registered as 'Not Specified'
    to explain the abnormal 'Not specified' line in plot produced in
    problem3a_helper.
    prints the number of cases related to each race to explain
    the abnormality in plot produced in problem3a_helper.
    A considerable amount of cases register the race as 'Not Specified',
    leaving the old formula used unreliable. The first attempt to solve
    is to plot the same graph without race as 'Not Specified'.
    The second attempt is to change involved groups to
    only four main races recorded (Asian, Black or African American,
    Hispanic or Latino, White) and simplify the ratio to:
    number of level 2,3 cases of the given group in a given
    year to number of level 1 cases of the given group in the given year.
    Supposedly an umbiased result is that all the ratios are similar.
    """
    force = force[force['ID'].str[0:4] != '2020'].copy()
    force = force[['Incident_Type', 'Occured_date_time',
                   'Subject_Race', 'Subject_Gender']]
    new = force['Occured_date_time'].str.split(pat='/', expand=True)
    force['Year'] = new[2].str[0:4].astype(int)
    force['Month'] = new[0].astype(int)
    force['Year and Month'] = new[2].str[0:4] + new[0]
    force['Crime'] = 1
    force['Crime_Total'] = 1

    problem3a_helper('Subject_Gender', force)
    problem3a_helper('Subject_Race', force)

    print(len(force))
    print(len(force[force['Subject_Gender'] == 'Not Specified']))
    print(force.groupby('Subject_Race').size())

    temp = force[(force['Subject_Race'] != 'Not Specified')]
    problem3a_helper('Subject_Race', temp, 1)

    r = ['Black or African American', 'Hispanic or Latino', 'White', 'Asian']
    force = force[force['Subject_Race'].isin(r)].copy()
    force_1 = force[(force['Incident_Type'] == 'Level 1 - Use of Force')]
    force_23 = force[force['Incident_Type'] != 'Level 1 - Use of Force']
    force_1_1 = force_1.groupby(['Year', 'Subject_Race'])['Crime_Total'].sum()
    force_1_1 = force_1_1.reset_index()
    force_23_1 = force_23.groupby(['Year', 'Subject_Race'])['Crime'].sum()
    force_23_1 = force_23_1.reset_index()
    force_f = force_1_1.merge(force_23_1, how='left')
    force_f['Percentage'] = force_f['Crime'] / force_f['Crime_Total']
    plt.figure(figsize=(7, 7))
    g = sns.lineplot(x='Year', y='Percentage',
                     hue='Subject_Race', data=force_f)
    fig = g.get_figure()
    fig.savefig('3a.png')


def problem3a_helper(key, force, check=0):
    """
    takes a parameter to specify how to group cases(Race or Gender),
    takes the use of force dataset, and takes an indicator
    to name different graphs.
    breaks the dataset into two parts based on the use of force level
    being 1 or 2, 3. Calculates the percentages and ratios mentioned
    in problem3a and produces a graph: x-axis is year, y-axis is ratio,
    each line represent a group.
    """
    force_1 = force[force['Incident_Type'] == 'Level 1 - Use of Force']
    force_23 = force[force['Incident_Type'] != 'Level 1 - Use of Force']

    force_1_1 = force_1.groupby(['Year', key])['Crime'].sum()
    force_1_1 = force_1_1.reset_index()
    force_1_2 = force_1.groupby(['Year'])['Crime_Total'].sum()
    force_1_2 = force_1_2.reset_index()
    force_1_3 = force_1_1.merge(force_1_2, how='left')
    force_1_3['Level1'] = force_1_3['Crime'] / force_1_3['Crime_Total']

    force_23_1 = force_23.groupby(['Year', key])['Crime'].sum()
    force_23_1 = force_23_1.reset_index()
    force_23_2 = force_23.groupby(['Year'])['Crime_Total'].sum()
    force_23_2 = force_23_2.reset_index()
    force_23_3 = force_23_1.merge(force_23_2, how='left')
    force_23_3['Level23'] = force_23_3['Crime'] / force_23_3['Crime_Total']

    force_23_3['Ratio'] = force_23_3['Level23'] / force_1_3['Level1']
    plt.figure(figsize=(10, 10))
    g = sns.lineplot(x="Year", y="Ratio", hue=key, data=force_23_3)
    g.set_title('Use of force Ratio for ' + key + ' per year')
    fig = g.get_figure()
    if check == 0:
        fig.savefig(key + '.png')
    else:
        fig.savefig(key + '_new.png')


def problem3b(df, force):
    """
    takes both the SPD data and the use of force data and reads
    police beats spatial data, then produces 6 maps:
    In 2015 and 2019, the ratio of crimes in a police beat to total crimes;
    In 2015, 2018, 2019, the ratio of use of force Lvl 2,3 to use of force
    Lvl 1 in a police beat.
    The ratio of use of force Lvl 2,3 to use of force
    Lvl 1 in a police beat over the years.
    """
    df['Year'] = df['Offense Start DateTime'].str[0:4].dropna().astype(int)
    df['Sum'] = 1
    beats = gpd.read_file('/project/SPD_BEATS_WGS84/SPD_BEATS_WGS84.shp')
    problem3b_helper0(df, beats, 2015)
    plt.suptitle('2015 Crime Ratio')
    plt.savefig('3b2015_0.png')
    problem3b_helper123(force, beats, '2015')
    plt.suptitle('2015 Use of Force Lvl 2,3 to Lvl 1 Ratio')
    plt.savefig('3b2015_1.png')
    problem3b_helper0(df, beats, 2019)
    plt.suptitle('2019 Crime Ratio by Beat')
    plt.savefig('3b2019_0.png')
    problem3b_helper123(force, beats, '2019')
    plt.suptitle('2019 Use of Force Lvl 2,3 to Lvl 1 Ratio')
    plt.savefig('3b2019_1.png')
    problem3b_helper123(force, beats, '2018')
    plt.suptitle('2018 Use of Force Lvl 2,3 to Lvl 1 Ratio')
    plt.savefig('3b2018_1.png')
    df1 = df[['Beat', 'Sum']]
    df1 = df1.groupby(['Beat'])['Sum'].sum()
    df1 = df1 / df1.sum()
    fig, ax = plt.subplots(1)
    beats.plot(color="#EEEEEE", ax=ax)
    merged = beats.merge(df1, left_on='BEAT', right_on='Beat', how='inner')
    merged.plot(column='Sum', legend=True, ax=ax)
    plt.suptitle('Use of Force Lvl 2,3 to Lvl 1 Ratio')
    plt.savefig('3b.png')


def problem3b_helper0(df, beats, year):
    """
    takes the SPD data, police beats spatial data and a year(2015 or 2019)
    and plots the ratio of crimes in a police beat to total crimes.
    Separates each crime record by beat and sums them up to get the total
    crimes, and then relates the beat names with spatial data.
    """
    df = df[df['Year'] == year].copy()
    df = df[['Beat', 'Sum']]
    df = df.groupby(['Beat'])['Sum'].sum()
    df = df / df.sum()
    fig, ax = plt.subplots(1)
    beats.plot(color="#EEEEEE", ax=ax)
    merged = beats.merge(df, left_on='BEAT', right_on='Beat', how='inner')
    merged.plot(column='Sum', legend=True, ax=ax)


def problem3b_helper123(force, beats, year):
    """
    takes the SPD data, police beats spatial data and a year(2015 or 2019)
    and plots the ratio of use of force Lvl 2,3 to use of force Lvl 1 in
    a poilce beat.
    Separates the use of force data by level 1
    and 2/3, and sums them up by beat.
    Calculates the ratio between two parts
    and relates the beat names with spatial data.
    """
    force = force.copy()
    force['Year'] = force['ID'].str[0:4]
    force = force[force['Year'] == year]
    force['Sum1'] = 1
    force['Sum23'] = 1
    force_1 = force[force['Incident_Type'] == 'Level 1 - Use of Force']
    force_23 = force[force['Incident_Type'] != 'Level 1 - Use of Force']
    force_1_1 = force_1.groupby(['Beat'])['Sum1'].sum()
    force_1_1 = force_1_1.reset_index()
    force_23_1 = force_23.groupby(['Beat'])['Sum23'].sum()
    force_23_1 = force_23_1.reset_index()
    force_final = force_1_1.merge(force_23_1, how='inner',
                                  left_on='Beat', right_on='Beat')
    force_final['Percentage'] = force_final['Sum23'] / force_final['Sum1']
    merged = beats.merge(force_final,
                         left_on='BEAT', right_on='Beat', how='inner')
    fig, ax = plt.subplots(1)
    beats.plot(color="#EEEEEE", ax=ax)
    merged.plot(column='Percentage', legend=True, ax=ax)


def main():
    """
    This is the main method. It reads a Seattle Police Department record
    of every crime reported from 2008 to present,
    and it reads a SPD Use of Force record from 2014 to present.
    Then it processes files in different methods corresponding to different
    research questions.
    """
    df = pd.read_csv('/project/SPD_Crime_Data__2008-Present.csv')
    problem1ab(df)
    problem1c(df)
    force = pd.read_csv('/project/Use_Of_Force.csv')
    problem3a(force)
    problem3b(df, force)


if __name__ == "__main__":
    main()
