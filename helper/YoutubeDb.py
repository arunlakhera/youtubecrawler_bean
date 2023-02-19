import logging
import pymysql


class YoutubeDb:
    """
    Class for Database operations in MySQL ,MongoDB Amazon S3
    """

    ############ MySQL SECTION ############
    def connect_mysql(self, host, username, password):

        """
        :param host:  MySQL host link
        :param username:  username to connect to MySQL
        :param password: password to connect to MySQL
        :return: sqlconnection & sqlcursor
        """

        try:
            sql_connection = pymysql.connect(host=host, user=username, password=password)
            sql_cursor = sql_connection.cursor()

            logging.info("Connected to MySQL Database...")

            return sql_connection, sql_cursor
        except Exception as e:
            logging.error(e)
            err_msg = f"Error occurred while connecting to MySQL: Check Host/Username/Password"
            logging.info(err_msg)

    def create_mysql_db(self, sql_cursor, db_name):

        """
        :param sql_cursor: Takes sqlcurosr as input
        :return:
        """

        try:
            # Create Database
            sql_createdb = f"CREATE DATABASE IF NOT EXISTS {db_name}"
            sql_cursor.execute(sql_createdb)
            sql_cursor.connection.commit()
            msg = f"Created Database...{db_name}"
            logging.info(msg)

            # Use Database created
            sql_usedb = f"USE {db_name}"
            sql_cursor.execute(sql_usedb)

            msg = f"Using Database...{db_name}"
            logging.info(msg)
        except Exception as e:
            logging.error(e)
            err_msg = f"Error occurred while creating Database: iNeuronDb"
            logging.info(err_msg)

    def create_mysql_table(self, sql_cursor, table_name):
        """

        :param sql_cursor: Takes sqlcursor as input
        :param table_name: Takes table_name for table to create
        :return: Creates table in the database
        """
        try:
            # Create Table
            sql_create_tab = f"CREATE TABLE IF NOT EXISTS {table_name} (video_id VARCHAR(100) NOT NULL, title TEXT, description TEXT, views TEXT, likes TEXT, PRIMARY KEY(video_id))"
            sql_cursor.execute(sql_create_tab)
            msg = f"Created Table...{table_name}"
            logging.info(msg)

        except Exception as e:
            logging.error(e)
            err_msg = f"Error occurred while creating Table: {table_name}"
            logging.info(err_msg)

    def insert_mysql_data(self, sql_conn, sql_cursor, table_name, video_data):
        """

        :param sql_conn: Takes sql_conn as input
        :param sql_cursor: Takes sql_cursor as input
        :param video_data: Takes video_data to be inserted into the table
        :return: Inserts data into the table
        """
        try:
            total_data = f'Total data to Insert: {video_data}'
            logging.info(total_data)

            # Insert Data into Table

            v_id = video_data['channel_id']
            v_title = video_data['title']
            v_desc = video_data['desc']
            normal_string = "".join(ch for ch in v_desc if ch.isalnum())
            v_desc = normal_string
            v_views = video_data['views']
            v_likes = video_data['likes']

            data = (v_id, v_title, v_desc, v_views, v_likes)

            sql_insert = f"""INSERT IGNORE INTO {table_name}(video_id, title, description, views, likes) VALUES(%s, %s, %s, %s, %s)"""

            sql_cursor.execute(sql_insert, data)

            sql_conn.commit()

            sql_count = f'''SELECT COUNT(*) FROM {table_name}'''
            total_inserted = sql_cursor.execute(sql_count)
            total_data_inserted = f'Total data Inserted in Table: {total_inserted}'
            logging.info(total_data_inserted)

        except Exception as e:
            sql_conn.rollback()
            logging.error(e)
            err_msg = f"Error occurred while Inserting Data in Table"
            logging.info(err_msg)

    def close_mysql(self, sql_connection):
        """
        :param sql_connection: Takes sql_connection as input
        :return: Closes the MySQL Connection
        """
        try:
            # Close MySQL Connection
            sql_connection.close()
            logging.info("MySQL Connection...Closed")
        except Exception as e:
            logging.error(e)
            err_msg = f"Error occurred while closing MySQL Connection."
            logging.info(err_msg)
