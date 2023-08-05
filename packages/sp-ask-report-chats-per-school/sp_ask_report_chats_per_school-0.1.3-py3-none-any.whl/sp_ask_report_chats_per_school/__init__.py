__version__ = '0.1.3'
import lh3.api
from datetime import date
from datetime import datetime
from pprint import pprint as print
import pandas as pd
import ask_schools
from ask_schools import school_name, find_school_by_operator_suffix
from ask_schools import find_school_by_queue_or_profile_name
from ask_schools import remove_practice_queues
from ask_schools import get_chats_answered


def remove_columns_from_df(df, columns):
    df.drop(columns, axis=1, inplace=True)
    return df

def convert_to_DataFrame(chat_not_none):

    df = pd.DataFrame(chat_not_none)
    columns = ['duration','reftracker_id',
    'reftracker_url','desktracker_id',
     'desktracker_url','wait',
     'referrer','ip','accepted','protocol'
        ]
    df = remove_columns_from_df(df, columns)

    df['started'] = pd.to_datetime(df['started'])
    df['ended'] = pd.to_datetime(df['ended'])
    df["started_time"] = df['started'].apply(lambda x:x.time())
    df["ended_time"] = None#df['ended'].apply(lambda x:x.time())
    del df['ended_time']
    del df['ended']
    df["guest"] = df['guest'].apply(lambda x:x[0:7])
    df['shift'] =df['started'].dt.hour
    df["school"] = df['queue'].apply(lambda x: find_school_by_queue_or_profile_name(x))
    df["university"] = df['queue'].apply(lambda x: find_school_by_queue_or_profile_name(x))

    return df

def get_nbr_of_chats_per_school_for_this_day(year, month, day):
    client = lh3.api.Client()
    chats = client.chats().list_day(year, month, day)
    chats_this_day = remove_practice_queues(chats)
    chats_answered = get_chats_answered(chats_this_day)
    df = convert_to_DataFrame(chats_answered)

    df = df.groupby('school').count()[['university']]
    df.sort_values(by=['school'])
    del client
    del chats
    del chats_this_day
    del chats_answered
    
    return df

if __name__ == '__main__':
    df = get_nbr_of_chats_per_school_for_this_day(2020,3,11)
    #df.to_excel("per_queue.xlsx", index=True)
    print(df.head(20))