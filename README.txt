458 Final Project
By Sam Levatich

***
ABSTRACT:
***

My project is a game recommender system, similar in concept to what Netflix does 
for movies. It assumes a Netflix-like library of games that every user has 
access to so there's no worry about platform specs or cost, and bases its 
recommendation entirely on what you've liked and what other users have liked, 
classifying games based on user tags.

***
HOW TO RUN:
***

My project runs on the zoo, and all you need to do is follow the text prompts 
after running recommender.py in the interpreter!

The actual recommendation part happens either after you add some games as a new 
user or once you 'log in' and choose recommendation. If you've played a fair 
amount of mainstream games I encourage you to add some games you've enjoyed (and 
some you've hated) to a new user profile. Otherwise log in as one of the 
pre-programmed users (Sam, Billy, Joe, Jae, Max) and see what the recommender 
recommends for them and why!

If you want to see the recommender changing in action, try checking the genres 
of the given result and adding a 10/10 game with some other common genres to 
your profile (most of the data currently in the program has the genres: Action, 
RPG, Adventure, Platformer, and Puzzle) or log in as another user and add the 
game recommended to you but give it a 1/10. The recommendation should change, 
unless your compatibility was super strong!

***
HOW IT WORKS:
***

The database of games is ultimately just a set of Game objects, but I've 
organized them in two filter dictionarys that hold objects of type UserList 
and GameList. This allows you to look at the database from the perspective of 
a user who owns multiple games, or a game that has multiple users, each of whom 
has prehaps reviewed the game and tagged it differently. These List objects have 
methods that allow you to interpret the given fields of a game in a manner 
relevant to the grouping (both types of List, for instance, have a method that 
gets a genre/tag profile, but the User version is interested in returning a 
genre profile weighted by the scores since the profile is used to figure out 
what genres they LIKE rather than what genres they ARE).

The recommender takes into account two primary factors. Each user has a 
genre/tag profile (see userProfile() in the UserList object) that can be 
compared to a game's genre profile (see genreProfile() in GameList object) 
which yields a compatability rating for the game and user based on genre 
(if a user hasn't played any games of the genre they are given a score of the 
constant ADVENTURE, which defaults to 0.5, which is equivalent to having played 
one game of the genre that you rated a perfect score, or two that you rated 
5/10). The game also has an average rating. The recommender multiplies both of 
these results together, with scaling factors defined in global variables 
GENRE_FACTOR and RATING_FACTOR (setting both to 1 works well) to get an overall 
rating for each game, and then returns the highest overall rated game that the 
user doesn't own as the recommendation.

A bit more about this overall rating (since this is really the 'automated 
decision' I'm performing with this 'system'): In effect, the genre compatibility 
involves multiple factors:

Compatibility = Sum over every tag in this game's profile
                (players of this game who thought it was this tag) * 
                (number of games you've played of this genre) * 
                (how much you tend to like this genre)

This multitude of factors helps the overall rating be more accurate in a variety 
of ways. One, it makes sure a fair amount of people have actually played this 
game (by checking how many people thought it was a certain tag rather than a 
percentage). Additionally, by not decreasing the bonus if the same user added 
multiple genres, it also gives boosts to games which share mutiple genres you 
enjoy. It takes both your preferences and the gaming community at large's 
preference into account to come up with the best rating.

The explain function then checks the relative value the genre and rating had in 
generating the recommendation, and explains accordingly. It also lets the user 
know what they're getting into length wise based on the average weighted length 
of the users game profile and the standard deviation of that set.

***
FUTURE WORK:
***

-User Authentication

-Allow for approximate equivalency in determining game and tag group, in 
addition to case insensitivity. Right now "Super Mario Bros" and "Super Mario 
Bros." are considered different games, and "RPG" is distinct from "Role Playing Game"

-The program could get feedback on whether the user liked its recommendations, 
and adjust the globals on a user by user basis depending on those results (maybe 
this user seems more adventurous since it liked those recommendations you made 
in a genre they hadn't heard of, or it's always preferred outcomes where 
avgScore played a bigger role than genre matching)
