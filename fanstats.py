import os
import numpy as np

fanoutMaxSoFar = 0
faninMaxSoFar = 0

command = "ls benchfolder/allfiles > listOfAllBenchFiles.txt"
os.system(command)

file = open("listOfAllBenchFiles.txt", "r")
temp_names = file.readlines()
benchfilenames = []
# remove \n
for all in temp_names:
  benchfilenames.append(all.rstrip())

file.close()

#print(benchfilenames)

print("\n")
print('{:<15}{:^10}{:^10}{:^10}{:^10}'.format("Filename", "|", "Max Fanin", "|", "Max Fanout"))
print("----------------------------------------------------------")


totalAvgFanout = []
totalAvgFanin = []
totalStdFanout = []
totalStdFanin = []
percentFanout = []
percentFanout_temp = []


for files in benchfilenames:
  file = open("run.txt", "w")
  file.write("read_library mcnc.genlib")
  file.write("\n")

  file.write("read benchfolder/allfiles/")
  file.write(files)
  file.write("\n")

  file.write("map")
  file.write("\n")

  file.write("show -g")
  file.write("\n")
  file.close()

  command = "./abc -f run.txt > output.txt"

  os.system(command)

  file = open("output.txt", "r")
  temp = file.readlines()

  file_fanoutStats = open("fanout_stats.txt", "r")
  file_faninStats = open("fanin_stats.txt", "r")

  faninMax_temp = []
  fanoutMax_temp = []
  fanoutStats = []
  faninStats = []

  fanin_temp = file_faninStats.readlines()
  fanin = []
  for val in fanin_temp:
    fanin.append(float(val.rstrip()))

  fanout_temp = file_fanoutStats.readlines()
  fanout = []
  for val in fanout_temp:
      fanout.append(float(val.rstrip()))

  totalAvgFanout.append(np.mean(fanout))
  totalStdFanout.append(np.std(fanout))
  totalAvgFanin.append(np.mean(fanin))
  totalStdFanin.append(np.std(fanin))

  for items in temp:
    if("numFanin: " in items):
      faninMax_temp.append(items)

  for items in temp:
    if("numFanout: " in items):
      fanoutMax_temp.append(items)

  for items in temp:
    if ("(<10)" in items):
      percentFanout_temp.append(items)

  temp1 = faninMax_temp[0].split(" ")
  temp2 = fanoutMax_temp[0].split(" ")
  temp3 = percentFanout_temp[0].split(" ")

  faninMax = int(temp1[-1].rstrip())
  fanoutMax = int(temp2[-1].rstrip())
  percentFanout.append(float(temp3[-1].rstrip()))

  if(faninMax > faninMaxSoFar):
    faninMaxSoFar = faninMax

  if(fanoutMax > fanoutMaxSoFar):
    fanoutMaxSoFar = fanoutMax

  print ('{:<15}{:^10}{:^10}{:^10}{:^10}'.format(files, "|", str(faninMax), "|", str(fanoutMax)))

  file_faninStats.close()
  file_fanoutStats.close()
  file.close()


print("\n")
print ("Average Fanin: " + str(np.mean(totalAvgFanin)))
print ("Average Fanout: " + str(np.mean(totalAvgFanout)))
print ("Average Std Fanout: " + str(np.mean(totalStdFanout)))
print ("Average Std Fanin: " + str(np.mean(totalStdFanin)))
print ("Average Std of Fanout Less than 10: " + str(np.std(percentFanout)))
print ("Average Fanout Less than 10: " + str(np.mean(percentFanout)))

print("\n")
print ("Max Fanin: " + str(faninMaxSoFar))
print ("Max Fanout: " + str(fanoutMaxSoFar))

os.system("rm *.dot")