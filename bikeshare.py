import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city = ''
    while city not in CITY_DATA.keys():
        city = input('Please enter a city (Chicago, New York City, or Washington): \n').lower()
        if city not in CITY_DATA.keys():
            print('\nError: invalid input!\n')
    
    # get user input for month (all, january, february, ... , june)
    months = ['january','february','march','april','may','june','all']
    month = ''
    while month not in months:
        month = input('Please enter a month (January, February, March, April, May, or June) or type all for all months: \n').lower()
        if month not in months:
            print('\nError: invalid input!\n')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all','sunday','monday','tuesday','wednesday','thursday','friday','saturday']
    day = ''
    while day not in days:
        day = input('Please enter a day (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) or type all for all days: \n').lower()
        if day not in days:
            print('\nError: invalid input!\n')
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    #df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':            
        # filter by month to create the new dataframe
        is_month = df['Month'] == month.title()
        df = df[is_month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        is_day = df['Day'] == day.title()
        df = df[is_day]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating the most frequent times of travel...\n')
    start_time = time.time()
    # display the most common month
    popular_month = df['Month'].mode()[0]
    
    print(('The most popular month is {}').format(popular_month))
    # display the most common day of week
    popular_day = df['Day'].mode()[0]
    print(('The most popular day of the week is {}').format(popular_day))
    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    popular_hour = df['Start Hour'].mode()[0]
    print(('The most common start hour is {}').format(popular_hour))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the most popular stations and trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print(('The most popular start station is {}').format(popular_start_station))
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print(('The most popular end station is {}').format(popular_end_station))
    
    # display most frequent combination of start station and end station trip
    df["Trip"] = df["Start Station"] + ' - ' + df["End Station"]
    popular_stations = df['Trip'].mode()[0]
    print(('The most popular trip is {}').format(popular_stations))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating trip duration...\n')
    start_time = time.time()

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print(('Total travel time is {}').format(total_trip_duration))
    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    print(('Average travel time is {}').format(mean_trip_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating user stats...\n')
    start_time = time.time()
    
    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(('Counts of user types are \n{}').format(user_types))
    # Display counts of gender
    if 'Gender' in df.columns:
        gender_types = df['Gender'].value_counts()
        print(('Counts of genders are \n{}').format(gender_types))
    else:
        print('\nNo gender data to show')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        popular_birth_year = int(df['Birth Year'].mode()[0])
        print(('Most common year of birth is {}').format(popular_birth_year))
        earliest_birth_year = int(df['Birth Year'].min())
        print(('Earliest year of birth is {}').format(earliest_birth_year))
        recent_birth_year = int(df['Birth Year'].max())
        print(('Most recent year of birth is {}').format(recent_birth_year))
    else:
        print('\nNo birth year data to show')
            
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
        
            
def raw_data(df):
    row_index = 0
    while True:
        user_input = input('\nWould you like to display the ' + ('first' if row_index == 0 else 'next') + ' 5 rows of data?\n')
        if user_input.lower() != 'yes':
            break
        else:
            for _ in range(5):
                output = str(df.iloc[row_index:row_index + 1,1:].to_dict('records')[0])
                print('\nRow ' + str(row_index) + '\n' + output.replace(', ','\n').replace('{','').replace('}','').replace('\'',''))
                row_index += 1
            print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    

if __name__ == "__main__":
	main()
