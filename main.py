import time
import pandas as pd

CITY_DATA = {1: 'chicago.csv',
             2: 'new_york_city.csv',
             3: 'washington.csv'}


def main():
    print("Good day, Welcome to Bike share, how may we help you today")
    print('Choose city to display Bike share data for...')
    print('1. Chicago')
    print('2. New York City')
    print('3. Washington')

    try:
        selected_city = input('Please enter a valid city number...  ')
        while int(selected_city) not in range(1, 4):
            selected_city = input('Enter a valid city number. e.g 1 for Chicago  ')
        else:
            selected_city = int(selected_city)
            selected_month = choose_month()
            selected_day = choose_day_week()
            dataframe = load_data(selected_city, selected_month, selected_day)
            user_interaction(dataframe)
    except ValueError:
        print('Invalid inputs.\n Restarting app in 5sec....')
        countdown_timer()

#main method that does user interaction
def user_interaction(df):

    """
    Facilitates user interaction by taking inputs and validating them to generate processed data
    Parameter:
        df(Panda dataframe): Dataframe passed in and analysed to processed data
    """

    print(time_stats(df))
    response = input('Press 1 to restart program or Press any key to continue... ')
    if response.strip() == '1':
        countdown_timer()
    else:
        print(station_stats(df))
    response = input('Press 1 to restart program or Press any key to continue... ')
    if response.strip() == '1':
        countdown_timer()
    else:
        print(trip_duration_stats(df))
    response = input('Press 1 to restart program or Press any key to continue... ')
    if response.strip() == '1':
        countdown_timer()
    else:
        print(user_stats(df))

    print('Would you like to see raw data?')
    raw_data_response = input('Enter \'Y\' for Yes or \'N\' for No...  ')
    while raw_data_response.lower() == 'y':
        print(df.head(5).to_json(orient='index', indent=5))
        raw_data_response = input('Press \'Y\' for more or \'N\' to stop...  ')
    else:
        print('Would you like to restart the program or exit the program')
        restart_or_exit = input('Press \'R\' to restart or any other key to exit....  ')
        if restart_or_exit.lower() == 'r':
            countdown_timer()
        else:
            print('Thank you for using bike share, have a lovely day')
            return

# method used in setting a countdown timer for app to reset
def countdown_timer():
    """
    Countdown timer that counts for 5secs before
    restarting app(To prevent user from continuously entering invalid data)
    """
    timer = 5
    while timer:
        minute, sec = divmod(timer, 60)
        display_timer = '{:02d}:{:02d}'.format(minute, sec)
        print(display_timer, end="\r")
        time.sleep(1)
        timer -= 1
    main()


def choose_month():

    """
    Helper method for validating input for month
    :Returns:
        int : user validated selected month(Data always in range 1..7)
    """

    print('Choose a specific month number or choose \'none at all\'')
    print('1. January')
    print('2. February')
    print('3. March')
    print('4. April')
    print('5. May')
    print('6. June')
    print('7. None at all')

    while True:
        try:
            selected_month = int(input('Enter month number..  '))
            while selected_month not in range(1, 8):
                print("Invalid month number entered. Try again")
                selected_month = int(input('Enter month number..  '))
        except ValueError:
            print('Invalid inputs. Month number expected')
            continue
        else:
            return selected_month


def choose_day_week():
    """
        Helper method for validating user input for choosing day of week
        :Returns:
           int: user validated selected day of week(Data always in range 1..8)
        """

    print('Choose a specific day of week')
    print('1. Sunday')
    print('2. Monday')
    print('3. Tuesday')
    print('4. Wednesday')
    print('5. Thursday')
    print('6. Friday')
    print('7. Saturday')
    print('8. None at all')

    while True:
        try:
            selected_day_of_week = int(input('Enter day of week number e.g 1 for Sunday..  '))
            while selected_day_of_week not in range(1, 9):
                print("Invalid number entered. Please try again")
                selected_day_of_week = int(input('Enter month number..  '))
        except ValueError:
            print('Invalid number, try again')
            continue
        else:
            return selected_day_of_week


def load_data(city, month, day):

    """
    Loads data from CSV file to dataframe and apply user selected filters
    :parameter
        city(int): City number selected by user
        month(int): User selected month
        day(int): User selected day
    :return:
        Dataframe : Filtered dataframe based on user inputs
    """

    data = pd.read_csv(CITY_DATA[city])
    data['Start Time'] = pd.to_datetime(data['Start Time'])
    data['month'] = data['Start Time'].dt.month
    data['day'] = data['Start Time'].dt.weekday
    data['hour'] = data['Start Time'].dt.hour

    if month != 7:
        data = data[data['month'] == month]

    if day != 8:
        data = data[data['day'] == day]

    return data


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    :parameter
        df(dataframe): Filtered dataframe where data would be extracted from
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Most common month: %s' % calculate_month(df['month'].mode()[0]))
    # display the most common day of week
    print('Most common day of week: %s' % calculate_day_of_week(df['day'].mode()[0]))
    # display the most common start hour
    print('Most popular hour is the %sth hour of the day' % df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    :parameter
        df(dataframe): Filtered dataframe to extract data from
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most popular start station is: %s' % df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most popular end station is: %s' % df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['start_and_end'] = df['Start Station'] + ' to ' + df['End Station']
    print('Most frequent start destination to end destination is: %s' % df['start_and_end'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    :parameter
        df(dataframe): Filtered dataframe to extract data from
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is: %s' % df['Trip Duration'].sum())

    # display mean travel time
    print('Average total travel time is: %s' % df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users.
    :parameter
        df(dataframe): Filtered dataframe to extract data from
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User types are: \n%s' % df['User Type'].value_counts())
    # Display counts of gender
    if 'Gender' in df.columns:
        print('Gender counts are: \n %s' % df['Gender'].value_counts())
    else:
        print('No available Gender data for Washington')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nEarliest year of birth is: %s' % int(df['Birth Year'].min()))
        print('Most recent year of birth is: %s' % int(df['Birth Year'].max()))
        print('Most common year of birth is: %s' % int(df['Birth Year'].mode()[0]))
    else:
        print('No available data for birth year in Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def calculate_month(month):

    """
    Helper method for mapping month number to readable month string
    :param
        month(int): Month number to be used in generating readable month of the year
    :return:
        String: Readable month of the year e.g January
    """

    switch = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June'
    }
    return switch.get(month)


def calculate_day_of_week(week):
    """
       Helper method for mapping week number to readable month string(weekday starts from sunday(1))
       :param
           month(int): Week number to be used in generating weeks in String
       :return:
           String: Readable week e.g Monday
       """

    switch = {
        1: 'Sunday',
        2: 'Monday',
        3: 'Tuesday',
        4: 'Wednesday',
        5: 'Thursday',
        6: 'Friday',
        7: 'Saturday',
    }
    return switch.get(week)


if __name__ == "__main__":
    main()
