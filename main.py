import csv
from math import sqrt

N = 1000 # control number of users using in the experiment


def load_foodDataset():
    with open("food-com-recipes-and-user-interactions/RAW_recipes.csv", 'r') as f:
        reader = csv.reader(f)
        reader_r = list(reader)

        recipes = {}

        for i, row in enumerate(reader_r[1:N + 1]):
            recipes[row[1]] = row[0]

    # Load default preprocessed user data
    with open("food-com-recipes-and-user-interactions/PP_users.csv", 'r') as f:
        reader = csv.reader(f)
        reader_u = list(reader)

        simUsers = {}

        for i, users in enumerate(reader_u[1:N + 1]):
            (userId, techniques, items, n_items, ratings, n_ratings) = users
            simUsers.setdefault(userId, {})
            temp_list = techniques.strip('[').strip(']').split(', ')
            simUsers[userId]['techniques'] = []
            for i in range(58):
                simUsers[userId]['techniques'].append(int(temp_list[i]))
            temp_itemlist = items.strip('[').strip(']').split(', ')
            temp_ratinglist = ratings.strip('[').strip(']').split(', ')
            temp_itemrating = {}
            for i in range(len(temp_itemlist)):
                if (float(temp_ratinglist[i]) == 5.0):
                    temp_itemrating[temp_itemlist[i]] = float(temp_ratinglist[i])
            simUsers[userId]['item_rating'] = temp_itemrating

    return simUsers

def sim_cosine(prefs, p1, p2):
    p1_tech = prefs[p1]['techniques']
    p2_tech = prefs[p2]['techniques']

    sum_of_squares_p1 = sum([pow(p1_tech[item], 2)
                          for item in range(len(p1_tech))])
    sum_of_squares_p2 = sum([pow(p2_tech[item], 2)
                             for item in range(len(p2_tech))])
    sum_of_squares = sum([p1_tech[item] * p2_tech[item]
                          for item in range(len(p1_tech))])
    denominator = sqrt(sum_of_squares_p1 * sum_of_squares_p2)
    try:
        value = sum_of_squares / denominator
    except ZeroDivisionError:
        value = 0
    return value

# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs, p1, p2):
    # Get the list of shared_items
    p1_tech = prefs[p1]['techniques']
    p2_tech = prefs[p2]['techniques']

    # Add up the squares of all the differences
    sum_of_squares = sum([pow(p1_tech[item] - p2_tech[item], 2)
                          for item in range(len(p1_tech))])

    return sqrt(sum_of_squares)


# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, p1, p2):
    # Get the list of mutually rated items
    si = {}
    p1_tech = prefs[p1]['techniques']
    p2_tech = prefs[p2]['techniques']
    for i in range(len(p1_tech)):
        # see whether they have same skill or not
        if p1_tech[i] * p2_tech[i] != 0:
            si[i] = 1

    # print(si)

    # Find the number of elements
    n = len(si)
    # if they have no ratings in common, return 0
    if n == 0: return 0
    # Add up all the preferences
    sum1 = sum([it in p1_tech for it in si])
    sum2 = sum([it in p2_tech for it in si])

    # Sum up the squares
    sum1Sq = sum([pow(it in p1_tech, 2) for it in si])
    sum2Sq = sum([pow(it in p2_tech, 2) for it in si])

    # Sum up the products
    pSum = sum([(it in p1_tech) * (it in p2_tech) for it in si])

    # Calculate Pearson score
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0
    r = num / den

    return r


def topSimilarityPerson(prefs, person, similarity=sim_distance):
    # return a list of Pearson scores between person and other people in prefs in descending order of scores
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    # Sort the list for all users so that the similarity appears in descending order of scores
    scores.sort()
    # reverse the order
    scores.reverse()
    return scores


def calculateSimilarPersons(prefs):
    # precomputes the similarity of users
    result = {}

    personPrefs = prefs
    c = 0
    for person in personPrefs:
        # Status updates for large datasets
        c += 1
        if c % 100 == 0: print("%d / %d" % (c, len(personPrefs)))
        # Find the most similar items to this one
        scores = topSimilarityPerson(personPrefs, person)
        result[person] = scores
    return result


# Gets recommendations for a person by using every similar user's preference
def getRecommendations(prefs, personsim, person):
    simSums = {}
    topPersonsim = dict(zip([user[1] for user in personsim[person]], [user[0] for user in personsim[person]]))

    for user in topPersonsim.keys():
        for key in prefs[user].get('item_rating').keys():
            if topPersonsim[user] > 0:
                simSums.setdefault(key, 0)
                simSums[key] += topPersonsim[user]

    # Create the normalized list
    rankings = [(total, item) for item, total in simSums.items()]
    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings


def hits_eval(itemList, rankedlist, count):
    i = 0
    hits = 0
    for ranked_item in rankedlist[:count]:
        for score, item in itemList:
            if item == ranked_item:
                hits += 1
    return hits / count


simUsers = load_foodDataset()
personsim = calculateSimilarPersons(simUsers)

hits_score_1 = []
hits_score_3 = []
hits_score_5 = []
hits_score_10 = []
hits_score_20 = []
hits_score_50 = []
hits_score_100 = []

for i in range(N):
  itemlist = getRecommendations(simUsers, personsim, str(i))
  hits_score_1.append(
      hits_eval(itemlist, list(simUsers[str(i)]['item_rating'].keys()), 1))
  hits_score_3.append(
    hits_eval(itemlist, list(simUsers[str(i)]['item_rating'].keys()), 3))
  hits_score_5.append(
    hits_eval(itemlist, list(simUsers[str(i)]['item_rating'].keys()), 5))
  hits_score_10.append(
    hits_eval(itemlist, list(simUsers[str(i)]['item_rating'].keys()), 10))
  hits_score_20.append(
    hits_eval(itemlist, list(simUsers[str(i)]['item_rating'].keys()), 20))
  hits_score_50.append(
    hits_eval(itemlist, list(simUsers[str(i)]['item_rating'].keys()), 50))
  hits_score_100.append(
    hits_eval(itemlist, list(simUsers[str(i)]['item_rating'].keys()), 100))
  print('%d / %d calculated' % (i, N))


with open('ehits1.txt', 'w', encoding='utf-8') as f:
  for i in range(N):
    f.write(str(hits_score_1[i]) + ',')
  f.write('\n' + str((sum(hits_score_1) / len(hits_score_1))))
with open('ehits3.txt', 'w', encoding='utf-8') as f:
  for i in range(N):
    f.write(str(hits_score_3[i]) + ',')
  f.write('\n' + str((sum(hits_score_3) / len(hits_score_3))))
with open('ehits5.txt', 'w', encoding='utf-8') as f:
  for i in range(N):
    f.write(str(hits_score_5[i]) + ',')
  f.write('\n' + str((sum(hits_score_5) / len(hits_score_5))))
with open('ehits10.txt', 'w', encoding='utf-8') as f:
  for i in range(N):
    f.write(str(hits_score_10[i]) + ',')
  f.write('\n' + str((sum(hits_score_10) / len(hits_score_10))))
with open('ehits20.txt', 'w', encoding='utf-8') as f:
  for i in range(N):
    f.write(str(hits_score_20[i]) + ',')
  f.write('\n' + str((sum(hits_score_20) / len(hits_score_20))))
with open('ehits50.txt', 'w', encoding='utf-8') as f:
  for i in range(N):
    f.write(str(hits_score_50[i]) + ',')
  f.write('\n' + str((sum(hits_score_50) / len(hits_score_50))))
with open('ehits100.txt', 'w', encoding='utf-8') as f:
  for i in range(N):
    f.write(str(hits_score_100[i]) + ',')
  f.write('\n' + str((sum(hits_score_100) / len(hits_score_100))))

