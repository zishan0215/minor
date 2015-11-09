# Minor Project
We have the data of 182 users but it was separated in multiple files. So the first task was to consolidate all the data 
in a single file per user. This task was accomplished by the script create_master.py.

Next up is finding places that are at a distance of 15 meters from each other for 120 users. get_places.py does this for
me. According to the database, there are 1302 such places.
  
Now the next thing to do is to find the strength of each place. One way of doing this is to count the number of times
users visit that place and assign that count as the strength of the place. I think this method is good enough so lets 
go code this up. Also, i don't want to use the entire data of 182 users. So i will only be working with 120 users for now.
This place file has to be a global file as it will include the data of 120 users.

It took around 25 minutes to assign weights to all the places. The next thing to do is create a weighted location - location
graph. So every user that visits a place and then goes to another place, those two places will be connected by the number
of time the users go that place.