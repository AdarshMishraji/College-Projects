import wikipedia # for making the connection with the wikipedia database.
import requests.exceptions as reqExcep # this exception is imported to show the user the error message when there is no internet connection.
import nltk # used to filter out the nouns from the user's input.

def secureResponse(str): # modifies the response
    resultantString = str
    resultantString = resultantString.replace('"', '')
    for chars in """!"#$%&'*+/:;<=>?@\^_`|~""":
        resultantString = resultantString.replace(chars, '')
    stack = []
    i = 0
    while True:
        startIndex = endIndex = -1
        try:
            if resultantString[i] in ['[', '(', '{']:
                stack.append(i)
            elif resultantString[i] == ')' and resultantString[stack[-1]] == '(':
                startIndex = stack[-1]
                endIndex = i
                i = stack[-1]
                stack.pop()
            elif resultantString[i] == ']' and resultantString[stack[-1]] == '[':
                startIndex = stack[-1]
                endIndex = i
                i = stack[-1]
                stack.pop()
            elif resultantString[i] == '}' and resultantString[stack[-1]] == '{':
                startIndex = stack[-1]
                endIndex = i
                i = stack[-1]
                stack.pop()
            if not(startIndex ==  -1) and not(endIndex == -1):
                stringToBeDeleted = resultantString[startIndex:endIndex + 1]
                resultantString = resultantString.replace(stringToBeDeleted, '')
            if startIndex == -1 and endIndex == -1:
                i += 1
        except IndexError:
            break
    return resultantString


def getResponse(input, number): # provides response for given input.
    response = None
    tokenized = nltk.word_tokenize(input.lower())
    def isNoun(pos):
        return True if pos[:1] == 'N' else False

    if 'Hi' in tokenized or 'hello' in tokenized or 'hi' in tokenized or 'hello' in tokenized:
        greetingMsg = 'Hi, I am Wikipedia Chatbot. You can ask me anything. Tell me, what you want to search?'
        response = greetingMsg
    elif "thank you" in input or "Thank you" in input or "thanks" in tokenized or "Thanks" in tokenized:
        welcomeMsg = "Your Welcome."
        response = welcomeMsg

    elif "bye" in tokenized or "Bye" in tokenized:
        endingMsg = "Thank You for interacting with me. It is a good conversation with you."
        response = endingMsg

    else:
        nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if isNoun(pos)]
        try:
            response = wikipedia.summary(" ".join(nouns), sentences=number)
            response = secureResponse(response)
        except wikipedia.exceptions.DisambiguationError:
            errorMsg = "Sorry, I'am not having any result for this query. Please change your query or try some different keywords."
            response = errorMsg
        except reqExcep.ConnectionError:
            errorMsg = "Sorry, I am not able to fetch data for you. Please try to connect to a stable internet connection."
            response = errorMsg
        except Exception as er:
            errorMsg = "Sorry, There is an error occured. Please try again."
            print(er)
            response = errorMsg
    responseList = []
    i = 0
    while i < len(response):
        if len(response) - i > 105:
            responseList.append(response[i:i + 105] + '-')
            i = i + 105
        else:
            remLen = len(response) - i
            responseList.append(response[i:i + remLen])
            break
    return responseList
