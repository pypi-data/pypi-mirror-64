"""Main module."""

import pandas
import psycopg2

from pymongo import MongoClient


def read_rs_query(query, db_config):
    """
    Returns a dataframe with the result from the query
    :param query: Query string
    :param db_config: configuration for the database in the following pattern:
    db_config = {
        'host': <string>,
        'port': <int>,
        'username': <string>,
        'password': <string>,
        'db': <string>
    }
    :return: A pandas dataframe with the content of the result query
    """
    if type(db_config) != dict:
        raise TypeError('The db_config parameter should be of type dict')
    if type(query) != str:
        raise TypeError('The query parameter should be of type str')

    try:
        connect = psycopg2.connect(**db_config)
    except ConnectionError:
        raise ConnectionError('Unable to connect to database')

    cursor = connect.cursor()
    cursor.execute(query)

    columns_list = [desc[0] for desc in cursor.description]
    data = pandas.DataFrame(cursor.fetchall(), columns=columns_list)

    connect.close()

    return data


def read_mongo_query(db_config):

    mongo_uri = 'mongodb://%s:%s@%s:%s/%s' % (db_config['username'], db_config['password'],
                                              db_config['host'], db_config['port'],
                                              db_config['db'])

    conn = MongoClient(mongo_uri)
