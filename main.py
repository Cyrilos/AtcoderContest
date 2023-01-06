#coding: utf-8
import os 
import requests 
from bs4 import BeautifulSoup as Soup 

# save a task 
def saveTask(taskLink, path = "./"):
  filename = taskLink.split("/")[-1] + ".html"
  with open(path + filename, "w") as taskFile: 
    taskRequest = requests.get(taskLink)
    taskParser = Soup(taskRequest.text, "html.parser")
    taskName = taskParser.find("span", class_="h2").text
    taskFile.write(taskParser.find("div", {"id": "task-statement"}).findNext("span", {"class": "lang-en"}).__str__())
    return {"path": path + filename, "description": taskName}

# save all tasks from a contest 
def saveContest(contestLink):
  contestRequest = requests.get(contestLink + "/tasks")
  contestParser = Soup(contestRequest.text, "html.parser")
  contestName = contestLink.split("/")[-1]
  filename = contestName + "/index.html"

  # creating directory for the contest files
  os.system("mkdir " + contestName)
  os.system("mkdir " + "./" + contestName + "/tasks")

  # saving all tasks 
  tasks = []
  for taskCode in contestParser.find("tbody").findAll("td", class_="text-center no-break"):
    tasks.append(saveTask("https://atcoder.jp" + taskCode.find("a")["href"], "./" + contestName + "/tasks/"))

  # writing contest index file 
  with open(filename, "w") as file:
    file.write(f"<!DOCTYPE html><html><head><title>{contestName}</title><meta charset='utf-8'></head><body><h1>{contestName}</h1><ol>")
    for task in tasks : 
      file.write(f"<li><a href={'./' + '/'.join(task['path'].split('/')[2:])}>{task['description']}</a></li>")
    file.write("</ol></body></html>")


def main():
  saveContest("https://atcoder.jp/contests/agc060")

if __name__ == "__main__":
  main()
