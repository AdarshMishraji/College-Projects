import wikipedia
import requests
import nltk


def secureResponse(string):
    resultantString = string.replace('"', "")
    try:
        startIndex = resultantString.index('[')
        endIndex = resultantString.index(']')
        stringTobeDeleted = resultantString[startIndex:endIndex + 1]
    except ValueError:
            stringTobeDeleted = ''
    resultantString = resultantString.replace(stringTobeDeleted, '')
    resultantString = resultantString.replace('pronounced', '')
    return resultantString


def getResponse(input):
    def isNoun(pos):
        return True if pos[:1] == 'N' else False

    if 'Hi' in input or 'hello' in input or 'hi' in input or 'hello' in input:
        greetingMsg = 'Hello.'
        return greetingMsg
    elif "thank you" in input or "Thank you" in input:
        welcomeMSg = "Your Welcome."
        return welcomeMSg

    elif "bye" in input or "Bye" in input:
        endingMsg = "Thank You for interacting with me. It is a good conversation with you."
        return endingMsg

    else:
        response = None
        tokenized = nltk.word_tokenize(input.lower())
        nouns = [word for (word, pos) in nltk.pos_tag(
            tokenized) if isNoun(pos)]
        try:
            response = wikipedia.summary(" ".join(nouns), sentences=2)
            response = secureResponse(response)
        except wikipedia.exceptions.DisambiguationError:
            errorMsg = "Sorry!, I'am not having any result for this query. Please change your query or try some different keyword(s)."
            response = errorMsg
        except requests.exceptions.ConnectionError:
            errorMsg = "Sorry! I am not able to fetch data for you. Please try to connect to a stable internet connection."
            response = errorMsg
        except Exception:
            errorMsg = "Sorry! There is an error occured. Please try again."
            response = errorMsg
        return response
