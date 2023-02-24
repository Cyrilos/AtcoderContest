#coding: utf-8

import os
import requests 
from bs4 import BeautifulSoup as Soup

# class for saving locally any contest from 
# the website of atcoder (https://atcoder.jp)

class Atcoder:

  def __init__(self, path = ".\\"):
    # path for saving saved contest 
    if path == ".\\":
      self.path = os.path.abspath(path)
    if(self.path[-1] != "\\"):
        self.path += "\\"

  @staticmethod 
  def changeExponent(data):
    # n^exponent to html exponent element
    newData = ""
    indexToSkip = -1
    for i in range(0, len(data)):
      if(data[i] == "^"):
        newData += "<sup>"
        k = i + 1
        while((data[k]).isdigit()):
          newData += data[k]
          k += 1
        newData += "</sup>"
        indexToSkip = k - 1
        continue

      if(i > indexToSkip):
        newData += data[i]
    return newData
 
  @staticmethod
  def changeIndex(data):
    # index to html index element
    newData = ""
    indexToSkip = -1
    for i in range(0, len(data)):
      if(data[i] == "_"):
        newData += "<sub>" + data[i+1] + "</sub>"
        indexToSkip = i+1
        continue
      if(i == indexToSkip):
        continue
      newData += data[i]
    return newData
  
  @staticmethod 
  def changeSpecialChar(data):
    # writing real special characters
    encodings = [
      {"string": "\\leq", "char": "&le;"},
      {"string": "\\ldots", "char": "&#8943"},
      {"string": "\\vdots", "char": "&#8942"}
    ]
    for item in encodings: 
      data = data.replace(item["string"], " " + item["char"] + " ")
    return data

  # get the name of a contest using a link
  def getContestName(self, contestLink): 
    return contestLink.split("/")[-1]

  # get tasks information of a given contest link 
  def getTasksInformation(self, contestLink):
    contestLink += "/tasks"
    response = requests.get(contestLink)
    parser = Soup(response.text, "html.parser").find("tbody").findAll("tr")
    tasks = [] 

    for trElement in parser: 
      tdElement = trElement.find("td").findNext("td")
      try:
        tasks.append({
          "link": "https://atcoder.jp" + tdElement.a['href'],
          "title": tdElement.a.string
        })
      except: 
        pass

    return tasks

  # saving contest task file 
  def saveTask(self, taskLink, path = ".\\"):
    filePath = os.path.abspath(path)
    fileName = taskLink.split("/")[-1] + ".html"
    if(filePath[-1] != "\\"):
      filePath += "\\"
    response = requests.get(taskLink)
    taskParser = Soup(response.text, "html.parser")
    taskCode = taskParser.find("div", {"id": "task-statement"}).findNext("span", {"class": "lang-en"}).__str__()
    taskCode = Atcoder.changeExponent(Atcoder.changeIndex(Atcoder.changeSpecialChar(taskCode)))
    with open(path + fileName, "w", encoding = "utf-8") as file: 
      file.write(taskCode)

    return fileName

  # save a single contest 
  def save(self, contestLink):
    contestName = self.getContestName(contestLink)
    try: 
      os.mkdir(contestName)
    except: 
      pass

    # creating index.html file and writing in  
    indexFile = open(contestName + "\\index.html", "w")
    indexFile.write("""
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset=\"utf-8\">
        <title>{}</title>
      </head>
      <body>
        <h1>{}</h1>
        <ol>
      """.format(contestName, contestName)
    )

    for task in self.getTasksInformation(contestLink):
      # creating index.html file 
      taskFileName = self.saveTask(task["link"], self.path + contestName + "\\")
      indexFile.write(f"<li><a href=\"{taskFileName}\">{task['title']}</a></li>\n")

    indexFile.write("  </ol>\n</body>\n</html>")
    indexFile.close()

  # save many contests
  def saveAll(self, contestLinksList):
    for contestLink in contestLinksList:
      self.save(contestLink)
