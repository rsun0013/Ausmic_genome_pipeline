#!/usr/bin/python3.7
import ausmic
connection = ausmic.db_connection()
cursor = connection.cursor()
cursor.execute("SHOW TABLES;")

print(cursor.fetchall())
print(ausmic.get_col_names("genome",cursor))
#print(ausmic.get_col_names("sample",cursor))
#cursor.execute("INSERT INTO GENOME (idisolate,contigfastalocation,length,contigcount,completeness) VALUES ({},{},{},{},{})".foramt())
#cursor.execute("INSERT INTO genome (idisolate,idpure_culture,n50,contigfastalocation,length,contigcount,completeness) VALUES (1,0,4,'/home',1,1,1);")
#cursor.execute("insert into pure_culture (ausmicc_name,idisolate,freezer_location) values (' test',1,'none')")
#cursor.execute("insert into isolate (isolate_name,idsample,idplate) values ('test',0,1)")
#print(cursor.execute("SELECT * from pure_culture"))
cursor.execute("INSERT INTO genome (genomeID,overlap,cont,completness,pass ,similarity) VALUES ('a',2,1,3,1,20);")
cursor.execute(
    "INSERT INTO genome (genomeID,overlap,cont,completness,pass,similarity) values ({},{},{},{},{},{});".format("'a'", 1,1,1,1,1))

cursor.execute("select * from genome;")
print(cursor.fetchall())
