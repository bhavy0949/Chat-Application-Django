def calculate_similarity(user1, user2):
    similarity = 0
    interests1 = user1["interests"]
    interests2 = user2["interests"]
    for interest,score in interests1.items():
        if interest in interests2:
            score2 = interests2[interest]
            similarity += abs(score-score2)
        
    return similarity