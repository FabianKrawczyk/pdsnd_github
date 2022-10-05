import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Additional explanation ...
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # Casefold is used to avoid any issues with loqer case letters or capitalization 
    city = input('Which city would you like to explore? Chicago, New York or Washington?: ').casefold()
    while city not in ['chicago', 'new york city', 'washington']:
        city = input('Your City is not available. Please try again (chicago, new york city or washington): ').casefold()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Which month would you like? Please return a specific month or "all": ').casefold()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input('Please enter a valid month: ').casefold()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day would you like? Please return a weekday or "all": ').casefold()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        day = input('Please enter a valid day: ').casefold()
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Loads data for the specified city
    if city not in ['new york city']:
        df = pd.read_csv('{}.csv'.format(city))
    else:
        df = pd.read_csv('new_york_city.csv')
    
    # Convert the Start Time and End Time column to datetime 
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # Extract and add month columns and filters if applicable
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]
                                      
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print('The most common month is: ', df['month'].mode()[0])

    # TO DO: display the most common day of week
    print('The most common day is: ', df['day_of_week'].mode()[0])

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common hour is: ', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('The most common start station is: ', df['Start Station'].mode()[0])

    # TO DO: display most commonly used end station
    print('The most common end station is: ', df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    most_frequent_combination = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('The most frequent combination of start and end station is: ', most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time is: ', df['Trip Duration'].sum())

    # TO DO: display mean travel time
    print('Mean travel time is: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        user_gender = df['Gender'].value_counts()
        print(user_gender)

    # TO DO: Display earliest, most recent, and most common year of birth
    # if clause is used to as some columns are empty for gender and birth year
    if 'Birth Year' in df.columns:
        print('The earliest birthday is: ', df['Birth Year'].min())
        print('The most recent birthday is: ', df['Birth Year'].max())
        print('The most common birthday is: ', df['Birth Year'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    

def raw_data (df):
    """
    #displays 5 more rows each time and if the user don't wanna see more raw data the script can be stopped with no
    """
    more_data_input = input('\nWould you like to see more raw data? Enter yes or no?.\n').casefold()
    while more_data_input not in ['yes', 'no']:
         more_data_input = input('\nPlease enter yes or no?.\n').casefold()
    n = 0
    while True:
        if more_data_input == 'yes':
            n = n+5
            print(df.head(n))
            more_data_input = input('\nWould you like to see more raw data? Enter yes or no?.\n').casefold()
            while more_data_input not in ['yes', 'no']:
                more_data_input = input('\nPlease enter yes or no?.\n').casefold()
        else:
            break


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
