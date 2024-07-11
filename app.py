from flask import Flask, request, render_template
from playlist import get_playlist_id, get_matching_videos, add_videos_to_playlist

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/playlist', methods=['GET', 'POST'])
def playlist():
    result = ""
    if request.method == 'POST':
       channel_playlist_id = get_playlist_id(request.form['input1'])
       personal_playlist_id = get_playlist_id(request.form['input2'])
       keyword = list(request.form['input3'])
       videos = get_matching_videos(channel_playlist_id,keywords=keyword)

       # assertion to check if videos were successfully added 
       result  = add_videos_to_playlist(your_playlist_id=personal_playlist_id, video_data=videos)
       if result: 
        return render_template('playlist.html', result=result)
       
    
    elif request.method == 'GET':
        return render_template('playlist.html',result = None)


# {% comment %} {% block script %}
# function PrintGo() {

# var playlist-url = document.getElementById("playlist-url").value;
# var personal-url = document.getElementById("personal-url").value;
# var keyword = document.getElementById("keyword").value;


# }
# {% endblock %} {% endcomment %}

if __name__ == "__main__":
    app.run(debug=True)

