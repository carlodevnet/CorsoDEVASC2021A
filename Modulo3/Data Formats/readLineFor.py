# È anche possibile scorrere le linee e leggere ogni riga in un ciclo.

print("Scorrere e leggere ogni riga")

my_file_object = open("my-file.txt",  "r")
x = 1

for line in my_file_object:
    print("Line" + str(x) + ": " + line)
    x += 1

my_file_object.close()
