from tournament import *
from ratingProcessor import *
import pdfkit

import datetime

config = pdfkit.configuration(wkhtmltopdf='C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')

def generateReport(listOfPlayers):
    f = open("report.txt","w")
    format = "name,ID,old rating,new rating,change\n"
    for player in listOfPlayers:
        format += f"{player.getName()},{player.getID()},{player.getOriginalRating()},{player.getRating()},{player.getRating()-player.getOriginalRating()}\n"
    
    f.write(format)
    f.close()
    
    

def sampleImportTournament():
    
    t = open("sample1.csv")
    t2 = open("sample2.csv")
    t3 = open("november.csv")
    # t4 = open("november.csv")

    players = open("playerList.csv")
    
    
    
    
    
    listOfPlayers = []
    next(players)
    for line in players:
        l = line.strip().split(",")
        player = Player(l[0], int(l[2]), l[1])
        listOfPlayers.append(player)
        
        
    
    november = Tournament("UCITT November Open", "", "", listOfPlayers)
    november.importFile(t3)
    
    tournament = Tournament("UCITT December Open", "", "", listOfPlayers)
    tournament2 = Tournament("UCITT 2024 Winter Tryouts", "", "", listOfPlayers)
    tournament.importFile(t)
    tournament2.importFile(t2)
    

    
    
    t.close()
    players.close()
    
    rp = RatingProcessor(november)
    rp.calculate()
    
    rp = RatingProcessor(tournament)
    rp.calculate()
    
    rp2 = RatingProcessor(tournament2)
    rp2.calculate()

    generateReport(listOfPlayers)
    
    for player in listOfPlayers:
        print(f"Player: {player.getName()} | oldRating: {player.getOriginalRating()} | newRating: {player.getRating()} | Change: {player.getRating() - player.getOriginalRating()}")    
        
    pass


def test():
    
    t = open("sample1.csv")
    t2 = open("sample2.csv")
    t3 = open("november.csv")
    # t4 = open("november.csv")
    players = open("playerList.csv")
    t4 = open("tournaments/2-2GameNight.csv")
    
    listOfPlayers = []
    next(players)
    for line in players:
        l = line.strip().split(",")
        player = Player(l[0], int(l[2]), l[1])
        listOfPlayers.append(player)
        
        
    november = Tournament("UCITT November Open", "11-19", "", listOfPlayers)
    november.importFile(t3)
    generateRatingReport(november)
    generatePDF(november)
    
    december = Tournament("UCITT December Open", "12-2", "", listOfPlayers)
    december.importFile(t)
    generateRatingReport(december)
    generatePDF(december)
    
    winterTryout = Tournament("UCITT 2024 Winter Tryouts", "1-13 ~ 1-20", "", listOfPlayers)
    winterTryout.importFile(t2)
    generateRatingReport(winterTryout)
    generatePDF(winterTryout)
    
    
    gameNightFeb2 = Tournament("UCITT Thursday Game Night", "2-2-2024", "Game Night", listOfPlayers)
    gameNightFeb2.importFile(t4)
    gameNightFeb2.setSpecialRule(lambda x: 500 if x==0 else -1)
    generateRatingReport(gameNightFeb2)
    generatePDF(gameNightFeb2)
    
    
    generatePDFAllPlayers(listOfPlayers)
    
    
    
    t.close()
    t2.close()
    t3.close()
    t4.close()
    
    
    
def calculateRating(tournament):
        
    rp = RatingProcessor(tournament)
    rp.calculate()


def generateRatingReport(tournament):
    
    try:
        calculateRating(tournament)
        f = open(f"{tournament.tournamentName}_({tournament.tournamentDate})_RatingReport", "w+")
        format = exportPlayerReport(tournament)
        f.write(format)
        f.close()
        
    except Exception as ex:
        raise ex
    
def exportPlayerReport(tournament):
    
    format = "name,ID,old rating,new rating,change\n"
    activePlayers = tournament.getMatches().keys()
    for player in tournament.getListOfPlayers():
        
        if player.getID() not in activePlayers:
            continue
        
        format += f"{player.getName()},{player.getID()},{player.getOriginalRating()},{player.getRating()},{player.getRating()-player.getOriginalRating()}\n"
    
    
    return format





def generatePDFAllPlayers(listOfPlayers):
    data = ["ID,Name,old rating,<b>new rating<b>,change".split(",")]
   
    for player in listOfPlayers:
        
        
        d = [player.getID(), player.getName(),  player.getAbsoluteOriginalRating(), player.getRating(), player.getRating()-player.getAbsoluteOriginalRating()]
        data.append(d)
    
    
    #sorts
    
    data[1:] = list(sorted(data[1:], key=lambda x:x[3], reverse=True))
    

    title = f"All Player Rating Report"
    
    template = generateTemplate(data,title)
    
    f = open(f"All_Player_Rating_Report.html","w+")
    f.write(template)
    f.close()
    
    
    pdfkit.from_file(f"All_Player_Rating_Report.html", f"All_Player_Rating_Report.pdf", configuration= config)
    # pdfkit.from_file(f"{tournament.tournamentName}_({tournament.tournamentDate})_RatingReport.html")
    

def generatePDF(tournament):


    data = ["name,ID,old rating,new rating,change".split(",")]
    activePlayers = tournament.getMatches().keys()
    for player in tournament.getListOfPlayers():
        
        if player.getID() not in activePlayers:
            continue
        
        d = [player.getID() ,player.getName(), player.getOriginalRating(), player.getRating(), player.getRating()-player.getOriginalRating()]
        data.append(d)
    
    
    title = f"{tournament.tournamentName} ({tournament.tournamentDate}) Rating Report"
    
    template = generateTemplate(data,title)
    
    f = open(f"{tournament.tournamentName}_({tournament.tournamentDate})_RatingReport.html","w+")
    f.write(template)
    f.close()
    
    
    pdfkit.from_file(f"{tournament.tournamentName}_({tournament.tournamentDate})_RatingReport.html", f"{tournament.tournamentName}_({tournament.tournamentDate})_RatingReport.pdf", configuration= config)
    # pdfkit.from_file(f"{tournament.tournamentName}_({tournament.tournamentDate})_RatingReport.html")
    
    



def generateTemplate(data,title = ""):
    
    
    format = f"<html> <h1>{title}</h1>"
    
    format += "<table>"
    
    format += f"<thead><tr>"
    
    for item in data[0]:
        format += f"<th>{item}</th>"
    format += "</tr></thead>"
    
    
    for row in data[1:]:
        format += f"<tr>"
        for item in row:
            
            format += f"<td>{item}</td>"
            
        format += "</tr>"
        
        
    format += "<style>table, th, td {border: 1px solid black;border-collapse: collapse;}</style>"
    
    return format + f"</table><p>Generated by UCITT Rating Processor: {datetime.datetime.now()}</p></html>"
    
    
    
    
    
    
    
    
        
        
    
    


if __name__ == "__main__":
    # sampleImportTournament()
    
    
    test()
    