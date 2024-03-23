import random
import json
import os

def add_xp(user_id, xp_path='data/rank/xp/user/'):
    if random.random() < 0.1:
        xp_to_add = 10
        user_xp_file = f'{xp_path}{user_id}.json'

        if not os.path.exists(user_xp_file):
            user_data = {'xp': 0, 'level': 1}
        else:
            with open(user_xp_file, 'r') as f:
                user_data = json.load(f)

        user_data['xp'] += xp_to_add

        with open(user_xp_file, 'w') as f:
            json.dump(user_data, f)
        return xp_to_add
    return 0