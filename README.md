# GymBuddy

#### Video Demo: https://youtu.be/rV9LsU1tBLg

#### Description: My final project titled "GymBuddy" is a gym/workout focused website that allows the users to lookup hundreds of exercises that either require some kind of gym equipment or just the bodyweight.

In the static directory I have added all the images that are needed to render the page. Besides that I created the style.css file that has all the CSS content in it and the script.js file that has the javascript functions that help the site to run correctly. The script.js file has a couple of functions that validate the user's input when he signs up on the website, basically checking if the username is shorter than 24 letters and if the password is at least 8 characters and matches the confirmation.

In the templates directory I have created the layout.html that is extended by the other html files and contains the navbar and the footer, index.html that is the main page, the exercises page that renders all the exercises for a certain muscle group, and the individual_exercises.html that renders every particular exercises.

Exercises.db is just the database that contains four tables where I have all the users information and the exercises details such as name, equipment, muscle group, description and images.

db_script.py is where I wrote the script to insert all the data from the datasets into the exercises database. It opens the CSV files and then loops through them inserting each row in the database.

requirements.txt is the file that has all the libraries used for the project.

app.py is where flask is configured, database is connected and where I wrote all the routes for the website. On the root route I have the index page. Here I created the log in and register logic that is submited through a modal window. Whenever the route is reached via POST it checks if it is a sign up or a log in request and then proceeds to execute the code for that specific request. If the user registers his username is sent to the database and the password is hashed and then the user is sent to the index page. The register logic checks if the username is already in the database and if it is, the user is alerted that the username is already taken. If the user logs in a session is created for that user, then he is sent to the index page, and is prompted with an alert that he is loged in, at the same time the navbar changes so that it displays the username of the user and adds a "favourites" list item in the navbar where the user can see his favourited exercises.

The exercises route takes a parameter so that it knows which exercises to display, the parameter is taken via a href and so it queries the database based on the muscle group in the parameter. Each exercise has a star button that when clicked adds the exercise to the users favourites tab. It also has a trashcan button that removes the exercise from favourites when clicked. Each element in the exercise is an anchor that sends the user to the exercises individual page.

The individual page for each exercise displays the description of the exercise , two images, one for the start of the exercise movement and one for the end of the movement as well as some information about the equipment used and the dificulty of the exercise. All of these are queried from the database with a parametere that is taken from the route parameter.

Lastly on the favourites page the user can see his favourited exercises and can remove them the same way he can from the exercises page, by clicking on the trashcan button.

The logout route just clears the session and redirects the user to the root page.
