import numpy as np
from typing import List, Tuple

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """
    matches = [()]
    
    # Number of people
    n = len(scores)
    
    # Set score of incompatible gender identity/preference pairs to 0
    for i in range(n):
        for j in range(i+1, n):
            if (gender_id[i] != gender_pref[j]):
                scores[i][j] = 0
                
    # Make preference list for each person. List of n lists of tuples list i is: (compatibility score (i, j), j) where i is fixed
    preference_list = [[()]]
    
    # For ith person
    for i in range(n):
        current_preference_list = [()]
        # Make list of tuples for compatibility scores between (i, j)
        for j in range(n):
            current_preference_list.append((scores[i][j], j))
        # Remove first empty tuple because apparently appending tuples appends to a list that already has an empty tuple?
        current_preference_list.pop(0)
        
        preference_list.append(current_preference_list)
        
    
    # Remove first empty list of tuples because apparently it appends to a list that already has an empty list of tuples?
    preference_list.pop(0)
    
    # Sort each preference list greatest to least score
    for i in range(n):
        preference_list[i].sort(reverse = True)
    
    # Proposer has proposed to 1st to xth choice where x is the element in this list
    last_person_proposed_to = [int(n/2)] * int(n/2)
    
    # List indicating index of match. Index is -1 if unmatched (free)
    temp_match = [-1] * n
    
    # 0th person begins. 0 to n/2 propose, n/2 to n receive
    current_proposer = 0
    
    # Keep making pairs until no one is free
    while (temp_match.count(-1) != 0):
        # If proposer is free
        if(temp_match[current_proposer] == -1):
            x = last_person_proposed_to[current_proposer]
            
            over = False
            while (over != True):
                for i in (x, n):
                    if(over != True):
                    
                        # If receiver is free, match
                        if (temp_match[i] == -1):
                            temp_match[i] = current_proposer
                            temp_match[current_proposer] = i
                            # Increment last_person_proposed_to
                            last_person_proposed_to[current_proposer] += 1
                            over = True
                        
                        # Else if receiver prefers proposer to current match, match them and free current match
                        elif (scores[i][current_proposer] > scores[i][temp_match[i]]):
                            # Free current match
                            current_match = temp_match[i]
                            temp_match[current_match] = -1
                            # Pair receiver and proposer
                            temp_match[i] = current_proposer
                            temp_match[current_proposer] = i
                            # Increment last_person_proposed_to
                            last_person_proposed_to[current_proposer] += 1
                            over = True
                            
                        # Else receiver rejects m (m still free)
                        else:
                            continue
                        
                        print(temp_match)
            
        # Move on to next proposer, make sure index goes from (n/2 - 1) to 0 at edge case when looping back around
        current_proposer += 1
        current_proposer = int(current_proposer % n/2)
    
                
    # Check whether matching is stable (could define separate function)
    is_stable_matching = True
    for i in range(n):
        current_match = temp_match[i]
        for j in range(n):
            if (preference_list[i][j][1] = current_match):
    
    
    # Transfer temp_match to matches
    for i in range(n):
        matches.append((i, temp_match[i]))
                    
            
    
    
    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
