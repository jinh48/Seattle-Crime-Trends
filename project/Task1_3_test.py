"""
Ruofeng Tang, Jin Ning Huang
This is the test file to project.py.
it tests non-plot parts of project.py.
Mostly it checks if dimensions and column names
of the datasets are correct. The nummerical parts
are usually displayed through graphs, so there is no
testing to numeric parts. The data visualization
itself is a check to numeric parts.
"""

from cse163_utils import assert_equals
import pandas as pd
import geopandas as gpd


def problem1ab_t(df):
    """
    tests the non-plot parts of problem1ab by using
    assert_equals. It will crash if an error occurs.
    """
    df = df[['Offense Start DateTime', 'Offense Parent Group']].copy()
    df['Year'] = df['Offense Start DateTime'].str[0:4].dropna().astype(int)
    df = df[(df['Year'] > 2007) & (df['Year'] < 2020)]
    assert_equals(12, len(df['Year'].unique()))
    # should be 12 years from 2008 to 2019
    new = df['Offense Start DateTime'].str.split(expand=True)
    df['Hour'] = new[1].str[0:2].astype(int)
    new1 = df['Offense Start DateTime'].str.split(pat='-', expand=True)
    df['Month'] = new1[1]
    assert_equals(12, len(df['Month'].unique()))  # should be 12 months
    df['Year and Month'] = new1[0].str[2:4] + new1[1]
    assert_equals(144, len(df['Year and Month'].unique()))
    # should be 12 years * 12 months = 144 year and month

    problem1a_t(df)
    problem1b1_t(df)
    problem1b2_t(df)


def problem1a_t(df):
    """
    tests the non-plot parts of problem1a by using
    assert_equals. It will crash if an error occurs.
    """
    crimes = df.groupby(['Year', 'Hour']).size()
    df1 = crimes.index.to_frame()
    df1['Crime Number'] = crimes
    assert_equals(288, len(df1))
    # 12 years times 24 hours should be 288 rows in df1

    a = problem1a_helper_t(df, 'Year')
    assert_equals(12, a)
    a = problem1a_helper_t(df, 'Hour')
    assert_equals(24, a)
    a = problem1a_helper_t(df, 'Month')
    assert_equals(12, a)
    a = problem1a_helper_t(df, 'Year and Month')
    assert_equals(144, a)


def problem1a_helper_t(df, x_axis):
    """
    helps problem1a_t to test problem1a.
    Does not do anything itself to test.
    """
    crimes = df.groupby([x_axis]).size()
    df1 = crimes.index.to_frame()
    df1['Crime Number'] = crimes
    return len(df1)


def problem1b1_t(df):
    """
    tests the non-plot parts of problem1b1 by using
    assert_equals. It will crash if an error occurs.
    """
    top_crimes = df.groupby(['Offense Parent Group']).size()
    top_crimes = top_crimes.nlargest(10, keep='all').index
    crimes = df.groupby(['Year', 'Offense Parent Group']).size()
    df = crimes.index.to_frame()
    df['Crime Number'] = crimes
    df = df[df['Offense Parent Group'].isin(top_crimes)]
    assert_equals(10, len(df['Offense Parent Group'].unique()))
    assert_equals(120, len(df))


def problem1b2_t(df):
    """
    tests the non-plot parts of problem1b2 by using
    assert_equals. It will crash if an error occurs.
    """
    top_crimes = df.groupby(['Offense Parent Group']).size()
    top_crimes = top_crimes.nlargest(10, keep='all').index
    crimes = df.groupby(['Year and Month', 'Offense Parent Group']).size()
    df = crimes.index.to_frame()
    df['Crime Number'] = crimes
    df = df[df['Offense Parent Group'].isin(top_crimes)]
    count = len(df['Offense Parent Group'].unique())
    assert_equals(10, count)
    # 10 crime types
    assert_equals(1440, len(df))
    # 12 years * 12 months * 10 crime types


def problem1c_t(df):
    """
    tests the non-plot parts of problem1c by using
    assert_equals. It will crash if an error occurs.
    """
    df['Sum'] = 1
    df = df[['Beat', 'Sum']].copy()
    df = df.groupby(['Beat'])['Sum'].sum()
    beats = gpd.read_file('/project/SPD_BEATS_WGS84/SPD_BEATS_WGS84.shp')
    merged = beats.merge(df, left_on='BEAT', right_on='Beat', how='inner')
    assert_equals(51, len(merged))   # there are 51 beats in Seattle


def problem3a_t(force):
    """
    tests the non-plot parts of problem3a_t by using
    assert_equals. It will crash if an error occurs.
    """
    force = force[force['ID'].str[0:4] != '2020'].copy()
    force = force[['Incident_Type', 'Occured_date_time',
                   'Subject_Race', 'Subject_Gender']]
    new = force['Occured_date_time'].str.split(pat='/',
                                               expand=True)
    force['Year'] = new[2].str[0:4].astype(int)
    assert_equals(6, len(force['Year'].unique()))
    # should be 6 years from 2014 to 2019
    force['Month'] = new[0].astype(int)
    assert_equals(12, len(force['Month'].unique()))
    # should be 12 months
    force['Year and Month'] = new[2].str[0:4] + new[0]
    assert_equals(72, len(force['Year and Month'].unique()))
    # should be 6 years * 12 months = 72 year and month
    force['Crime'] = 1
    force['Crime_Total'] = 1

    a = problem3a_helper_t('Subject_Gender', force)
    assert_equals(18, a)   # should be 6 years * 3 genders = 18 rows
    a = problem3a_helper_t('Subject_Race', force)
    assert_equals(41, a)
    # should be 6 years * 7 genders = 42. It is 41 though because some
    # dod not have use of force level 2/3 records in 2014. Shown below.
    temp = force[force['Incident_Type'] != 'Level 1 - Use of Force']
    temp = temp.groupby(['Subject_Race', 'Year']).size()
    assert_equals(41, len(temp))

    a = problem3a_helper_t('Subject_Race',
                           force[(force['Subject_Race'] != 'Not Specified')])
    assert_equals(35, a)
    # should be 6 years * 6 genders = 36. Again due to missing record it is 35.

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
    assert_equals(24, len(force_f))
    # should be 6 years * 4 selected races = 24


def problem3a_helper_t(key, force):
    """
    helps problem3a_t to test the non-plot parts of problem3a.
    returns the length of processed data and check if it is correct
    in problem3a_t using assert_equals
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

    force_23_3['Percentage'] = force_23_3['Level23'] / force_1_3['Level1']

    return len(force_23_3)


def problem3b_t(df, force):
    """
    It helps problem3b_helper0_t to test problem3b_helper_0
    and it tests the non-plot parts of problem3b_helper123_t using
    assert_equals. Will crash if something is wrong.
    """
    df['Year'] = df['Offense Start DateTime'].str[0:4].dropna().astype(int)
    df['Sum'] = 1
    beats = gpd.read_file('/project/SPD_BEATS_WGS84/SPD_BEATS_WGS84.shp')

    problem3b_helper0_t(df, beats, 2015)
    a, b, c = problem3b_helper123_t(force, beats, '2015')
    assert_equals(48, a)
    # Supposedly, length of police beats with use of force data is 51,
    # there are 51 police beats. But a is smaller because not every beat
    # has both Lvl1 and Lvl2,3 information, as displayed by b and c.
    assert_equals(53, b)
    assert_equals(49, c)
    problem3b_helper0_t(df, beats, 2019)
    a, b, c = problem3b_helper123_t(force, beats, '2019')
    assert_equals(45, a)
    # Similarly, only 45 police beats have the required ratio because
    assert_equals(54, b)
    # 54 police beats (more than existed due to recording error) are recorded,
    assert_equals(49, c)
    # only 49 police beats have Lvl 2,3 information.


def problem3b_helper0_t(df, beats, year):
    """
    tests the non-plot parts of problem3b_helper_t using
    assert_equals. It will crash if an error occurs.
    """
    df = df[df['Year'] == year].copy()
    df = df[['Beat', 'Sum']]
    df = df.groupby(['Beat'])['Sum'].sum()
    df = df / df.sum()
    merged = beats.merge(df, left_on='BEAT', right_on='Beat', how='inner')
    assert_equals(51, len(merged))
    # there are 51 beats in Seattle


def problem3b_helper123_t(force, beats, year):
    """
    helps problem3b_t to test problem3b_helper123.
    returns the length of processed final dataset,
    length of the dataset with use of force Lvl 1 by police beat,
    and length of the dataset of Lvl 2,3 by police beat.
    check if they are correct in problem3b_t using assert_equals
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
    merged = beats.merge(force_final, left_on='BEAT',
                         right_on='Beat', how='inner')
    return len(merged), len(force_1_1), len(force_23_1)


def main():
    """
    reads SPD crime data and use of force data and runs all the test methods.
    """
    df = pd.read_csv('/project/SPD_Crime_Data__2008-Present.csv')
    problem1ab_t(df)
    problem1c_t(df)
    force = pd.read_csv('/project/Use_Of_Force.csv')
    problem3a_t(force)
    problem3b_t(df, force)


if __name__ == "__main__":
    main()
