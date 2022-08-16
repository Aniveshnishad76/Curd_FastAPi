string = "absafvbbabdbfbsdasa"

dict = {}

for i in string:
    dict[i] = dict.get(i,0).count()

print(dict)
