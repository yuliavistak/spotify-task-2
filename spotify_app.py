from flask import Flask, render_template, request, redirect
from spotify_map import main

app = Flask(__name__)
@app.route('/action_page', methods=['POST'])
def do_search():
    name = request.form['artist name']
    map1, song = main(name)

    return render_template('end.html', the_title = f"The most popular is '{song}' ", maps = map1._repr_html_())
@app.route('/')
def entry_page():
    return render_template('start.html')

if __name__ == '__main__':
    app.run(debug = True)
