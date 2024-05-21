from flask import Flask, abort,render_template, request, jsonify, redirect, url_for, session
from function import get_data


#set up the app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'webpage'



@app.route("/", methods=['GET', 'POST'])
def show_index():
    if 'username' not in session:
        return redirect("/login")

    context = {"bool": False, "match_list":[0]}
    return render_template('main.html', **context)

@app.route("/result", methods=['GET', 'POST'])
def get_result():
    value = int(request.form['profit'])

    match_list = get_data(value)
    # match_list = [{'home_name': 'Wellington Phoenix FC', 'away_name': 'Melbourne Victory', 'profit': 0.0712762505215423, 'away_odds': 2.96, 'away': 33.78378378378378, 'away_web': 'matchbook', 'draw_odds': 3.52, 'draw': 28.40909090909091, 'draw_web': 'onexbet', 'home_odds': 2.65, 'home': 37.735849056603776, 'home_web': 'mrgreen'}]
    context = {"bool": True, "matches": match_list}
    return render_template('main.html', **context)


@app.route('/account', methods=['GET', 'POST'])
def check_login():
    if request.form['operation'] == 'login':
        if (len(request.form['password']) == 0
                or len(request.form['username']) == 0):
            abort(400)
        if request.form['password']!= "liguo123" or request.form['username']!= "liguo123":
            abort(403)
        else:
            session['username'] = request.form['username']
            return redirect(url_for('show_index'))

#handle the login functionality
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('show_index'))
    else:
        return render_template("login.html")




if __name__ == "__main__":

  app.directory='./'
  app.run(host='127.0.0.1', port=5000)





