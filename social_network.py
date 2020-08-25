# DaeHyun Chung
import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter


practice_graph = nx.Graph()
practice_graph.add_edge("A", "B")
practice_graph.add_edge("A", "C")
practice_graph.add_edge("B", "C")
practice_graph.add_edge("B", "D")
practice_graph.add_edge("C", "D")
practice_graph.add_edge("C", "F")
practice_graph.add_edge("D", "F")
practice_graph.add_edge("D", "E")


assert len(practice_graph.nodes()) == 6
assert len(practice_graph.edges()) == 8


# Test shape of practice graph
assert set(practice_graph.neighbors("A")) == set(["B", "C"])
assert set(practice_graph.neighbors("B")) == set(["A", "D", "C"])
assert set(practice_graph.neighbors("C")) == set(["A", "B", "D", "F"])
assert set(practice_graph.neighbors("D")) == set(["B", "C", "E", "F"])
assert set(practice_graph.neighbors("E")) == set(["D"])
assert set(practice_graph.neighbors("F")) == set(["C", "D"])


def draw_practice_graph(graph):
    """Draw practice_graph to the screen.
    """
    nx.draw_networkx(graph)
    plt.show()


rj = nx.Graph()
rj.add_edge("Nurse", "Juliet")
rj.add_edge("Juliet", "Tybalt")
rj.add_edge("Juliet", "Capulet")
rj.add_edge("Juliet", "Romeo")
rj.add_edge("Juliet", "Friar Laurence")
rj.add_edge("Tybalt", "Capulet")
rj.add_edge("Capulet", "Escalus")
rj.add_edge("Capulet", "Paris")
rj.add_edge("Escalus", "Paris")
rj.add_edge("Escalus", "Mercutio")
rj.add_edge("Escalus", "Montague")
rj.add_edge("Paris", "Mercutio")
rj.add_edge("Mercutio", "Romeo")
rj.add_edge("Romeo", "Friar Laurence")
rj.add_edge("Romeo", "Benvolio")
rj.add_edge("Romeo", "Montague")
rj.add_edge("Montague", "Benvolio")


assert len(rj.nodes()) == 11
assert len(rj.edges()) == 17


# Test shape of Romeo-and-Juliet graph
assert set(rj.neighbors("Nurse")) == set(["Juliet"])
assert set(rj.neighbors("Friar Laurence")) == set(["Juliet", "Romeo"])
assert set(rj.neighbors("Tybalt")) == set(["Juliet", "Capulet"])
assert set(rj.neighbors("Benvolio")) == set(["Romeo", "Montague"])
assert set(rj.neighbors("Paris")) == set(["Escalus", "Capulet", "Mercutio"])
assert set(rj.neighbors("Mercutio")) == set(["Paris", "Escalus", "Romeo"])
assert set(rj.neighbors("Montague")) == set(["Escalus", "Romeo", "Benvolio"])
assert set(rj.neighbors("Capulet")) == \
    set(["Juliet", "Tybalt", "Paris", "Escalus"])
assert set(rj.neighbors("Escalus")) == \
    set(["Paris", "Mercutio", "Montague", "Capulet"])
assert set(rj.neighbors("Juliet")) == \
    set(["Nurse", "Tybalt", "Capulet", "Friar Laurence", "Romeo"])
assert set(rj.neighbors("Romeo")) == \
    set(["Juliet", "Friar Laurence", "Benvolio", "Montague", "Mercutio"])


def draw_rj(graph):
    """Draw the rj graph to the screen and to a file.
    """
    nx.draw_networkx(graph)
    plt.savefig("romeo-and-juliet.pdf")
    plt.show()


def friends(graph, user):
    """Returns a set of the friends of the given user, in the given graph.
    """
    return set(graph.neighbors(user))


assert friends(rj, "Mercutio") == set(['Romeo', 'Escalus', 'Paris'])


def friends_of_friends(graph, user):
    """Returns a set of friends of friends of the given user, in the given
    graph. The result does not include the given user nor any of that user's
    friends.
    """
    friends_friends = set()
    users_friends = friends(graph, user)
    for person in users_friends:
        friends_friends = friends_friends | friends(graph, person)
    friends_friends.remove(user)
    friends_friends = friends_friends - users_friends

    return friends_friends


assert friends_of_friends(rj, "Mercutio") == \
    set(['Benvolio', 'Capulet', 'Friar Laurence', 'Juliet', 'Montague'])


def common_friends(graph, user1, user2):
    """Returns the set of friends that user1 and user2 have in common.
    """
    return friends(graph, user1) & friends(graph, user2)


assert common_friends(practice_graph, "A", "B") == set(['C'])
assert common_friends(practice_graph, "A", "D") == set(['B', 'C'])
assert common_friends(practice_graph, "A", "E") == set([])
assert common_friends(practice_graph, "A", "F") == set(['C'])
assert common_friends(rj, "Mercutio", "Nurse") == set()
assert common_friends(rj, "Mercutio", "Romeo") == set()
assert common_friends(rj, "Mercutio", "Juliet") == set(["Romeo"])
assert common_friends(rj, "Mercutio", "Capulet") == set(["Escalus", "Paris"])


def number_of_common_friends_map(graph, user):
    """Returns a map (a dictionary), mapping a person to the number of friends
    that person has in common with the given user. The map keys are the
    people who have at least one friend in common with the given user,
    and are neither the given user nor one of the given user's friends.
    """
    common_friends_res = {}
    friends_friends = friends_of_friends(graph, user)
    for person in friends_friends:
        count = len(common_friends(graph, user, person))
        common_friends_res[person] = count
    return common_friends_res


assert number_of_common_friends_map(practice_graph, "A") == {'D': 2, 'F': 1}
assert number_of_common_friends_map(rj, "Mercutio") == \
    {'Benvolio': 1, 'Capulet': 2, 'Friar Laurence': 1,
     'Juliet': 1, 'Montague': 2}


def number_map_to_sorted_list(map_with_number_vals):
    """Given map_with_number_vals, a dictionary whose values are numbers,
    return a list of the keys in the dictionary.
    The keys are sorted by the number value they map to, from greatest
    number down to smallest number.
    When two keys map to the same number value, the keys are sorted by their
    natural sort order for whatever type the key is, from least to greatest.
    """
    sorted_by_key = sorted(map_with_number_vals.items(), key=itemgetter(0))
    sorted_items = sorted(sorted_by_key, key=itemgetter(1), reverse=True)
    res = []
    for key, val in sorted_items:
        res.append(key)
    return res


assert number_map_to_sorted_list({"a": 5, "b": 2, "c": 7, "d": 5, "e": 5}) == \
    ['c', 'a', 'd', 'e', 'b']


def recommend_by_number_of_common_friends(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the number of common friends (people
    with the most common friends are listed first).  In the
    case of a tie in number of common friends, the names/IDs are
    sorted by their natural sort order, from least to greatest.
    """
    common_friends = number_of_common_friends_map(graph, user)
    return number_map_to_sorted_list(common_friends)


assert recommend_by_number_of_common_friends(practice_graph, "A") == ['D', 'F']
assert recommend_by_number_of_common_friends(rj, "Mercutio") == \
    ['Capulet', 'Montague', 'Benvolio', 'Friar Laurence', 'Juliet']


def influence_map(graph, user):
    """Returns a map (a dictionary) mapping from each person to their
    influence score, with respect to the given user. The map only
    contains people who have at least one friend in common with the given
    user and are neither the user nor one of the users's friends.
    See the assignment writeup for the definition of influence scores.
    """
    friends_friends = friends_of_friends(graph, user)
    influence_dict = {}

    for person in friends_friends:
        c_friends = common_friends(graph, user, person)
        score = 0
        for common in c_friends:
            num_friends = len(friends(graph, common))
            score += 1 / num_friends
        influence_dict[person] = score

    return influence_dict


assert influence_map(rj, "Mercutio") == \
    {'Benvolio': 0.2, 'Capulet': 0.5833333333333333,
     'Friar Laurence': 0.2, 'Juliet': 0.2, 'Montague': 0.45}


def recommend_by_influence(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the influence score (people
    with the biggest influence score are listed first).  In the
    case of a tie in influence score, the names/IDs are sorted
    by their natural sort order, from least to greatest.
    """
    return number_map_to_sorted_list(influence_map(graph, user))


assert recommend_by_influence(rj, "Mercutio") == \
    ['Capulet', 'Montague', 'Benvolio', 'Friar Laurence', 'Juliet']


print("Problem 4:")
print()


unchanged_list = []
changed_list = []
users = ['Capulet', 'Montague', 'Benvolio', 'Friar Laurence', 'Juliet',
         'Mercutio', 'Nurse', 'Paris', 'Tybalt', 'Escalus', 'Romeo']
for user in users:
    if recommend_by_influence(rj, user) == \
       recommend_by_number_of_common_friends(rj, user):
        unchanged_list.append(user)
    else:
        changed_list.append(user)


print("Unchanged Recommendations:", sorted(unchanged_list))
print("Changed Recommendations:", sorted(changed_list))


facebook = nx.Graph()
myfile = open("facebook-links.txt")
for line in myfile:
    word_list = line.split()
    facebook.add_edge(int(word_list[0]), int(word_list[1]))
myfile.close()
assert len(facebook.nodes()) == 63731
assert len(facebook.edges()) == 817090


print()
print("Problem 6:")
print()


facebook = nx.Graph()
myfile = open("facebook-links-small.txt")
for line in myfile:
    word_list = line.split()
    facebook.add_edge(int(word_list[0]), int(word_list[1]))
users = sorted(facebook.nodes())
for id in users:
    if id % 1000 == 0:
        print(id, "(by number_of_common_friends):",
              recommend_by_number_of_common_friends(facebook, id)[0:10])
myfile.close()


print()
print("Problem 7:")
print()


for id in users:
    if id % 1000 == 0:
        print(id, "(by influence):",
              recommend_by_influence(facebook, id)[0:10])


print()
print("Problem 8:")
print()


same_count = 0
different_count = 0
for id in users:
    if id % 1000 == 0:
        list1 = recommend_by_number_of_common_friends(facebook, id)[0:10]
        list2 = recommend_by_influence(facebook, id)[0:10]
        if list1 == list2:
            same_count += 1
        else:
            different_count += 1
print("Same:", same_count)
print("Different:", different_count)
