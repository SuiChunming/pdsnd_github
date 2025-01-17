#The script for bickshare project
import time
import pandas as pd
#import numpy as np

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
    city_name_list = ['chicago','new york city','washington']
    
    city = input("Please enter the name of the city you want to explore: \n")
    
    while city.lower() not in city_name_list:
        city = input("The city you searched is not in our database, please enter a valid city name again: \n")
    
    city = city.lower()    

    # get user input for month (all, january, february, ... , june)
    month_name_list = ['all','january','february','march','april','may','june']
    
    month = input("Please enter the month you want to search (please enter 'all' if you want to search all months): \n")
    
    while month.lower() not in month_name_list:
        month = input("The month you searched is not in our database, please enter a valid month again or 'all' to search all months: \n")
    
    month = month.lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_name_list = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    
    day = input("Please enter the weekday name you want to search (please enter 'all' if you want to search all days): \n")
    
    while day.lower() not in day_name_list:
        day = input("The weekday name you searched is not in our database, please enter a valid weekday name again or 'all' to search all days : \n")

    day = day.lower()


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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    #df = pd.read_csv('chicago.csv')
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week_num'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        
        # filter by day of week to create the new dataframe
        weekday_name = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3,
                        'friday':4, 'saturday':5, 'sunday':6}        
        df = df[df['day_of_week_num'] == weekday_name[day]]
    
    
    answer = input("Would you like to have a look at the raw data you selected? Please enter \'Y (Yes)\' or \'N (No)\': \n" )
    answer = answer.lower()
    
    while answer == "y":
        i = 0
        print(df[i:i+5])
        answer = input("\n Would you like to check more rows of the data? Please enter \'Y (Yes)\' or \'N (No)\': \n" )
        answer = answer.lower()
        while answer == "y":
            i+=5
            if i+5 < len(df):
                print(df[i:i+5])
                answer = input("\n Would you like to check more rows of the data? Please enter \'Y (Yes)\' or \'N (No)\': \n" )
            elif i+5 > len(df):
                print(df[i:len(df)-i])
                print("\n No more data avaliable!")
                answer = "n"
    
    button = input("\n Now we start to enter into data analysis section! Press anyrthing to continue \n")

    return df
    


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # display the most common month
    df['month'] = df['Start Time'].dt.month
    month_count = df['month'].value_counts()
    popular_month= month_count.idxmax()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most Frequent Start Month: ', months[popular_month-1])
    
    # display the most common day of week
    df['day'] = df['Start Time'].dt.weekday
    day_count = df['day'].value_counts()
    popular_day= day_count.idxmax()
    weekday_name = {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday',
                    4:'friday', 5:'saturday', 6:'sunday'}
    print('Most Frequent Start Day: ', weekday_name[popular_day])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    hour_count = df['hour'].value_counts()
    popular_hour= hour_count.idxmax()
    print('Most Frequent Start Hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    s_station_count = df['Start Station'].value_counts()
    popular_s_station= s_station_count.idxmax()
    print('Most commonly used start station: ', popular_s_station)
    
    # display most commonly used end station
    e_station_count = df['End Station'].value_counts()
    popular_e_station= e_station_count.idxmax()
    print('Most commonly used end station: ', popular_e_station)

    # display most frequent combination of start station and end station trip
    # for solving this problem we need firtly group start station and end station as a new column
    popular_com_station = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('Most frequent combination of start station and end station trip: ', popular_com_station)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_trave_time = df['Trip Duration'].sum()
    print('The total travel time for explored dataframe is {}s'.format(total_trave_time))
    # display mean travel time
    mean_travel_time = total_trave_time/len(df['Trip Duration'])
    print('The mean travel time for explored dataframe is {}s'.format(mean_travel_time))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print('The counts of user types for searched dataframe: ', user_types_count)

    # Display counts of gender
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print('The counts of gender of users for searched dataframe: ', gender_count)
    elif 'Gender' not in df:
        print('Sorry! The selected city do not have \'gender\' data!')
            
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth = df['Birth Year'].min()
        mostrecent_birth = df['Birth Year'].max()
        birth_count = df['Birth Year'].value_counts().idxmax()
        print('The earliest, most recent, and most common year of birth are: {}, {}, and {} '.format(earliest_birth, mostrecent_birth, birth_count))
    elif 'Birth Year' not in df:
        print('Sorry! The selected city do not have \'Birth Year\' data!')
    
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

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
