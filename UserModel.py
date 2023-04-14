import json

class UserModel:

    # Constructor
    def __init__(self, username, age):
        self.username = username
        self.age = age
        self.likes = []
        self.dislikes = []

    # Adds likes to the user list
    def updateLikes(self, likes):
        self.likes.extend(likes)

    # Adds dislikes to the user list
    def addDislikes(self, dislikes):
        self.dislikes.extend(dislikes)


    # Updates the JSON dictionary for a user already created
    def updateCredential(self):
        with open('user_data/user_data.json', 'r') as f: # Opens JSON and loads data
            users_list = json.loads(f.read())

        for user in users_list:
            if user['username'] == self.username and user['age'] == self.age:

                # If a like already exists for the user do not add repetitive likes
                existingLikes = user['likes']
                for like in self.likes:
                    if like not in existingLikes:
                        existingLikes.append(like)

                # If a dislike already exists for the user do not add repetitive dislikes
                existingDislikes = user['dislikes']
                for dislike in self.dislikes:
                    if dislike not in existingDislikes:
                        existingDislikes.append(dislike)

        # Format the user in the JSON properly
        users_json = json.dumps(users_list, indent=4, separators=(',', ': '))

        # Write to the JSON
        with open('user_data/user_data.json', 'w') as f:
            f.write(users_json)


    # Create the JSON file for new user
    def createCredentials(self):

        # Opens JSON and loads data
        with open('user_data/user_data.json', 'r') as f:
            users_list = json.loads(f.read())

        # Create dictionary for user
        credentials = {
            'username': self.username,
            'age': self.age,
            'likes': self.likes,
            'dislikes': self.dislikes
        }

        # Create proper format for JSON
        users_list.append(credentials)
        users_json = json.dumps(users_list, indent=4, separators=(',', ': '))

        # Add the user to the JSON file
        with open('user_data/user_data.json', 'w') as f:
            f.write(users_json)


    # Get the user likes and dislikes
    def getPersonalizedRemark(self):
        with open('user_data/user_data.json', 'r') as f:
            users_list = json.loads(f.read())

        likes = []
        dislikes = []

        for user in users_list:
            if user['username'] == self.username:
                likes = user['likes']
                dislikes = user['dislikes']

        return likes, dislikes

