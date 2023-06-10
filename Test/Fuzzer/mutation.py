import math
import os
import random
import subprocess
import time


file_list = ["./origin/epub/conan_doyle_le_signe_des_quatre.epub",
             "./origin/epub/conan_doyle_une_etude_en_rouge.epub",
             "./origin/epub/doyle_aventures_sherlock_holmes.epub",
             "./origin/epub/doyle_chien_baskerville.epub",
             "./origin/epub/doyle_vallee_de_la_peur_illustre.epub",
             "./origin/fb2/Alices Adventures in Wonderland.fb2",
             "./origin/fb2/Around the World in 28 Languages.fb2",
             "./origin/fb2/famouspaintings.fb2",
             "./origin/fb2.zip/Alices Adventures in Wonderland.fb2.zip",
             "./origin/fb2.zip/Around the World in 28 Languages.fb2.zip",
             "./origin/fb2.zip/famouspaintings.fb2.zip",
             "./origin/mobi/1682561968_scaramouche.mobi",
             "./origin/mobi/1682563129_the-aeneid.mobi",
             "./origin/mobi/1682563997_thus-spake-zarathustra.mobi",
             "./origin/pdf/1560395369_the-notebooks-of-leonardo-da-vinci-complete-by-da-vinci-leonardo.pdf",
             "./origin/pdf/1560998911_the-complete-works-of-william-shakespeare-by-william-shakespeare.pdf",
             "./origin/pdf/1587558410_the-odyssey-by-homer.pdf",
             "./origin/prc/sample3.prc",
             "./origin/prc/sample4.prc",
             "./origin/prc/Symphony No.6 (1st movement).prc"]



app = "C:/Users/32491/AppData/Local/Programs/Python/Python39/python.exe"
software = "C:/Users/32491/Documents/Uni/MA1/Software testing/LectorTesting/lector/__main__.py"

FuzzFactor = 5
num_tests = 10*20000
Success = 0
fail = 0
errors = 0

for i in range (num_tests):
    try :
        #chosing a random file in the list
        file_choice = random.choice(file_list)
        file_name = file_choice.split("/")[2]
        file_name_without_extension = file_name.split(".")[0]
        file_extension = file_name.split(".")[-1]

        #output file's name
        if file_extension == "zip":
            fuzz_output = "output/"+file_extension+"/fuzzed"+file_name_without_extension+str(i)+".fb2.zip"
        else:
            fuzz_output = "output/"+file_extension+"/fuzzed"+file_name_without_extension+str(i)+"."+file_extension
        print("Cases tested until now:",i)
        
        #reading chosen file's byte
        with open(file_choice, 'rb') as f:
            buf = bytearray(f.read())

        #replacing random bytes by random integers
        numwrites = random.randrange(math.ceil((float(len(buf)) / FuzzFactor)))+1
        for j in range(numwrites):
            rbyte = random.randrange(256)
            rn = random.randrange(len(buf))
            buf[rn] = rbyte

        #creating a new file
        with open(fuzz_output, 'wb') as file:
            file.write(buf)

        #openning generated file with our app
        process = subprocess.Popen([app,software,fuzz_output])

        time.sleep(3.5)
        crashed = process.poll()
        if not crashed:
            Success +=1
            process.terminate()
            os.remove("./"+fuzz_output)
        else:
            fail +=1
    except Exception as e:
        errors += 1
        print("Erreur rencontrée:",e)
    print("\nruns:",num_tests, "\nSuccess :", Success,"\nFail :",fail,"\nError :", errors)