# About
This is my base Flask project. It is very basic and still a work in progress and it should go without saying that I work on as and when I have the time to do so. 

My end goal here is an application that taps into the apis of crypto exchanges or crypto aggregators and looks at opportunities(?).

There is a lot of work to be done, and maybe my objective is not to finish this (is anything ever) but to learn how to use Flask as I go along so that eventually I have enough solid building blocks and patterns to build the app I have always wanted to. So if you are reading this just because you have searched github for the crypto keyword sorry, close, but no cigar.

# Feature-list
+ wtforms
+ bootstrap for styling
+ partial html in snippets
+ flask-authenticate
+ use jquery to call api, get result and display in div (triggered by button in a dynamically generated table)
+ display data in inline chart (using peity) after getting values from api
+ datepicker widget in flask-bootstrap
+ charts in flask (https://github.com/mher/chartkick.py)
+ paginate sqlachemy results in generic list form
+ download and read json file, then populate table using sqlalchemy
+ use logging
+ use configuration stored in prod or dev config files (dev.env containing passwords not checked in)
+ set environment variables as config items
+ use blueprints
+ download content in configured urls
+ basic bash scripting, especially setting up virtualenv environment to run flask app cli 

# Meta
I started this project after leaning things in this video https://www.youtube.com/watch?v=8aTnmsDMldY, which I found to be pretty unusable once you dig into it. Instead I bought Miguel Grinberg's latest [flask mega tutorial](https://learn.miguelgrinberg.com/) book and am using that as a reference. USD 15, great bargain for what you end up learning. 

Highly recommended book but having to google a lot of edge-case stuff

Nearly time to start thinking about a ui framework/library. Can't decide between angular or react.

