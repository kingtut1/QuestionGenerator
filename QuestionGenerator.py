import random
import csv
import io
class Question:
    templateFile = ""
    answerKey = ""
    correctAnswer = 0
    a = ""
    b = ""
    c = ""
    question = ""
    title = ""
    description = ""
    fileName = ""
    output = ""
    def __init__(self, templateFile, answerKey, nameOfOutput):
        self.templateFile = templateFile
        self.answerKey = answerKey
        self.fileName = nameOfOutput
        self.output = open(nameOfOutput, "w")
    def RandomizeAnswers(self, answer1, answer2, answer3, answer4):
        answersUsed = [answer1, answer2, answer3, answer4]
        order = []
        isNone = False
        while len(answersUsed) > 0:
            x = random.choice(answersUsed)
            #append to the end
            if x == "*None of the above":
                isNone = True
                answersUsed.remove(x)
            #append to    
            else:
                order.append(x)
                answersUsed.remove(x)
        if len(order) == 4:
            order.append("None of the above")
        if isNone == True:
            order.append("*None of the above")
        return order
    def CorrectAnswer(self, line):
        formatted = ""
        if line.rfind("*") != -1:
            formatted = "*" + line.replace("*", "")
            return formatted
        return line
    def ReadHeading(self):
        Heading = []
        with open(self.answerKey) as answerKey:
            file = csv.reader(answerKey, delimiter = ",")
            count = 0
            variableCount = 0
            for lines in file:
                if count < 1:
                    for ch in lines:
                        if ch != "*":
                            Heading.append(ch)
                            variableCount += 1
                        else:
                            break   
                else:
                    break
                count +=1
        for i in range(variableCount, 20):
            Heading.append("")
        return variableCount, Heading
    def GenerateQuestions(self):
        with open(self.answerKey) as answerKey:
            next(answerKey, None)
            file = csv.reader(answerKey, delimiter = ",")
            questionNumber = 1
            variables = []
            variableCount, headerName = self.ReadHeading()
            for lines in file:
                for index in range(len(headerName)):
                    if index == variableCount:
                        break
                    variables.append(lines[index])
                self.correctAnswer = "*" + lines[variableCount]
                self.a = lines[variableCount + 1]
                self.b = lines[variableCount + 2]
                self.c = lines[variableCount + 3]
                with open(self.templateFile) as templateFile:
                    template = templateFile.readlines()
                    titleSet = False
                    for sentence in template:
                        if sentence.split()[0] == "Title:":
                            if sentence.split()[1] != "":
                                titleSet = True
                                self.title = "Title: " + sentence.split()[1] + "-" + format(questionNumber, "03d")
                        elif titleSet == False:
                            self.title = "Title: " + self.fileName + "-" + format(questionNumber, "03d")
                        if sentence.split()[0] == "@":
                            self.description = sentence + "\n"
                        else:
                            self.description = "\n"
                            newSentence = sentence.replace("[" + headerName[0] + "]", variables[0])
                            for x in range(1, variableCount):
                                newSentence = newSentence.replace("[" + headerName[x] + "]", variables[x] )
                            self.question = newSentence
                    variables.clear()
                    orderOfAnswers = self.RandomizeAnswers(self.a, self.b, self.c, self.correctAnswer)
                    self.output.write(
                    self.title + "\n" +
                    str(questionNumber) + ") " + self.question +
                    self.description +
                    self.CorrectAnswer("a. " + orderOfAnswers[0]) + "\n" + 
                    self.CorrectAnswer("b. " + orderOfAnswers[1]) + "\n" +
                    self.CorrectAnswer("c. " + orderOfAnswers[2]) + "\n" +
                    self.CorrectAnswer("d. " + orderOfAnswers[3]) + "\n" +
                    self.CorrectAnswer("e. " + orderOfAnswers[4]) + "\n" + "\n")
                    questionNumber += 1
                    
def main():
    #x = Question("q_template copy.txt", "answerkey (1) copy.csv", "output.txt")
    x = Question("q_FV_withdraw.txt", "FV_withdraw.csv", "output1.txt")
    #x.SetVariables(x.ReadHeading())
    x.GenerateQuestions()
    print("Program done running")
main()              
                
                
    
            
            
        
