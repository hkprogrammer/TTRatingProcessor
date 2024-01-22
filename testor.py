from tournament import *
from ratingProcessor import *
import pdfkit

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
    players = open("samplePlayers2.csv")
    
    
    
    
    
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
    players = open("samplePlayers2.csv")
    
    listOfPlayers = []
    next(players)
    for line in players:
        l = line.strip().split(",")
        player = Player(l[0], int(l[2]), l[1])
        listOfPlayers.append(player)
        
        
    november = Tournament("UCITT November Open", "", "", listOfPlayers)
    november.importFile(t3)
    generateRatingReport(november)
    generatePDF(november)
    
    december = Tournament("UCITT December Open", "", "", listOfPlayers)
    december.importFile(t)
    generateRatingReport(december)
    generatePDF(december)
    
    winterTryout = Tournament("UCITT 2024 Winter Tryouts", "", "", listOfPlayers)
    winterTryout.importFile(t2)
    generateRatingReport(winterTryout)
    generatePDF(winterTryout)
    
    
    
    t.close()
    t2.close()
    t3.close()
    
    
    
def calculateRating(tournament):
        
    rp = RatingProcessor(tournament)
    rp.calculate()


def generateRatingReport(tournament):
    
    try:
        calculateRating(tournament)
        f = open(f"{tournament.tournamentName}_({tournament.tournamentDate})_RatingReport", "w")
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



def generatePDF(tournament):


    data = ["name,ID,old rating,new rating,change".split(",")]
    activePlayers = tournament.getMatches().keys()
    for player in tournament.getListOfPlayers():
        
        if player.getID() not in activePlayers:
            continue
        
        d = [player.getName(), player.getID(), player.getOriginalRating(), player.getRating(), player.getRating()-player.getOriginalRating()]
        data.append(d)
    
    
    template = generateTemplate(data)
    
    f = open(f"{tournament.tournamentName}_({tournament.tournamentDate})_RatingReport.html","w")
    f.write(template)
    f.close()
    
    
    pdfkit.from_file(f"{tournament.tournamentName}_({tournament.tournamentDate})_RatingReport.html", f"{tournament.tournamentName}_({tournament.tournamentDate})_RatingReport.pdf", configuration= config)
    # pdfkit.from_file(f"{tournament.tournamentName}_({tournament.tournamentDate})_RatingReport.html")
    
    



def generateTemplate(data):
    
    
    format = "<html><table border='1'>"
    
    format += f"<thead><tr>"
    
    for item in data[0]:
        format += f"<th>{item}</th>"
    format += "</tr></thead>"
    
    
    for row in data[1:]:
        format += f"<tr>"
        for item in row:
            
            format += f"<td>{item}</td>"
            
        format += "</tr>"
        
    
    return format + "</table></html>"
    
    
    
    
    
    
    
    
        
        
    
    


if __name__ == "__main__":
    # sampleImportTournament()
    
    
    test()
    