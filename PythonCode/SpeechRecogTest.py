# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 20:26:25 2018

@author: Matthew
"""

import speech_recognition as sr
print(sr.__version__)
import random
import time

def getSpeechFromMic(recognizer, mic):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("Recongizer must be a Recognizer Instace")
        
    if not isinstance(mic, sr.Microphone):
        raise TypeError("mic must be a Miocrophone Instance")
    
    with mic as source:
        #Make adjustment to audio input
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    #Response object
    response ={"success": True,
               "error": None,
               "transcription": None
               }
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response



if __name__ == "__main__":
    
    WORDS =["big hamster", "little hammy", "gus"] 
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5
    
    r = sr.Recognizer()
    mic = sr.Microphone()
    
    word = random.choice(WORDS)
    
    
    # format the instructions string
    instructions = (
        "I'm thinking of one of these words:\n"
        "{words}\n"
        "You have {n} tries to guess which one.\n"
    ).format(words=', '.join(WORDS), n=NUM_GUESSES)

    # show instructions and wait 3 seconds before starting the game
    print(instructions)
    #time.sleep(3)

    for i in range(NUM_GUESSES):
        # get the guess from the user
        # if a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their guess again. Do this up
        #     to PROMPT_LIMIT times
        for j in range(PROMPT_LIMIT):
            print('Guess {}. Speak!'.format(i+1))
            guess = getSpeechFromMic(r, mic)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        # show the user the transcription
        print("You said: {}".format(guess["transcription"]))

        # determine if guess is correct and if any attempts remain
        guess_is_correct = guess["transcription"].lower() == word.lower()
        user_has_more_attempts = i < NUM_GUESSES - 1

        # determine if the user has won the game
        # if not, repeat the loop if user has more attempts
        # if no attempts left, the user loses the game
        if guess_is_correct:
            print("Correct! You win!".format(word))
            break
        elif user_has_more_attempts:
            print("Incorrect. Try again.\n")
        else:
            print("Sorry, you lose!\nI was thinking of '{}'.".format(word))
            break