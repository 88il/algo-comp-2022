#!usr/bin/env python3
import json
import sys
import os
from operator import itemgetter
from collections import Counter

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses


# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    # Initialize compatibility to 0
    compatibility = 0
    num_questions = len(users[0].responses)
    num_answer_choices = 5
               
               
    # WEIGHT for gradYear compatibility
    year1 = user1.grad_year
    year2 = user2.grad_year
    # Smaller age gap results in larger gradYear_compatibility
    # Age gap of 0 corresponds to gradYear_compatibility of 1/4... age gap of 4 deducts 1/12 from overall compatibility
    gradYear_compatibility = (3 - abs(year1 - year2)) / 12
    compatibility += gradYear_compatibility
    
    
    # WEIGHT for gender preferences–only add points if preferences agree mutually
    if (user1.preferences[0] == user2.gender and user2.preferences[0] == user1.gender):
        compatibility += 1 / 12
    
    
    # WEIGHT responses based on frequency response is chosen
    # List of lists of length num_questions for response weights based on frequency of response
    response_weights = [[]] * num_questions
    
    for i in range(num_questions):
        # List of responses to question i
        responses_i = []
        for j in range(len(users)):
            # List of responses to question i
            responses_i.append(users[j].responses[i])
        for j in range(num_answer_choices):
            # Frequency of answer j for question i
            freq = Counter(responses_i)[j]
            # Weight is max 1, min 20/(20+12) = 5/8
            weight = num_questions / (num_questions + freq)
            response_weights[i].append(weight)
            
    # Calculate response weights between two users
    sum_weights = 0
    for i in range(num_questions):
        if (user1.responses[i] == user2.responses[i]):
            # If same answer, get corresponding response weight
            sum_weights += response_weights[i][user1.responses[i]]


    # Normalize sum to (0,1)
    compatibility += sum_weights / 20
    
    
    # Max compatibility is 1 + 1/12 + 1/12 = 7 / 6. Normalize:
    compatibilitiy = 6 * compatibility / 7
    
    return compatibility


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
