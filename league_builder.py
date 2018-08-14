"""
TechDegree: Python Web developer
Project 1: Build a Soccer league
Date: Aug, 2018
"""

import csv

# define constant variables
INPUT_CSV = 'soccer_players.csv'
OUTPUT_FILE = 'teams.txt'
TEAM_NAMES = ['Sharks', 'Dragons', 'Raptors']

# for extra credit, a letter template
LETTER_TEMPLATE = """
                  Dear {},
                  We are writing to inform you that {} has recently been assigned to team {}.
                  The first practice will be {}. You are welcome to join and show you support.

                  sincerely
                  lionel Messi
                  League Manager
                  """

PRACTICE_TIME = '7 pm on April 1st 2019'

############################################
##
##           helper functions
##
#############################

def loadPlayers(filename):
    """
    a help function to load csv files for all players
    input parameter: filename, a csv filename
    return: a list of for all players
    """

    # read raw data from a provided csv file
    with open(filename, newline = '') as csvfile:
        all_players = list(csv.DictReader(csvfile, delimiter = ','))

    return all_players


def sortPlayers(player_list):
    """
    a help function to separate players with experience from those without experience
    input parameter: player_list, a list for all players
    return: a dictionary with two keys -- 'experience' and 'no_experience'
    """
    # initial two empty lists for players with experience and wihtou experience
    with_exp, without_exp = [], []

    # iterate the whole player list, one player at a time
    for a_player in player_list:
        # check if the player has experience
        if a_player['Soccer Experience'] == 'YES':
            # append player with experience into the experience player list
            with_exp.append(a_player)
        else:
            # append player without experience into wihtou experience player list
            without_exp.append(a_player)

    return {'experience': with_exp, 'no_experience': without_exp}



def assignTeams(teamnames, players):
    """
    a help function to assign experienced and non-experienced players evenly into each team
    input parameters: 1) teamnames, a list of names for all teams
                      2) players, a dictioanry of all players, categorized by experience level
    return: a dictionary for all teams with assigned players
    """
    # initial a dictionary
    teams = dict()
    # find counts for all experienced and non-experienced players
    num_exp, num_no_exp = len(players['experience']), len(players['no_experience'])
    num_teams = len(teamnames)

    # for slicing purpose, set a pointer as 0 to start with
    pointer = 0
    # iterate through team names
    for a_team in teamnames:
        # create a sub-dictionary for each team
        teams[a_team] = dict()
        # name the team
        teams[a_team]['team_name'] = a_team

        # assign players: each team will get equal numbers of experienced and non-experienced player
        # indices to slice experience players list
        left, right = int(pointer*num_exp/num_teams), int((pointer+1)*num_exp/num_teams)
        # select experienced player by slicing
        teams[a_team]['players'] = players['experience'][left:right]

        # indices to slice non expereince players list
        left, right = int(pointer*num_no_exp/num_teams),int((pointer+1)*num_no_exp/num_teams)
        # append selected non experience player by slicing
        teams[a_team]['players'].extend(players['no_experience'][left:right])


        # update the pointer by 1
        pointer += 1

    return teams


def writeOutput(filename, teams):
    """
    a helper function to write teams and players into a txt file as required
    input parameters: 1) filename, a txt filename
                      2) teams, a dictionary to store teams and players' name
    return: no variable to be returned, just create a txt file with all required info
    """

    # open the output file and use 'a' -- open for writing in an appending fashion
    with open(OUTPUT_FILE, 'a') as output:

        # iterate through individual teams
        for a_team in TEAM_NAMES:

            # write the team name first
            output.write(dict_teams[a_team]['team_name'] + '\n')

            # write players' info through iteration
            for a_player in dict_teams[a_team]['players']:
                # for each player, name, experience and guidians are separated by a comma
                output.write(a_player['Name'] + ', ' + a_player['Soccer Experience'] + ', ' + a_player['Guardian Name(s)'] + '\n')

            # write an empty row by the end of all players of a team
            output.write('\n')


def welcomeLetters(teams):
    """
    a help function to create welcome letters with guardian, player, team information
    input parameter: teams, a dictionary to store all teams and players' data
    return: no variable to return, create a txt file for each player
    """
    # start by iterating each team
    for a_team in TEAM_NAMES:
        # next, iterate each player from the team
        players = teams[a_team]['players']
        for a_player in players:
            # generate output txt filename
            filename = a_player['Name'].replace(' ', '_').lower() + '.txt'   # use .replace() method to replace spaces with underscores
            with open(filename, 'w') as letter_file:
                letter_file.write(LETTER_TEMPLATE.format(a_player['Guardian Name(s)'], a_player['Name'], a_team, PRACTICE_TIME))

####################################################
##
##        code to build a soccer league
##
######################

if __name__ == '__main__':

    # read raw data file
    list_all_players = loadPlayers(INPUT_CSV)

    # sort players by experience level
    dict_players = sortPlayers(list_all_players)

    # assign players to teams, experienced and non-experienced players equally distributed
    dict_teams = assignTeams(TEAM_NAMES, dict_players)

    # write teams and players info into a text file
    writeOutput(OUTPUT_FILE, dict_teams)

    # extra credits, parepare welcome letters for all players
    welcomeLetters(dict_teams)
