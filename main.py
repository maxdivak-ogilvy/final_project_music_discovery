import sys
from flask import Flask, render_template, flash, url_for, request, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from music import spotify, get_top_five_tracks

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

class ReusableForm(Form):
    name = TextField('Name:', validators=[validators.required()])

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

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
    else:
        name = "Bob Marley"
        # spotify_lookup("RUSH")

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
        similar_err = f""
        return render_template("music.html", name=err, similar=similar_err, form=form)
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

        i=0
        while i < len(similar_results["artists"]):
            similar_artists_names.append(similar_results["artists"][i]["name"])
            similar_artists_URI.append(similar_results["artists"][i]["uri"])
            similar_artists_image.append(similar_results["artists"][i]["images"][0])
            i+=1

        if similar_artists_names==[]:
            similar_artists_notalist = f"Sorry, there's no one quite like {artist_name}!"
        else:
            similar_artists_notalist = str(similar_artists_names)[1:-1] # no brackets

        # print(f"-------\nSimilar_artists is: {similar_artists_notalist}\n-------")

        you_searched_for = f"You searched for: {artist_name}"
        you_may_like_these_bands = f"You should check out: {similar_artists_notalist}"

        print(f"-------\nFirst similar_artists_URI: {similar_artists_URI[0]}\nWhose name is: {similar_artists_names[0]}\n-------")

        get_top_five_tracks(similar_artists_URI[0])

        return render_template("music.html", name=you_searched_for, image_url=artists_photo, similar=you_may_like_these_bands, form=form)

if __name__ == "__main__":
    app.run(debug=True)
