import Tweets
import csv

tweets = Tweets.read_json_file("results_clean.json")
def categorizar(tweets): #recibe arreglo de tweets
	tweetsandvalues = leercsv('tweetsvalues.csv');
	ids = []
	values = []
	for rows in tweetsandvalues:
		values.append(rows[1])
		ids.append(rows[0])
	palabras = {} #diccionario con palabras y valor {string : dict(int,int)}
	for tweet in tweets:
		#Primero determinamos el valor del tweet
		#print(ids)
		value = values[ids.index(str(tweet.id))]

		for word in (tweet.text.split(" ")):
	 		if word not in palabras:
	 			palabras[word] = {"p":0,"n":0,"-":0} #Crea una nueva palabra en el diccionario
	 		#Ahora añade uno al valor correspontiente
	 		if value == "p":
	 			palabras[word]["p"] = palabras[word]["p"] + 1   
	 		elif value == "n":
	 			palabras[word]["n"] = palabras[word]["n"] + 1   
	 		else:
	 			palabras[word]["-"] = palabras[word]["-"] + 1   
	print (palabras["hola"])

def leercsv(filename):
	datos = []
	with open(filename, "r") as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			datos.append([row[0],row[1]])
	return datos

categorizar(tweets)