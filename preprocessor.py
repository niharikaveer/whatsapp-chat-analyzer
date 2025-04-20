import re
import pandas as pd

def preprocess(data):
    # Step 1: Replace narrow space (U+202F) with regular space
    data = data.replace('\u202f', ' ')

    # Step 2: Adjust regex pattern to match your format: MM/DD/YY, H:MM AM/PM -
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} [AP]M - '

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Step 3: Clean dates (remove ' - ' from end)
    dates = [date.strip(' - ') for date in dates]

    # Step 4: Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Step 5: Parse datetime using correct format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Add extra features
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
