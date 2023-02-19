import logging
from helper.YoutubeDb import YoutubeDb
from helper.YoutubeData import YoutubeCrawler
import json
import re

def get_yt_channel_url(base_url, url, id=None):
    videos_viewby = "/videos?view=57&sort=dd&flow=grid"

    if url:
        channel_url = f"{base_url}{url}{videos_viewby}"
        return channel_url
    elif id:
        return f'{base_url}/channel/{id}{videos_viewby}'
    else:
        return None


async def get_videos_by_channel(channel_url):
    base_url = "https://www.youtube.com/"
    yt_channel_videos_url = get_yt_channel_url(base_url, channel_url)

    if yt_channel_videos_url is None:
        logging.info("Could not Generate Youtube link")

    try:
        youtube_c = YoutubeCrawler(yt_channel_videos_url)

        yt_uclient = youtube_c.get_webpage()
        yt_page_data = youtube_c.read_webpage(yt_uclient)
        yt_soup_html_data = youtube_c.convert_webpage_to_html(yt_page_data)

        channel_search_list_page = youtube_c.get_webpage()
        yt_channel_videos_read_page = youtube_c.read_webpage(channel_search_list_page)
        yt_channel_videos_page = youtube_c.convert_webpage_to_html(yt_channel_videos_read_page)

        data = re.search(r"var ytInitialData = ({.*?});", yt_channel_videos_page.prettify()).group(1)
        data_json = json.loads(data)
        totalvideolist = data_json['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer']['content'][
            'richGridRenderer']['contents']

        video_list = []
        for vid in totalvideolist:
            video_list.append(vid['richItemRenderer']['content']['videoRenderer']['videoId'])

        return len(video_list)

    except Exception as e:
        logging.error(e)


async def get_video_data(url):

    youtube = YoutubeCrawler(url)

    yt_uclient = youtube.get_webpage()
    yt_page_data = youtube.read_webpage(yt_uclient)
    yt_soup_html_data = youtube.convert_webpage_to_html(yt_page_data)

    all_meta = yt_soup_html_data.find("meta", itemprop="name")

    result = {}

    result['channel_id'] = yt_soup_html_data.find("meta", itemprop="channelId")["content"]
    result['title'] = yt_soup_html_data.find("meta", itemprop="name")["content"]
    result['desc'] = yt_soup_html_data.find("meta", itemprop="description")["content"]
    result['views'] = yt_soup_html_data.find("meta", itemprop="interactionCount")["content"]

    data = re.search(r"var ytInitialData = ({.*?});", yt_soup_html_data.prettify()).group(1)
    data_json = json.loads(data)
    videoPrimaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0][
        'videoPrimaryInfoRenderer']

    videoSecondaryInfoRenderer = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents'][1]['videoSecondaryInfoRenderer']

    likes = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0][
        'segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility'][
        'accessibilityData']['label']
    result['likes'] = likes

    return result


async def save_to_mysql(video_data):
    """
    :param video_data: Pass video data

    Stores passed data into MySQL Database
    """
    logging.info("Database")
    logging.info(video_data)

    host = "ineurondb.cckavecit4n5.ap-northeast-1.rds.amazonaws.com"
    username = "ineuron"
    password = "pwdineuron"

    youtube_db = YoutubeDb()

    # Connect to MySQL Server
    sql_conn, sql_cursor = youtube_db.connect_mysql(host, username, password)

    # Create Database
    db_name = 'youtubeDb'
    youtube_db.create_mysql_db(sql_cursor, db_name)

    # Create Table
    table_name = 'video'
    youtube_db.create_mysql_table(sql_cursor, table_name)

    # Insert Data into table
    youtube_db.insert_mysql_data(sql_conn, sql_cursor, table_name, video_data)