import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv'}

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

    city = input("Would you like to see data for Chicago, New york, Washington?\n").lower()
    while city not in("new york ", "chicago", "washington"):
        city = input("invalid input, please try again\n").lower()

    # get user input for month (all, january, february, ... , june)

    month = input("Which month you want to fillter by? Please enter the choice as \'january, february, march, april, may, ot june\'. You can type \'all\' if you want all months\n").lower()
    while month not in ('january', 'february', 'march', 'april', 'may', 'june','all'):
        month = input("invalid input, please try again\n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = input("Which dat you would like to fillter by? Please enter the choice as \'sunday, monday, tuesday, wednesday, thursday, friday or saturday. You can \'all\' if you wanr all days\n").lower()
    while day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
        day = input("invalid input, please try again\n").lower()

    print('-'*40)
    return city, month, day

#this method displays the cities that included in the system.
def cities():
    print("These are the three cities that included in our system, Chicago, New York, and Washington\n")

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

    # here we load data file into dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert start time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filtering by month
    if month != 'all':
        # here we use the index of the months list to get the month integer
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # here we filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filtering by day of week
    if day != 'all':
        # here we filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    months = ['january', 'february', 'march', 'april', 'may', 'june']
    commonMonth = df['month'].mode()[0]
    print('\nThe most common month is: {}'.format(months[commonMonth-1]))

    # display the most common day of week

    print('\nThe most common day is: {}'.format(df['day_of_week'].mode()[0]))

    # display the most common start hour

    print('\nThe most common hour is: {}'.format(df['hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nThe most commonly used start station is: {} '.format(df['Start Station'].value_counts().idxmax()))

    # display most commonly used end station
    print('The most commonly used end station is: {}'.format(df['End Station'].value_counts().idxmax()))

    # display most frequent combination of start station and end station trip
    df['combination stations'] = df['Start Station'] + " AND " + df['End Station']
    print('The most frequent combination of start station and end station trip are: {}'.format(
        df['combination stations'].value_counts().idxmax()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_seconds = df['Trip Duration'].sum()
    print('The total travel time is: {} days'.format(total_seconds/86400))

    # display mean travel time

    mean_seconds = df['Trip Duration'].mean()
    print('The avrage of travel time is: {} hours'.format(mean_seconds/60))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The user types are:\n\n{} '.format(df['User Type'].value_counts()))

    # Display counts of gender
    print('The counts of gender are:\n\n')
    try:
        print(df['Gender'].value_counts())
    except KeyError:
        print("\nSorry, no data available for this month.")

    # Display earliest, most recent, and most common year of birth

    print('\nThe earlist year of birth is: ')
    try:
        earliset_birth = df['Birth Year'].min()
        print(earliset_birth)
    except KeyError:
        print("\nSorry, no data available for this month.")

    print('\nThe most recent year of birth is: ')
    try:
        recent_birth = df['Birth Year'].max()
        print(recent_birth)
    except KeyError:
        print("\nSorry, no data available for this month.")

    print('\nThe most common year of birth is: ')
    try:
        common_birth = df['Birth Year'].mode()[0]
        print(common_birth)
    except KeyError:
        print("\nSorry, no data available for this month.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        rawData = input("Would you like yo view individual trip data? Type \'yes\' or \'no\'.").lower()

        if rawData == "yes":
            Number = 0
            print("If you want to stop, write \'no\'")
            while(rawData != "no"):
                Number+=5
                print(df.head(Number))
                rawData = input("Do you want to continue?\n")


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


main()
