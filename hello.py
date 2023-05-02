#
#
# from flask import Flask, render_template, request, redirect, url_for, session
# from flask_mysqldb import MySQL
# import os
#
# import MySQLdb.cursors
# import re
# from fuzzywuzzy import process
# import pickle
# import ast
# import requests
# import pandas as pd
# movies = pickle.load(open('model/movies_list.pk1', 'rb'))
# similarity = pickle.load(open('model/similarity.pk1', 'rb'))
#
#
#
# def fetch_poster(movie_id):
#     url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
#         movie_id)
#     data = requests.get(url)
#     data = data.json()
#     poster_path = data['poster_path']
#     full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path
#
#
#
# def fetch_genre(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
#     data = requests.get(url).json()
#     genres = [genre['name'] for genre in data['genres']]
#     return genres
#
#
# def fetch_overview(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
#     data = requests.get(url).json()
#     return data['overview']
#
#
# def fetch_releasedate(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
#     data = requests.get(url).json()
#     return data['release_date']
#
#
# def fetch_cast(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=8265bd1679663a7ea12ac168da84d2e8"
#     data = requests.get(url).json()
#     cast = [member['name'] for member in data['cast'][:3]]
#     return cast
#
#
#
# def fetch_crew(movie_id, job):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=8265bd1679663a7ea12ac168da84d2e8"
#     data = requests.get(url).json()
#     crew_members = [member['name'] for member in data['crew'] if member['job'] == job][:1]
#     if crew_members:
#         return crew_members[0]
#     else:
#         return None
#
# def recommend(movie):
#     index = process.extractOne(movie, movies['title'])[2]
#     print('Movie Selected: ', movies['title'][index], 'index: ', index)
#     print('Searching for recommendations.....')
#     distances = sorted(
#         list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_movie_names = []
#     recommended_movie_posters = []
#     recommended_movie_genres = []
#     recommended_movie_overviews = []
#     recommended_movie_release_dates = []
#     recommended_movie_cast = []
#     recommended_movie_crew = []
#     for i in distances[1:11]:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movie_posters.append(fetch_poster(movie_id))
#         recommended_movie_names.append(movies.iloc[i[0]].title)
#         recommended_movie_genres.append(", ".join(fetch_genre(movie_id)))
#         recommended_movie_overviews.append(fetch_overview(movie_id))
#         recommended_movie_release_dates.append(fetch_releasedate(movie_id))
#         recommended_movie_cast.append(", ".join(fetch_cast(movie_id)))
#         recommended_movie_crew.append("".join(fetch_crew(movie_id, "Director")[0]))
#
#
#     return recommended_movie_names, recommended_movie_posters, recommended_movie_genres, recommended_movie_overviews, recommended_movie_release_dates, recommended_movie_cast, recommended_movie_crew
#
#
# app = Flask(__name__)
# app.secret_key = os.urandom(30)
#
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'user-system'
#
# mysql = MySQL(app)
#
# #
# # @app.route('/')
# # def firstpage():
# #
# #     return render_template('firstpage.html')
# @app.route('/firstpage')
# def firstpage():
#     if 'username' in session:
#         return render_template('firstpage.html')
#     else:
#         return redirect(url_for('login'))
#
# @app.route('/')
# def home():
#     return render_template('index.html')
#
# # @app.route('/')
# # def index():
# #     return redirect(url_for('login'))
#
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     message = ''
#     if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'mobile' in request.form and 'password' in request.form:
#         name = request.form['name']
#         email = request.form['email']
#
#         mobile = request.form['mobile']
#         password = request.form['password']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
#         account = cursor.fetchone()
#
#
#         if account:
#             message = 'Account already exists!'
#         elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$', email):
#             message = 'Invalid Email Address!!'
#         elif not name or not password or not email:
#             message = 'Please fill out the necessary details !!'
#         else:
#             cursor.execute('INSERT INTO user (name, email, mobile, password) VALUES (%s, %s, %s, %s)',
#                            (name, email, mobile, password,))
#             mysql.connection.commit()
#             message = 'You are successfully signed in!!'
#     elif request.method == 'POST':
#         message = 'Please fill out the necessary details !!'
#
#     return render_template('signup.html', message = message)
#
#
# @app.route('/login', methods = ['GET','POST'])
# def login():
#     message = ''
#     if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
#         email = request.form['email']
#
#
#         password = request.form['password']
#         cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         cursor.execute('SELECT * FROM user WHERE email = %s and password = %s',(email,password))
#         user = cursor.fetchone()
#         if user:
#             session['loggedin'] = True
#             session['userid'] =user['userid']
#             session['name'] = user['name']
#             session['email'] = user['email']
#             session['mobile'] = user['mobile']
#             session['password'] = user['password']
#
#             message = "Successfully logged in!!"
#             return render_template('firstpage.html', message = message)
#         else:
#             message = "Please enter valid credentials!!"
#         # if len(user)>0:
#         #     session['userid'] = user[0][0]
#         #     return redirect('/firstpage')
#         # else:
#         #     return redirect('/')
#         form = LoginForm()
#
#         if form.validate_on_submit():
#             user = User.query.filter_by(email=form.email.data).first()
#             if user is not None and user.verify_password(form.password.data):
#                 login_user(user)
#                 return redirect('/profile', name=user.name, email=user.email)
#         return render_template('login.html', form=form)
#
#
#
#     return render_template('login.html', message = message)
#
#
#
# #
# # @app.route('/logout')
# # def logout():
# #     session.pop('loggedin',None)
# #     session.pop('userid',None)
# #     session.pop('email',None)
# #     session.pop('name',None)
# #     session.clear()
# #     return redirect(url_for('login'))
#
# @app.route('/logout')
# def logout():
#     session.pop('loggedin', None)
#     session.pop('userid', None)
#     session.pop('name', None)
#     session.pop('email', None)
#
#     return redirect(url_for('login'))
#
#
#
# @app.route('/about')
# def about():
#     return render_template('about.html')
#
#
# @app.route('/contact')
# def contact():
#     return render_template('contact.html')
#
# # @app.route('/profile')
# # def profile():
# #     return render_template('profile.html')
# @app.route('/profile')
# def profile():
#     # check if user is logged in
#     if 'name' and 'userid' in session:
#         name = session['name']
#         email = session['email']
#         return render_template('profile.html', name = name, email = email)
#     else:
#         return redirect('/login')
#
# @app.route('/recommendation', methods=['GET', 'POST'])
# def recommendation():
#     movie_list = movies['title'].values
#     status = False
#     if request.method == 'POST':
#         try:
#             if request.form:
#                 movies_name = request.form['movies']
#                 status = True
#                 index = process.extractOne(movies_name, movies['title'])[2]
#                 print('Movie Selected: ', movies['title'][index], 'index: ', index)
#                 print('Searching for recommendations.....')
#                 distances = sorted(
#                     list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#                 recommended_movie_names = []
#                 recommended_movie_posters = []
#                 recommended_movie_genres = []
#                 recommended_movie_overviews = []
#                 recommended_movie_releasedates = []
#                 recommended_movie_cast = []
#                 recommended_movie_crew = []
#                 for i in distances[1:11]:
#                     # fetch the movie poster
#                     movie_id = movies.iloc[i[0]].movie_id
#                     recommended_movie_posters.append(fetch_poster(movie_id))
#                     recommended_movie_names.append(movies.iloc[i[0]].title)
#                     recommended_movie_genres.append(", ".join(fetch_genre(movie_id)))
#                     recommended_movie_overviews.append(fetch_overview(movie_id))
#                     recommended_movie_releasedates.append(fetch_releasedate(movie_id))
#                     recommended_movie_cast.append(", ".join(fetch_cast(movie_id)))
#                     recommended_movie_crew.append(fetch_crew(movie_id, "Director"))
#
#
#                 return render_template('recommendation.html', movies_name=recommended_movie_names,poster=recommended_movie_posters, genre=recommended_movie_genres, overview=recommended_movie_overviews, release_date=recommended_movie_releasedates, cast=recommended_movie_cast, crew=recommended_movie_crew, movie_list=movie_list, status=status)
#         except Exception as e:
#             error = {'error': e}
#             return render_template('recommendation.html', error=error, movie_list=movie_list, status=status)
#     else:
#         return render_template('recommendation.html', movie_list=movie_list)
#
#
#
#
#
# if  __name__ == '__main__':
#     app.run(debug=True, port=8888)
# #
# # if len(user)>0:
# #     session['userid'] = user[0][0]
# #     return redirect('/firstpage')
# # else:
# #     return redirect('/')


