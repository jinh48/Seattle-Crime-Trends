#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 15:22:27 2020

@author: Jin Ning Huang
CSE 163 SUMMER 2020

This file contains for Task 2A.

NOTE: I am using local file, so please change the desirable filepath for your
computer.
"""

import pandas as pd
import matplotlib.pyplot as plt


def filtering_crime_type(df, crime):
    '''
    Takes the given Dataframe and the given string of certain crime. Returns
    the new filtered Dataframe that will only contains that crime type.
    '''
    filtered_df = df[df['Crime_Type'] == crime]

    return filtered_df


def sum_report_per_year(df):
    '''
    Takes the given Dataframe and will returns the sum of crime reports
    per year in Dataframe format. This function is meant to agg the invivudal
    crime type
    '''
    sum_year = df.groupby('Report_Year')['Report_Year_Total'].sum()

    return sum_year


def get_filter_spd(df):
    '''
    Take the given Dataframe, and filtering down to certain eight types of
    crimes: ASSAULT OFFENSES, HOMICIDE OFFENSES, BURGLARY/BREAKING&ENTERING,
    SEX OFFENSES, ROBBERY, LARCENY-THEFT, MOTOR VEHICLE THEFT, and
    DESTRUCTION/DAMAGE/VANDALISM OF PROPERTY. Also filtering the certain year
    range from 2007 to 2020. Then will do the sum aggregation of total report
    per ctime type, and will return a Dataframe.
    '''

    df = df[['Offense Start DateTime', 'Offense Parent Group', 'Longitude',
             'Latitude']].copy()

    df = df[df['Offense Parent Group'].isin([
        'ASSAULT OFFENSES', 'HOMICIDE OFFENSES', 'BURGLARY/BREAKING&ENTERING',
        'SEX OFFENSES', 'ROBBERY', 'LARCENY-THEFT', 'MOTOR VEHICLE THEFT',
        'DESTRUCTION/DAMAGE/VANDALISM OF PROPERTY'])]

    df['Year'] = df['Offense Start DateTime'].str[0:4].dropna().astype(int)
    df = df[(df['Year'] > 2007) & (df['Year'] < 2020)]

    df['Report_Year_Total'] = 1
    crimes = df.groupby(['Year', 'Offense Parent Group']
                        )['Report_Year_Total'].sum()
    df = crimes.reset_index()
    df = df.rename(columns={
        'Year': 'Report_Year',
        'Crime Number': 'Report_Yeat_Total',
        'Offense Parent Group': 'Crime_Type'
        })

    return df


def get_filter_crime(df):
    '''
    Takes the given Dataframe and filtering the unnecessary columns out; such
    as, Violent Crimes Total and Property Crimes Total, as they are
    overlapping with other crime types. Then will do the sum aggregation on
    total report per crime types, and will return a Dataframe.
    '''

    is_not_violent = df['Crime_Type'] != 'Violent Crimes Total'
    is_not_property = df['Crime_Type'] != 'Property Crimes Total'
    df = df[is_not_violent | is_not_property]

    df = df.groupby(['Report_Year', 'Crime_Type'])['Report_Year_Total'].sum()
    df = df.reset_index()

    return df


def get_filter_final(df):
    '''
    Takes the given Dataframe and renaming all the crime name on the column in
    order to get an appropriate naming. Will returns the Dataframe
    '''

    df['Crime_Type'].replace('Aggravated Assault', 'ASSAULT OFFENSES',
                             inplace=True)
    df['Crime_Type'].replace('Homicide', 'HOMICIDE OFFENSES', inplace=True)
    df['Crime_Type'].replace('NonResidential Burglary',
                             'DESTRUCTION/DAMAGE/VANDALISM OF PROPERTY',
                             inplace=True)
    df['Crime_Type'].replace('Rape', 'SEX OFFENSES', inplace=True)
    df['Crime_Type'].replace('Residential Burglary',
                             'BURGLARY/BREAKING&ENTERING', inplace=True)
    df['Crime_Type'].replace('Robbery', 'ROBBERY', inplace=True)
    df['Crime_Type'].replace('Theft', 'LARCENY-THEFT', inplace=True)
    df['Crime_Type'].replace('Vehicle Theft', 'MOTOR VEHICLE THEFT',
                             inplace=True)

    return df


def ploting_lines(df):
    '''
    Takes the given Dataframe and will filter the overall dataframe into eight
    individual dataframe based on each unique crime types. Then will plots
    eight lines chart for each of the crime. All of them will be in one
    map figure. Will save the map in png format.
    '''

    # filtering into 8 crimes types
    assault_df = filtering_crime_type(df, 'ASSAULT OFFENSES')
    homicide_df = filtering_crime_type(df, 'HOMICIDE OFFENSES')
    NR_burglary_df = filtering_crime_type(
        df, 'DESTRUCTION/DAMAGE/VANDALISM OF PROPERTY')
    rape_df = filtering_crime_type(df, 'SEX OFFENSES')
    R_burglaey_df = filtering_crime_type(df, 'BURGLARY/BREAKING&ENTERING')
    robbery_df = filtering_crime_type(df, 'ROBBERY')
    theft_df = filtering_crime_type(df, 'LARCENY-THEFT')
    car_theft_df = filtering_crime_type(df, 'MOTOR VEHICLE THEFT')

    # getting the reports per year data values
    Assault_report = sum_report_per_year(assault_df)
    Homicide_report = sum_report_per_year(homicide_df)
    NR_burglary_report = sum_report_per_year(NR_burglary_df)
    rape_report = sum_report_per_year(rape_df)
    R_burglaey_report = sum_report_per_year(R_burglaey_df)
    robbery_report = sum_report_per_year(robbery_df)
    theft_report = sum_report_per_year(theft_df)
    car_theft_report = sum_report_per_year(car_theft_df)

    # ploting
    fig, [[ax1, ax2], [ax3, ax4], [ax5, ax6], [ax7, ax8]] = plt.subplots(
        4, figsize=(10, 10), ncols=2)

    Assault_report.plot(ax=ax1, x='Report_Year', y='Report_Yeat_Total')
    Homicide_report.plot(ax=ax2, x='Report_Year', y='Report_Yeat_Total')
    NR_burglary_report.plot(ax=ax3, x='Report_Year', y='Report_Yeat_Total')
    rape_report.plot(ax=ax4, x='Report_Year', y='Report_Yeat_Total')
    R_burglaey_report.plot(ax=ax5, x='Report_Year', y='Report_Yeat_Total')
    robbery_report.plot(ax=ax6, x='Report_Year', y='Report_Yeat_Total')
    theft_report.plot(ax=ax7, x='Report_Year', y='Report_Yeat_Total')
    car_theft_report.plot(ax=ax8, x='Report_Year', y='Report_Yeat_Total')

    # labeling
    ax1.set_title('Assault Offenses')
    ax2.set_title('Homicide')
    ax3.set_title('NonResidential Burglary')
    ax4.set_title('Sex Offenses')
    ax5.set_title('Residential Burglary')
    ax6.set_title('Robbery')
    ax7.set_title('Larceny-Theft')
    ax8.set_title('Vehicle Theft')

    plt.tight_layout()
    plt.savefig('combined_crime_report.png')


def main():
    '''
    Wills use the raw datasets of Seattle Police Dept (SPD) Crime Data and the
    crime stats, and turn them into Dataframe format. This main function would
    filtering both Dataframe into get certain values, and do the aggregation
    of summing the values. Then will merge them into one to do the plot the
    lines figure.
    '''
    # raw data
    spd = pd.read_csv(
        '~/Desktop/CSE/CSE 163/project/part 2/Task 2/' +
        'SPD_Crime_Data__2008-Present.csv')
    crime_stats = pd.read_csv(
        '~/Desktop/CSE/CSE 163/project/part 2/Task 2/' +
        'Seattle_Crime_Stats_by_1990_Census_Tract_1996-2007.csv')

    # filtering datasets
    filtered_spd = get_filter_spd(spd)
    filtered_crime = get_filter_crime(crime_stats)

    # combine datasets into one and contintue filterings
    final = filtered_crime.merge(filtered_spd, how='outer')
    filtered_final = get_filter_final(final)

    # ploting
    ploting_lines(filtered_final)


if __name__ == '__main__':
    main()
