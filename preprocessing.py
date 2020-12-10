import numpy as np
import csv
import collections

#Load default preprocessed recipe data
with open("food-com-recipes-and-user-interactions/PP_recipes.csv", 'r') as f:
  reader = csv.reader(f)
  recipes = list(reader)

#Load default preprocessed user data
with open("food-com-recipes-and-user-interactions/PP_users.csv", 'r') as f:
  reader = csv.reader(f)
  users = list(reader)

all_recipes = dict()

good_recipes = dict() #rating = 5.0

bad_recipes = dict() # rating < 5.0



# u,techniques,items,n_items,ratings,n_ratings

# for i,user in enumerate(users[1:]):
#       all_recipes[i] = [a for a in user[5] if a == '5.0']
#       print(all_recipes)

for i,user in enumerate(users[1:]):
  for j in range(user[i][5]):



