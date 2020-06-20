import sys
from flask import (
    flash,
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from wtforms import (
    Form,
    StringField,
    SubmitField,
    TextAreaField,
    TextField,
    validators,
)
from music import get_top_five_tracks, spotify


app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me-to-something-unique'

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])


@app.route("/")
def about():
    return render_template("about.html")

@app.route("/music/<artist>", methods=["GET"])
def get_artist(artist):
    output = get_top_five_tracks(artist)

    try:
        name = output["tracks"][0]["album"]["artists"][0]["name"]
    except IndexError as e:
        print(e)
        name = "Sorry, these guys must suck, No valid songs found"
        print(f"-------\nCan't find artists NAME from TOP 5 !! \n-------")

    return render_template("artist.html", artist=name, tracks=output["tracks"])

@app.route("/music", methods=['GET', 'POST'])
def music():
    musician=""

    form = ReusableForm(request.form)
    print(form.errors)
    if request.method == 'POST':
        musician=request.form['name']

    if form.validate():
        # Save the comment here.
        flash('Hello ' + musician)
    else:
        flash('The form must be filled out. ')

    # musician="bob marley"
    if musician!="":
        name = musician
        # spotify_lookup(str(musician))

        # remove spaes and replace with %20
        print(f"""

-------
-------

Name Searched is: {name}
-------""")

        results = spotify.search(q="artist:"+name,type="artist",limit="5")
        items = results["artists"]["items"]
        # print(f"-------\nItems returned are: {items}\n-------")

        if items==[] or items[0]["images"]==[]:
            #returned nothing so do someting
            print(f"-------\nERROR, try again please: {items}\n-------")
            err = f"Sorry, something went wrong. Could be your spelling?"
            error_photo = "static/img/no-results.jpg"
            similar_err = f""
            return render_template("music.html", name=err, image_url=error_photo, similar=similar_err, form=form)
        else:
            artist_name = items[0]["name"]
            artist_id = items[0]["id"]
            artists_photo = items[0]["images"][0]["url"]
            print(f"-------\nName returned is: {artist_name}")
            print(f"Artist_id is: {artist_id}\n-------")

            similar_results = spotify.artist_related_artists(artist_id)
            # print(f"-------\nsimilar_results is: {similar_results}\n-------")

            similar_artists_names=[]
            similar_artists_URI=[]
            similar_artists_image=[]
            similar_dict={}

            i=0
            while i < len(similar_results["artists"]):

                try:
                    similar_artists_names.append(similar_results["artists"][i]["name"])
                    similar_dict[similar_results["artists"][i]["name"]]=None
                except IndexError as e:
                    print(e)
                    similar_artists_names = None
                    similar_dict[None]=None

                try:
                    similar_artists_URI.append(similar_results["artists"][i]["uri"])
                    similar_dict[similar_results["artists"][i]["name"]]=str(similar_results["artists"][i]["uri"])
                except IndexError as e:
                    print(e)
                    similar_artists_URI = None
                    similar_dict[None]=None

                try:
                    similar_artists_image.append(similar_results["artists"][i]["images"][0])
                except IndexError as e:
                    print(e)
                    similar_artists_image.append("static/img/no-results.jpg")

                i+=1

            if similar_artists_names==[]:
                similar_artists_notalist = f"Sorry, there's no one quite like {artist_name}!"
            else:
                similar_artists_notalist = str(similar_artists_names)[1:-1] # no brackets

            try:
                print(f"-------\nFirst similar_artists_URI: {similar_artists_URI[0]}\nWhose name is: {similar_artists_names[0]}\n-------")
                # get_top_five_tracks(similar_artists_URI[0])
            except IndexError as e:
                print(e)
                print(f"-------\nFirst similar_artists_URI: NO SIMILAR URI\nWhose name is: NO SIMILARS\n-------")

            you_searched_for = f"You searched for: {artist_name}"
            you_may_like_these_bands = f"You should check out: {similar_artists_notalist}"


            return render_template("music.html", name=you_searched_for, image_url=artists_photo, similar=similar_dict, form=form)

    else:
        first_run = ""
        return render_template("music.html", name=first_run, image_url=None, similar=None, form=form)

if __name__ == "__main__":
    app.run(debug=True)
