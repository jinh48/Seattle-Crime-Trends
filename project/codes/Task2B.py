#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 15:07:23 2020

@author: Jin Ning Huang
CSE 163 SUMMER 2020

This file contains for Task2B.

NOTE: I am using local file, so please change the desirable filepath for your
computer.
"""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


def crime_report():
    '''
    Using the two datasets of crime stats and the census of 1990 in order to
    plots the maps with following years: 1996, 2000, and 2005
    '''
    # dataset
    crime_stats = pd.read_csv(
            '~/Desktop/CSE/CSE 163/project/part 2/Task 2/' +
            'Seattle_Crime_Stats_by_1990_Census_Tract_1996-2007.csv')

    census_1990 = gpd.read_file(
        '/Users/jinninghuang/Desktop/CSE/CSE 163/' +
        'project/part 2/Task 2/Census_Tracts_1990-shp/Census_Tracts_1990.shp')

    merged_df = crime_stats.merge(
        census_1990, left_on='Census_Tract_1990',
        right_on='TRACTLAB', how='right')
    merged_df = merged_df[merged_df['Report_Year_Total'].notna()]
    merged_gdf = gpd.GeoDataFrame(merged_df)

    # plotting
    crime_helper(merged_gdf, 1996)
    plt.title('Crime Percentage Ratio by 1996')
    plt.savefig('crime_ratio_1996.png')

    crime_helper(merged_gdf, 2000)
    plt.title('Crime Percentage Ratio by 2000')
    plt.savefig('crime_ratio_2000.png')

    crime_helper(merged_gdf, 2005)
    plt.title('Crime Percentage Ratio by 2005')
    plt.savefig('crime_ratio_2005.png')


def spd_report():
    '''
    Using the two datasets of Seattle Police Dept (SPD) Crime Data and Seattle
    Police Dept Beats in order to plots the map with following years: 2010,
    2015, and 2019
    '''
    # dataset
    spd = pd.read_csv(
        '~/Desktop/CSE/CSE 163/project/part 2/Task 2/' +
        'SPD_Crime_Data__2008-Present.csv')

    spd['Year'] = spd['Offense Start DateTime'].str[0:4].dropna().astype(int)
    spd['Sum'] = 1
    beats = gpd.read_file('/Users/jinninghuang/Desktop/CSE/CSE 163/project/' +
                          'part 2/Task 2/spdbeat_WGS84/spdbeat_WGS84.shp')
    beats = beats.to_crs(epsg=4326)

    # plotting
    spd_helper(spd, beats, 2010)
    plt.title('Crime Percentage Ratio by 2010')
    plt.savefig('crime_ratio_2010.png')

    spd_helper(spd, beats, 2015)
    plt.title('Crime Percentage Ratio by 2015')
    plt.savefig('crime_ratio_2015.png')

    spd_helper(spd, beats, 2019)
    plt.title('Crime Percentage Ratio by 2019')
    plt.savefig('crime_ratio_2019.png')


def crime_helper(gdf, year):
    '''
    Takes the given GeoDataFrame and given value of year, and will filtering
    the dataset based on that given year. Will aggregate the data by the sum
    the census tract. Will make new column, 'ratio, that will take each of the
    census tract's sum value into the ratio percentage. Then will plots out.
    '''
    get_year = gdf[gdf['Report_Year'] == year]
    sum_result = get_year.dissolve(by='Census_Tract_1990', aggfunc='sum')

    total = get_year['Report_Year_Total'].sum()
    sum_result['ratio'] = sum_result['Report_Year_Total'] / total * 100
    sum_result.plot(column='ratio', legend=True)


def spd_helper(spd, beats, year):
    '''
    Takes the given Dataframe of SPD, given GeoDataframe of Beats, and given
    value of year, and will filtering the dataset based on that given year.
    Will aggregate the data by the sum of the sector (county area), and also
    will take each of the sector's sum value into the ratio percentage.
    Then will plots out.
    '''
    spd = spd[spd['Year'] == year].copy()
    total = spd['Sum'].sum()

    spd = spd.groupby(['Sector'])['Sum'].sum() / total * 100
    merged = beats.merge(spd, left_on='SECTOR', right_on='Sector',
                         how='inner')
    merged.plot(column='Sum', legend=True)


def main():
    '''
    Contains two functions that will produce 6 map figures for Seattle Crime
    Ratio.
    '''
    crime_report()
    spd_report()


if __name__ == '__main__':
    main()
