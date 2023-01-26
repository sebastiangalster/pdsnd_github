import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# list of available months january to june 
months = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington) + make input case insensitiv
    city = input("Please type in the city you want to check? ").lower()

    # check if the input meets the available values to screen
    while city not in {"chicago", "new york city", "washington"}:
        print("\n{} is not a valid input! Please choose either:\n\n- Chicago\n- New York City\n- Washington\n".format(city))
        city = input("Please choose a city from the list! ").lower()

    # get user input for month and make input case insensitiv
    month = input("Which month do you want to check? Or do you want to check all? ").lower()

    # check if the input meets the available values to screen
    while month not in months and month != 'all':
        print("\n{} is not a valid input! Please choose either:\n\n- all\n- {}\n- {}\n- {}\n- {}\n- {}\n- {}\n".format(month,*months))
        month = input("Please choose a value form the list! ").lower()

    # get user input for day of week and make input case insensitiv
    day = input("What day do you want to check? Or do you want to check all? ").lower()
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # check if the input meets the available values to screen
    while day not in days and day != 'all':
        print("\n{} is not a valid input! Please choose either:\n\n- all\n- {}\n- {}\n- {}\n- {}\n- {}\n- {}\n- {}\n".format(day,*days))
        day = input("Please choose a value form the list! ").lower()

    print('-'*40)
    # return the entered values
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name() 

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    # return dataframe
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]

    # display the most common popular hour
    print('Most Popular Start Hour:', popular_hour)


    # find the most popular day
    popular_day = df['day_of_week'].mode()[0]

    # display the most common day of week
    print('Most Popular Start Day:', popular_day)


    # find the most popular month
    popular_month = df['month'].mode()[0]

    # display the most common month
    print('Most Popular Start Month:', popular_month)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    popular_startstation = df['Start Station'].mode()[0]

    print('Most Popular Start Station:', popular_startstation)

    # display most commonly used end station

    popular_endstation = df['End Station'].mode()[0]

    print('Most Popular End Station:', popular_endstation)

    # display most frequent combination of start station and end station trip

    popular_startandendstation = pd.concat([df['Start Station'], df['End Station']], axis=1, join='inner').mode()
    print('\nMost Popular Combination of Start-& End-Station:\n\n', popular_startandendstation.to_string(index=False))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    print('The total duration of all filtered trips is: {} hours. '.format(total_duration))

    # display mean travel time
    average_duration = df['Trip Duration'].mean()
    print('The average duration of all filtered trips is: {} hours. '.format(average_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Number of user types:\n', user_types.to_string())

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print('\nNumber of gender types:\n', gender_types.to_string())
    except KeyError:
        print("There isn't a [Gender] column in this spreedsheet!")

    
    # Display earliest, most recent, and most common year of birth
    try:
        earliest = df['Birth Year'].min()
        print("\nEarliest year of customers birth:", earliest)
    except KeyError:
        print("There isn't a [Birth Year] column in this spreedsheet!")

    try:
        latest = df['Birth Year'].max()
        print("Most recent year of customers birth:",latest)
    except KeyError:
        print("There isn't a [Birth Year] column in this spreedsheet!")

    try:
        common = df['Birth Year'].mode()
        print("Most common year of customers birth:", common.to_string(index=False))
    except KeyError:
        print("There isn't a [Birth Year] column in this spreedsheet!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def showrawdata(df):
    # display the number of results
    counter = df.shape[0]
    rawdata = input("There are {} rows! Do you want so see the raw data? type y or n! ".format(counter)).lower()

    # ask to show raw data - if yes show 5 rows
    low = 0
    high = 5
    while rawdata != 'n':
        print(df[low:high])
        low += 5
        high += 5
        rawdata = input("Do you want so see 5 more rows? type y or n! ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # call all functions
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        showrawdata(df)



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
