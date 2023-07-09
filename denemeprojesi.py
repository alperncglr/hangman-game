import random

# Load the hangman images from files
with open('hangman_images.txt', 'r') as file:
    contents = file.read().rstrip()
with open('hangman_images_2.txt', 'r') as file:
    contentss = file.read().rstrip()

HANGMAN_PICS = contents.split('\n\n')
HANGMAN_PICS_2 = contentss.split('\n\n')

# Load the list of words for the game

with open('hangman_words.txt', 'r') as file:
    words = [word.lower() for word in file.read().splitlines()]

def get_player_name(): # Function to get the player's name and surname
    name = ''
    surname = ''
    while not name:
        print("Please enter your name: ")
        name = input().strip() # Remove leading/trailing whitespace
        if not name: #asking for name again if it is empty
            print("Name must be provided. Please try again.")
    while not surname:
        print("Please enter your surname: ")
        surname = input().strip() # Remove leading/trailing whitespace
        if not surname: #asking for surname again if it is empty
            print("Surname must be provided. Please try again.")
    return name.lower(), surname.lower()

name, surname = get_player_name()


def choose_game_type(): # Function to choose the game type (hard or easy)

    while True:
        print("Please choose a game type: Hard or Easy?")
        game_type= input().lower()
        if game_type== "hard" or game_type== "easy":
            return game_type
        else: #if game_typeis something else ask for game_typeagain
            print("Choose Hard or Easy, not anything else")

# Get the game type from the player
game_type= choose_game_type()

# Set the hangman images based on the game type if it is easy or hard
if game_type== "easy":
    pics = HANGMAN_PICS

elif game_type== "hard":
    pics = HANGMAN_PICS_2




def get_random_word(wordList): # Function to choose a random word from the word list
    return random.choice(wordList)


def display_board(missed_letters, correct_letters, secret_word, guessed_words, remaining_word_guesses, pics, true_words,
                 hinted_letters):  # Function to display the game board
    #printing the remain attempts and other things
    print(pics[len(missed_letters)])
    print()
    print("Remanining letter attempts:", (len(pics) - 1) - len(missed_letters))
    print("Remaining word attempts:", (remaining_word_guesses))
    print('Missed letters:', end=' ')
    for letter in missed_letters:
        print(letter + ",", end=' ')
    print(('\nMissed words:'), end=' ')
    for word in guessed_words:
        print(word + ",", end=' ')

    print()

    # Create a list of blanks and filled letters for the secret word
    secret_words = secret_word.split()
    blanks = []
    for word in secret_words:
        if word in true_words:
            blanks.append(word)
        else: #making word hidden
            blanks.extend(['_' if letter not in correct_letters and letter not in hinted_letters else letter for letter in word])
        blanks.append(' ')

    # Remove the last space from the blanks list
    blanks.pop()
    #adding spaces between letters
    print(' '.join(blanks))

# Function to get a hint for the secret word
def get_hint(secret_word, correct_letters, hinted_letters):
    # Get all the letters that have not been guessed or hinted yet
    available_hints = [letter for letter in secret_word if
                       letter not in correct_letters and letter not in hinted_letters and letter.isalpha()]

    # If there are no available hints left, return None
    if not available_hints:
        return None


    # Choose a random letter from the available hints and return it
    return random.choice(available_hints)

# Function to get the player's guess (letter or word)
def get_guess(already_guessed_letters, already_guessed_words, already_hinted_letters):
    while True:
        print('Guess a letter or the a word or "?" for hint')
        guess = input()
        guess = guess.lower()
        if guess == "?": #if player wants to get a hint
            return guess
        if len(guess) == 1: #if guess is a letter
            if guess in already_guessed_letters: #if guessed letter is already guessed
                print('You have already guessed that. Choose again.')
            elif guess in already_hinted_letters: #if guessed letter already given as a hint
                print("You already have that letter by using hint.")
            elif guess not in 'abcdefghijklmnopqrstuvwxyz': #if guess is not one of the letters
                print('Please enter a LETTER.')
            else:
                return guess
        elif len(guess) > 1: #if guess is a word
            if guess in already_guessed_words: #if guessed word is already guessed
                print('You have already guessed that. Choose again.')
            elif any(char.isdigit() for char in guess): #if guess contains any number
                print("Guess can't contain numbers")
            else:
                return guess

#Function to play game again
def play_game_again(current_game_type):
    while True:
        print('Do you want to play again? (yes or no)')
        answer = input().lower()
        if answer == "yes":
            while True:
                print("Please choose a game type: Hard or Easy?") #making player choose a gametype
                new_game_type = input().lower()
                if new_game_type != "hard" and new_game_type != "easy": #if it is not easy or hard asking for it again
                    print("Choose Hard or Easy, not anything else")
                else:
                    return True, new_game_type  # Return the updated game type
        elif answer == 'no':
            return False, None
        else:
            print("Please answer with yes or no:")


    while True:
        play_again, new_game_type = play_game(game_type, HANGMAN_PICS, HANGMAN_PICS_2, words)
        if not play_again:
            break
        game_type= new_game_type if new_game_type else game_type

    # Function the update leaderboard
def update_leaderboard(name, surname, score):
    # Open the leaderboard file in read mode
    with open('leaderboard.txt', 'r') as file:
        leaderboard = file.readlines()

    # Split the lines and convert scores to integers
    leaderboard = [line.strip().split(',') for line in leaderboard]
    leaderboard = [(name.strip(), surname.strip(), int(score)) for name, surname, score in leaderboard]

    # Check if the player already exists in the leaderboard
    player_exists = False
    for i, entry in enumerate(leaderboard):
        if entry[0] == name and entry[1] == surname:
            # If the player exists, update their score if the new score is higher
            if score > entry[2]:
                leaderboard[i] = (name, surname, score)
            player_exists = True
            break

    # If the player doesn't exist, add them to the leaderboard
    if not player_exists:
        leaderboard.append((name, surname, score))

    # Sort the leaderboard based on scores
    leaderboard.sort(key=lambda x: x[2], reverse=True)

    # Open the leaderboard file in write mode to update the contents
    with open('leaderboard.txt', 'w') as file:
        # Write the updated leaderboard to the file
        for entry in leaderboard:
            file.write(f'{entry[0]}, {entry[1]}, {str(entry[2])}\n')


def display_leaderboard():
    # Open the leaderboard file in read mode
    with open('leaderboard.txt', 'r') as file:
        # Read the contents of the file
        leaderboard = file.readlines()

    # Split the lines and convert scores to integers
    leaderboard = [line.strip().split(',') for line in leaderboard]
    leaderboard = [(name, surname, int(score)) for name, surname, score in leaderboard]

    # Sort the leaderboard based on scores
    leaderboard.sort(key=lambda x: x[2], reverse=True)

    # Print the contents of the leaderboard
    for entry in leaderboard:
        print(f'{entry[0]} {entry[1]} {entry[2]}')


def exit_game(user_input):
    # Check if the user entered "xox bye"
    if user_input.lower() == 'xox bye':
        # Exit the game
        print('Goodbye!')
        return True
    return False

def play_game(game_type, HANGMAN_PICS, HANGMAN_PICS_2, words): # Function to play the hangman game
    print('ANIMAL HANGMAN')
    hinted_letters = ''
    missed_letters = ''
    correct_letters = ''
    true_words =[]
    guessed_words = []
    if game_type== "hard":
        remaining_word_guesses = 3
        pics = HANGMAN_PICS_2
    if game_type== "easy":
        remaining_word_guesses = 5
        pics = HANGMAN_PICS
    secret_word =get_random_word(words)
    score = 0
    game_is_done = False
    first_turn = True

    while True:
        # Display the game board
        display_board(missed_letters, correct_letters, secret_word, guessed_words, remaining_word_guesses, pics, true_words, hinted_letters)
        if first_turn: #letting player know about exit feature on the first turn
            print("Enter 'xox bye' at any time to exit the game.")
        first_turn = False

        # Get the player's guess (letter or word)
        guess = get_guess(missed_letters + correct_letters , guessed_words+true_words, hinted_letters)
        if exit_game(guess):
            return False, None  # Return False and None to exit the game

        #getting a hint as a guess
        if guess == '?':
                hint = get_hint(secret_word, correct_letters, hinted_letters)
                if hint:
                    hinted_letters += hint #adding hint to hinted_letters

                    #taking point from player if game type easy or hard and point they lose getting more for every hint they use
                    if game_type== "hard":
                        score -= 5 * len(hinted_letters)
                    elif game_type== "easy":
                        score -= 3  * len(hinted_letters)
                    print(f'The hint is: {hint}')

                    found_all_letters = all(letter in correct_letters + hinted_letters for letter in secret_word if letter.isalpha())
                    if found_all_letters:
                        if len(hinted_letters) == len(set(secret_word.replace(" ", ""))): #penalizing player if they use hint feature for all the letters
                            print("I wasn't born yesterday")
                            score = -1773
                            game_is_done = True
                        else: #if user won the game letting them know
                            print('Yes! The secret word is "' + secret_word + '"! You have won!\nAfter ' +
                              str(len(missed_letters)) + ' missed guesses and ' +
                              str(len(correct_letters)) + ' correct guesses.')
                            game_is_done = True

        #if guess a letter
        if len(guess) == 1:
            if guess in secret_word:
                # adding guess to correct_letters if it is true and giving them point according to their gametype
                if game_type== "hard":
                    correct_letters += guess
                    score += 5
                if game_type== "easy":
                    correct_letters += guess
                    score += 3
                #checking if all the letters or words have been found
                found_all_letters = all(letter in correct_letters + hinted_letters for letter in secret_word if letter.isalpha())
                found_all_words = all(word in true_words for word in secret_word.split())

                #letting player know if they found all the letters
                if found_all_letters:
                    print('Yes! The secret word is "' + secret_word + '"! You have won!\nAfter ' +
                        str(len(missed_letters)) + ' missed guesses and ' +
                        str(len(correct_letters)) + ' correct guesses.')

                    print()
                    game_is_done = True

            else:
                if guess != "?":
                    missed_letters = missed_letters + guess #if guess is wrong adding it to missed_letters
                if len(missed_letters) == len(pics) - 1: #player ran out of guesses
                    display_board(missed_letters, correct_letters, secret_word, guessed_words, remaining_word_guesses, pics, true_words, hinted_letters)
                    print('You have run out of guesses!\nAfter ' +
                        str(len(missed_letters)) + ' missed guesses and ' +
                        str(len(correct_letters)) + ' correct guesses, the word was "' + secret_word + '"')
                    game_is_done = True

        elif guess is not None and len(guess) > 1:
            secret_words = secret_word.split()
            if guess == secret_word:
                hidden_letters_2 = list(
                    set(letter for letter in secret_word if letter not in correct_letters and letter.isalpha()))
                num_hidden_letters_2 = len(hidden_letters_2)
                true_words.append(guess)
                # adding letter in user correct word guess to correct letters and giving user point for each of the hidden words while they guessed word accorindg to their gametype
                for letter in guess:
                    correct_letters += letter
                if game_type == "hard":
                    score += 10 * num_hidden_letters_2
                if game_type == "easy":
                    score += 7 * num_hidden_letters_2
                print(score)
                update_leaderboard(name, surname,score)  # Update the leaderboard when the player guesses the entire secret word in one guess
            else:
                for word in secret_words:
                    if guess == word: #if word guess of player is true
                        hidden_letters_2 = [letter for letter in word if letter not in correct_letters and letter.isalpha()]
                        num_hidden_letters_2 = len(hidden_letters_2)
                        true_words.append(guess)
                        #adding letter in user correct word guess to correct letters and giving user point for each of the hidden words while they guessed word accorindg to their gametype
                        for letter in guess:
                            correct_letters += letter
                        if game_type== "hard":
                            score += 10 * num_hidden_letters_2
                        if game_type== "easy":
                            score += 7 * num_hidden_letters_2
                        print(score)
                found_all_words = all(word in true_words for word in secret_word.split())

            #whenn word guess is wrong
            if guess != secret_word and guess not in secret_words:
                guessed_words.append(guess)
                remaining_word_guesses -= 1 #player's word guessing right is decreasing and taking point from user for their wrong word guesses
                if game_type== "hard":
                    score -= 10
                if game_type== "easy":
                    score -= 5

                if remaining_word_guesses == 0: #checking if player ran out of word guesses
                    display_board(missed_letters, correct_letters, secret_word, guessed_words,
                                 remaining_word_guesses, pics, true_words, hinted_letters)
                    print('You have run out of guesses!\nAfter ' +
                          str(len(missed_letters)) + ' missed guesses and ' +
                          str(len(correct_letters)) + ' correct guesses, the word was "' + secret_word + '"')
                    game_is_done = True

            elif guess == secret_word or found_all_words == True :
                print('Yes! The secret word is "' + secret_word + "! You have won!")


                game_is_done = True
        found_all_letters = all(letter in correct_letters + hinted_letters for letter in secret_word if letter.isalpha())
        found_all_words = all(word in true_words for word in secret_word.split())

        # Check if the game is done
        if game_is_done:
            if found_all_letters or found_all_words or guess == secret_word:
                print(f'Your current score is: {score}')
                if score != -1773:
                    (name, surname, score)

            with open('leaderboard.txt', 'r') as file:
                leaderboard = file.readlines()
                leaderboard = [line.strip().split(',') for line in leaderboard]
                leaderboard = [[name, surname, int(score)] for name, surname, score in leaderboard]
                previous_high_score = 0
                for entry in leaderboard:
                    if entry[0] == name and entry[1] == surname:
                        previous_high_score = entry[2]
                        break

                # Only update the leaderboard if the player's new score is higher than their previous high score
            if score > previous_high_score:
                update_leaderboard(name, surname, score)

            #asking if they wanna see the leaderboard after game is ended
            while True:
                if found_all_letters or found_all_words or guess == secret_word:

                    print('Do you want to view the leaderboard? (yes or no)')
                    answer = input().lower()
                    if answer == 'yes':
                        display_leaderboard()
                        break
                    elif answer != "yes" and answer != "no":
                        print("Please answer with yes or no:")
                    else:
                        break
                else:
                    break
            #checking if player wants to play again or not
            play_again, new_game_type = play_game_again(game_type)
            if play_again:
                game_type=  new_game_type
                if game_type== "hard":
                    remaining_word_guesses = 3
                    pics = HANGMAN_PICS_2
                if game_type== "easy":
                    remaining_word_guesses = 5
                    pics = HANGMAN_PICS
                return play_again, new_game_type
            else:
                print("It was fun. Hope to see you soon <3")
                return False, None


# Start the game
while True:
    play_again, new_game_type = play_game(game_type, HANGMAN_PICS, HANGMAN_PICS_2, words)
    if not play_again:
        break
    game_type= new_game_type
