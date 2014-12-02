

def process(data, f):
	i = 1

	for l in data.split("===="):
		s1 = str(i)
		if l != "\n":
			row = l.split(">")
			for w in row[0].split():
				#print w
				s1 += "," + w 
			#print row[1]
			s1 += "," + row[1].replace(" ","")

			print s1
			f1.write(s1)
			i += 1



data = open("raw_emails_ip.txt").read()
f1 = open("training_data_final", "w")

process(data, f1)
f1.close()

data = open("raw_test_emails.txt").read()
f1 = open("test_data_final", "w")

process(data, f1)
f1.close()



