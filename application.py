from flask import Flask, request, render_template
import logging
import utilities

application = Flask(__name__)
app = application

logging.basicConfig(filename='youtube.log',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')

ch_data = []

@app.route('/loading')
async def loading():
    """
    :return: loading.html

    Loading message is shown till load_data route finishes loading the data
    """
    return render_template("loading.html")


@app.route('/',  methods=['GET', 'POST'])
@app.route('/home_page', methods=['GET', 'POST'])
async def home_page():
    ch_data.clear()
    if request.method == 'POST':
        return render_template("loading.html")
    return render_template('home.html')


@app.route('/channel_data', methods=['GET', 'POST'])
def channel_data():
    if request.method == 'POST':
        return render_template("channel_data.html", cdata=ch_data)
    else:
        return render_template("channel_data.html", cdata = ch_data)


@app.route('/load_data', methods=['GET', 'POST'])
async def load_data():
    """
    Saves the data being scrapped and stores in Mongo and MySQL Database.
    Once completed its status is sent to the loading.html
    """
    try:

        ineuron_vid = await utilities.get_videos_by_channel('@iNeuroniNtelligence')
        krish_vid = await utilities.get_videos_by_channel('@krishnaik06')
        coll_vid = await utilities.get_videos_by_channel('@CollegeWallahbyPW')
        ch_data.append({"ineuron": ineuron_vid, "krish": krish_vid, "college": coll_vid})

        logging.info(ch_data)
        return True
    except Exception as e:
        logging.error(e)


@app.route("/load_video_detail", methods =["GET", "POST"])
async def load_video_detail():
    if request.method == "POST":
        video_url = ''
        video_url = request.form.get("vid_url")
        video_detail = await utilities.get_video_data(video_url)
        await utilities.save_to_mysql(video_detail)
        return render_template("video_detail.html", detail=video_detail)
    else:
        return render_template("home.html")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

