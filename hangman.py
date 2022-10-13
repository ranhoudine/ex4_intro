#################################################################
# FILE : hangman.py
# WRITER : Ran Houdine , ranho , 313261133
# EXERCISE : intro2cs2 ex4 2021
# DESCRIPTION: A program running a game of hangman.
# STUDENTS I DISCUSSED THE EXERCISE WITH: none.
# WEB PAGES I USED: none
#################################################################
import hangman_helper as helper
from collections import Counter

WON_MESSAGE = 'You won the game! '
LOSE_MESSAGE = "You lost the game. The word was "
INVALID_INPUT = "The input introduced is not a valid letter "
ALREADY_GUESSED = "You have already guessed this letter "
PLAY_AGAIN = "Would you like to keep playing? "


def update_word_pattern(word, pattern, letter):
    """
    Updates the pattern with the given input
    :param word: The current word to be guessed
    :param pattern: The current pattern
    :param letter: The current guess of the player
    :return: an updated pattern
    """
    updated_pattern = ''

    if letter in word:
        for i in range(len(word)):
            if pattern[i] != '_':
                updated_pattern += pattern[i]
            elif word[i] == letter:
                updated_pattern += letter
            else:
                updated_pattern += '_'
        return updated_pattern
    return pattern


def input_is_valid(input_type, input_string):
    """
    Checks whether the given hangman input is valid
    :param input_type: HINT, WORD or LETTER
    :param input_string: input
    :return: True if the input is valid. Else otherwise
    """
    if input_type == helper.LETTER and len(input_string) > 1:
        return False
    if input_type == helper.LETTER and not input_string.islower():
        return False
    return True


def run_single_game(words_list, score):
    """
    The function runs an iteration of hangman game
    :param words_list: list of words that could be used
    :param score: starting score for this iteration
    :return: post-iteration score
    """
    word = helper.get_random_word(words_list)
    wrong_guess_list = []
    current_pattern = '_' * len(word)
    points = score
    msg = ""
    while '_' in current_pattern and points > 0:  # while game is still on
        helper.display_state(current_pattern, wrong_guess_list, points, msg)
        input_type, input_string = helper.get_input()
        if input_type == helper.LETTER:
            if not input_is_valid(input_type, input_string):
                msg = INVALID_INPUT
                continue
            if input_string in wrong_guess_list or input_string in current_pattern:
                msg = ALREADY_GUESSED
                continue
            points -= 1
            if input_string in word:
                n = Counter(word)[input_string]
                points += (n * (n + 1) // 2)
                current_pattern = update_word_pattern(word, current_pattern, input_string)
                msg = ""
            else:
                wrong_guess_list.append(input_string)
                msg = ""
        elif input_type == helper.WORD:
            points -= 1
            if input_string == word:
                n = Counter(current_pattern)['_']
                current_pattern = word
                points += (n * (n + 1) // 2)
            msg = ""
        elif input_type == helper.HINT:
            points -= 1
            hintable_words = filter_words_list(words_list, current_pattern, wrong_guess_list)
            words_to_display = []
            if len(hintable_words) > helper.HINT_LENGTH:  # More hints available than required length
                for i in range(helper.HINT_LENGTH):
                    words_to_display.append(hintable_words[i * len(hintable_words) // helper.HINT_LENGTH])
            else:
                words_to_display = hintable_words
            helper.show_suggestions(words_to_display)
            msg = ""
    if points > 0:
        msg = WON_MESSAGE
    else:
        msg = LOSE_MESSAGE + word
    helper.display_state(current_pattern, wrong_guess_list, points, msg)
    return points


def is_hintable(word, pattern, wrong_guess_list):
    """
    Checks if the given word makes a valid hint
    :param word: The word to be checked
    :param pattern: The current pattern
    :param wrong_guess_list: wrong guesses so far
    :return: True if the given word is a valid hint. False otherwise
    """
    if len(word) != len(pattern):  # not too long
        return False
    for letter in word:  # doesn't have letters already guessed
        if letter in wrong_guess_list:
            return False
    for pattern_index in range(len(pattern)):  # revealed letters in pattern match
        if pattern[pattern_index] != '_':
            if pattern[pattern_index] != word[pattern_index]:
                return False
            for word_index in range(len(word)):
                if word[word_index] == pattern[pattern_index] and pattern[word_index] == '_':
                    return False

    return True


def filter_words_list(words, pattern, wrong_guess_list):
    """
    Gets a list of words and creates a new list of words that make valid hints
    :param words: original list of words
    :param pattern: current pattern of the game
    :param wrong_guess_list: list of letters guessed
    :return: a list of words that make valid hints
    """
    new_words_list = []
    for word in words:
        if is_hintable(word, pattern, wrong_guess_list):
            new_words_list.append(word)
    return new_words_list


def main():
    """
    Runs the game.
    :return: None
    """
    words_list = helper.load_words()
    score = helper.POINTS_INITIAL
    keep_playing = True
    games_played = 0
    while keep_playing:
        score = run_single_game(words_list, score)
        games_played += 1
        if score <= 0:  # iteration lost
            keep_playing = helper.play_again("You managed to survive "
                                             + str(games_played) +
                                             " rounds. Would you like to play again?")
            if keep_playing:
                games_played = 0
                score = helper.POINTS_INITIAL
        else:  # iteration won
            keep_playing = helper.play_again("You have played " + str(games_played) +
                                             " rounds. Would you like to keep playing?")


if __name__ == '__main__':
    main()
