from tokenize import String
import requests
import json
import os
from subprocess import PIPE, run

RATEAPI = "http://localhost:3002"
USERAPI =  "http://localhost:3001"

class Interact:



    def menu(self):
        print("Rate Skills: An app to find and rank skills")
        s = Skills()
        u = User()
        selection = ''
        print("To get started search for a skill by pressing 3 and typing in a word or two to find a skill")
        print("The search function will return skills that contain the term you input in its name to find specific skills")
        print("Or browse popular skills directly by looking at some trending skills and using option 4")
        print("-------------")
        print("Trending:")
        s.trending()
        print("-------------")

        while selection.lower() != 'q':
                
                print("Menu\n"
                  "1: Add Skill | "
                  "2: Rank Skill | "
                  "3: Search Skills | "
                  "4: View Skill | "
                  "5: register account | "
                  "6: log in | "
                  "q: to exit")

                
                selection = input('Selection: ')

                if selection == "1":
                    name = input('Name: ')
                    print("Added succesfully")
                    if input(f'You added the skill for {name}. Would you like to undo this operation? y/n ') == 'y':
                        print("Skill has not been committed to the database")
                        break
                    s.add_skill(name)
                if selection == "2":
                    id = input('ID: ')
                    ranking = input('Ranking (1-5): ')
                    print(f"Alert: You can only rank a skill. Are you sure you'd like to rank skill {id} with ranking {ranking}?")
                    if input('y/n: ') == 'y':
                        s.rank_skill(id, ranking)
                        print("Ranked succesfully: Rank has been committed to the database")
                if selection == "3":
                    searchTerm = input('Search Term ')
                    s.search_skills(searchTerm)
                if selection == "4":
                    id= input('ID ')
                    s.get_skill(id)

                if selection == "5":
                    username = input('username: ')
                    password = input('password: ')
                    u.register(username, password)
                if selection == "6":
                    username = input('username: ')
                    password = input('password: ')
                    u.validate(username, password)
                print("")
        


class Skills:

    def trending(self):
        searchTerm = ""
        command = ['curl ' + RATEAPI + '/skill/search -d \'{"name": "' +searchTerm+'"}\'']
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        data = json.loads(result.stdout)
        index = 1
        for i in data['skill']:
            if index > 3:
                break
            print(f"{index}: {self.format_skill(i)}")
            index += 1


    def add_skill(self, name):
        command=['curl ' + RATEAPI + '/skill/add -d \'{"name": "' +name+'"}\'']
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        data = json.loads(result.stdout)
        print(f"Skill {name} has been committed to the database. ID: {data['id']}")

    def rank_skill(self, id, ranking):
        command=['curl ' + RATEAPI + '/skill/rank -d \'{"id": "' +id+'", "ranking": ' +str(ranking)+ '}\'']
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)

    def search_skills(self, searchTerm):
        command = ['curl ' + RATEAPI + '/skill/search -d \'{"name": "' +searchTerm+'"}\'']
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        data = json.loads(result.stdout)
        if data['skill']:
            idMap = {}
            index = 1
            for i in data['skill']:
                idMap[str(index)] = i['id']
                print(f"{index}: {self.format_skill(i)}")
                index += 1
            choice = input('Would you like to view the page for any of these skills? Enter n or skill number: ')
            
            if choice != 'n':
                print(idMap[choice])
                self.get_skill(idMap[choice])

        else:
            print(f"Nothing found for the search term: {searchTerm}")

    def get_skill(self, id):
        print(f"id is {id}")
        command=['curl ' + RATEAPI + f'/skill/{id}']
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        data = json.loads(result.stdout)["skill"]
        print(f"{self.format_skill(data)}")
        print("You can rank this skill from here or the home screen.")
        if input("Would you like to rate this skill? y/n ") == "y":
            ranking = input('Ranking (1-5): ')
            self.rank_skill(data['id'], ranking)

    def format_skill(self, skill):
        return f"ID: {skill['id']}  Name: {skill['name']}  Ranking: {self.calculate_ranking(skill['rankings2'])}"

    def calculate_ranking(self, rankings):
        if len(rankings) == 1:
            return 0
        return sum(rankings) / (len(rankings) - 1)


class User:
    def register(self, username, password):
        command=['curl ' + USERAPI + '/user/add -d \'{"username": "' +username+'", "passhash": "' +password+'"}\'']
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if result.returncode:
            print("failed to connect")
            return
        print("Account registered")

    def validate(self, username, password):
        command=['curl ' + USERAPI + '/user/verify -d \'{"username": "' +username+'", "passhash": "' +password+'"}\'']
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if result.returncode:
            print("failed to connect")
            return
        if 'Failed' in result.stdout:
            print('Login attempt failed')
            return
        print('Login success')

def main():
    t1 = Interact()
    t1.menu()

if __name__ == '__main__':
    main()