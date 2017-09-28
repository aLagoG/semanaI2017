import Tweets
import csv
import json

tweets = Tweets.read_json_file("results_clean.json")
def categorizar(tweets): #recibe arreglo de tweets y un csv con los tweets id y su su valor; exporta un diccionario en json con las palabras y sus valores positivos o negativos 
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
	with open("diccionario_valores.json", 'w') as file:
		file.write(json.dumps(palabras))

def analizarTweet(tweet):
	palabras = read_file("diccionario_valores.json")
	polaridadtotal = 0

	sentence = tweet.text.split(" ")
	for word in sentence:
		polaridad = "-"
		confiabilidad = 0
		if word in palabras:
			p = palabras[word]["p"]
			n = palabras[word]["n"]
			neutral = palabras[word]["-"]
			total = p + n + neutral

			if (p > n and p > neutral):
				polaridad = "p"
				confiabilidad = (p*100)/total
			elif (n > p and n > neutral):
				polaridad = "n"
				confiabilidad = (n*100)/total
			else:
				polaridad = "-"
				confiabilidad = neutral/total
		if polaridad == "p":
			polaridadtotal = polaridadtotal + confiabilidad
		elif polaridad == "n":
			polaridadtotal = polaridadtotal - confiabilidad
		#print(word + " : " + polaridad + " : " + str(confiabilidad) + " : " + str(total)+"\n" )
	valor = polaridadtotal/len(sentence)
	if (polaridadtotal > 0):
		print("Polaridad: positiva")
		#print("Confiabilidad: " + str(valor))
	elif(polaridadtotal < 0):
		print("Polaridad: negativa")
		#print("Confiabilidad: " + str(-valor))
	else:
		print("Polaridad: neutra")
		#print("Confiabilidad: " + str(valor))
	return  valor

def analizarTweet2(tweet):
	palabras = read_file("diccionario_valores.json")
	polaridadtotal = 0
	polaridadpositiva = 0
	polaridadnegativa = 0

	sentence = tweet.text.split(" ")
	for word in sentence:
		if word in palabras:
			p = palabras[word]["p"]
			n = palabras[word]["n"]
			neutral = palabras[word]["-"]
			total = p + n + neutral

			polaridadpositiva = polaridadpositiva + (p*100)/total
			polaridadnegativa = polaridadnegativa - (n*100)/total

			polaridadtotal = polaridadpositiva + polaridadnegativa
			
		#print(word + " : " + str(p) + " : " + str(n) + " : " + str(neutral) +"\n" )
	valor = polaridadtotal/len(sentence)
	#print("Polaridad positiva = " + str(polaridadpositiva))
	#print("Polaridad negativa = " + str(polaridadnegativa))
	#print("Polaridad total = " + str(polaridadtotal))
	#print("Valor final = " + str(valor))
	return valor

def analizador(tweets):
	for tweet in tweets:
		print(tweet.text)
		print (str(tweet.id) +" | " + str(analizarTweet(tweet))+ " | "+ str(analizarTweet2(tweet)))
		print()

#Este metodo ya esta en jsonToMap.py
def read_file(filename):
    with open(filename) as f:
        data = json.load(f)
    return data

def leercsv(filename):
	datos = []
	with open(filename, "r") as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in spamreader:
			datos.append([row[0],row[1]])
	return datos

analizador(tweets)