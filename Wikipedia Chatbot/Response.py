import wikipedia
import requests.exceptions as reqExcep
import nltk


def secureResponse(string): # modifies the response
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


def getResponse(input): # provides response for given input.
    response = None
    tokenized = nltk.word_tokenize(input.lower())
    def isNoun(pos):
        return True if pos[:1] == 'N' else False

    if 'Hi' in tokenized or 'hello' in tokenized or 'hi' in tokenized or 'hello' in tokenized:
        greetingMsg = 'Hello.'
        return greetingMsg 
    elif "thank you" in input or "Thank you" in input or "thanks" in tokenized or "Thanks" in tokenized:
        welcomeMSg = "Your Welcome."
        return welcomeMSg

    elif "bye" in tokenized or "Bye" in tokenized:
        endingMsg = "Thank You for interacting with me. It is a good conversation with you."
        return endingMsg

    else:
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if isNoun(pos)]
        try:
            response = wikipedia.summary(" ".join(nouns), sentences=2)
            response = secureResponse(response)
        except wikipedia.exceptions.DisambiguationError:
            errorMsg = "Sorry!, I'am not having any result for this query. Please change your query or try some different keyword(s)."
            response = errorMsg
        except reqExcep.ConnectionError:
            errorMsg = "Sorry! I am not able to fetch data for you. Please try to connect to a stable internet connection."
            response = errorMsg
        except Exception:
            errorMsg = "Sorry! There is an error occured. Please try again."
            response = errorMsg
        return response
