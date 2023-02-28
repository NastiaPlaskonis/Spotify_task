from flask import Flask, request, render_template
import spotify_api as api
import geo



db = {}
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html", data=db)


@app.route('/map')
def map():
    return render_template('map.html')


@app.route("/search", methods=["POST"])
def search():
    name = request.form.get("query")
    try:
        artist_id, artist_name = api.get_artist_by_name(name)
    except ValueError as err:
        db.clear()
        return index()
    db['artist_name'] = artist_name
    try:
        track_id, track_name = api.get_most_popular_track(artist_id, 'UA')
        print(track_id)
    except ValueError as err:
        db.clear()
        return index()
    db['track'] = track_name
    markets = api.get_available_markets(track_id)
    db['markets'] = geo.get_geodata(markets)
    
    geo.create_map(db['markets']).save("templates/map.html")
    db['map'] = 'map.html'
    return index()


if __name__ == "__main__":
    app.run()
