# .readline() legge solo 1 riga alla volta nel file

print("Leggi solo la prima riga del file:")

my_file_object = open("my-file.txt",  "r")

print(my_file_object.readline())

print("\n")

my_file_object.close()