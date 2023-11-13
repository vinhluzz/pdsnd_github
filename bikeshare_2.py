import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york.csv',
              'washington': 'washington.csv' }

listMonth = {'January':1, 'Feburary':2, 'March':3, 'April':4, 'May':5, 'June':6}
listDayOfWeek = {
                "Monday": 0,
                "Tuesday":1,
                "Wednesday":2,
                "Thursday":3,
                "Friday":4,
                "Saturday":5,
                "Sunday":6
               }

def input_month():
    """
     Input Month for filter
    """
    while True:
            month = input("Which month? January, Feburary, March, April, May, or June?\n")
            month = month.capitalize()
            if listMonth.get(month) is not None:
                break

    print("You input month: " + month)
    return month

def input_day():
    """
       Input day of week: Sunday, Monday,...
    """
    while True:
             day = input("Which day?(Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday).\n")
             day = day.capitalize()
             
             if listDayOfWeek.get(day) is not None:
                break
                
    print("You input day: " + day)
    return day

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = 'chicago'
    month = "none"
    day = "none"
    
    print('Hello! I am MrFour It! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for Chicago, New York, or Washington?\n")
        city = city.lower()
        if city == "chicago" or city == "new york" or city == "washington":
            break

    print(city)

    # get user input for month (all, january, february, ... , june)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        validOptions = ['day','month','both','none']
        option = input("Would you like to filter the data by month, day, both, or not at all? Type 'none' for no time filter \n")
        option = option.lower()
        if option in validOptions:
            break

    if option == "both":
        month = input_month()
        day = input_day()
    elif option == "month":
        month = input_month()
    elif option == "day":
        day = input_day()

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
    print("Load data frame for: Citiy={}, month={}, day={}".format(city,month,day))
    filename = './' + CITY_DATA[city]
    print("Filename = ", filename)
    data = pd.read_csv(filename)
    print(data)
    """Convert Start Time to Datetime """
    data["Start Time"] = pd.to_datetime(data["Start Time"])

    """Fitler data by month and day."""
    if month != "none":
        print("Filter data by month\n")
        data = data[data["Start Time"].dt.month ==  listMonth.get(month)]

    if day != "none":
        print("Filter data by Day of week\n")
        data = data[data["Start Time"].dt.dayofweek == listDayOfWeek.get(day)]

    df = pd.DataFrame(data)
    print(df)

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_stats = df["Start Time"].dt.month.value_counts()
    most_common_month = month_stats.idxmax()
    print("The most common month:", most_common_month)
    
    # display the most common day of week
    day_stats = df["Start Time"].dt.dayofweek.value_counts()
    most_common_day = day_stats.idxmax()

    for key, value in listDayOfWeek.items():
        if value == most_common_day:
            print("The most common day of week:", key)
            break

    # display the most common start hour
    hour_stats = df["Start Time"].dt.hour.value_counts()
    most_common_hour = hour_stats.idxmax()
    print("The most common hour: ", most_common_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_stats = df["Start Station"].value_counts()
    common_start = start_stats.idxmax()
    print("Most commonly used start station: ", common_start)

    # display most commonly used end station
    end_stats = df["End Station"].value_counts()
    common_end = end_stats.idxmax()
    print("Most commonly used end station: ", common_end)

    # display most frequent combination of start station and end station trip
    group_combination = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    most_frequent = group_combination.loc[group_combination['count'].idxmax()]
    print("Most frequent combination:")
    print("Start station: ", most_frequent['Start Station'])
    print("End station: ", most_frequent['End Station'])
    print("Count: ", most_frequent['count'])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['Trip Duration'] = df['Trip Duration'].astype('int')

    # display total travel time
    sum_duration = df['Trip Duration'].sum()
    print("Total duration: {} (seconds)".format(sum_duration))

    # display mean travel time
    travel_time = df.groupby(["Start Station", "End Station"])["Trip Duration"].mean()
    print("Mean travel time")
    print(travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types and ignore na
    user_types = df["User Type"].value_counts(dropna=True)
    print(user_types)

    # Display counts of gender and ignore na
    genders = df["Gender"].value_counts(dropna=True)
    print(genders)

    # Display earliest, most recent, and most common year of birth
    earliest_year = int(df["Birth Year"].min())
    print("The Earliest Year of birth: ", earliest_year)

    most_recent = int(df["Birth Year"].max())
    print("Most recent: ", most_recent)
    
    # Ignore if Birth Year is na
    year_stats = df["Birth Year"].value_counts(dropna=True)
    most_common_year_of_birth = year_stats.idxmax()
    print("Most common year of birth:", int(most_common_year_of_birth))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """ Display raw data """
    i = 0
    raw = input("Do you want to view raw data? (yes/no)\n").lower()
    # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns',200)
    
    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df.iloc[i:(i+5)])
            raw = input("Do you want to view raw data? (yes/no)\n").lower()
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def main():
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)
        
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        except BaseException:
            print("The data is invalid!")

if __name__ == "__main__":
	main()
