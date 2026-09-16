import csv
from datetime import datetime
def load_valid_rows(file):
    #qui vediamo le righe valide
    valid=[]
    with open(file) as my_file:
        for line in csv.reader(my_file,delimiter=";"):
            if len(line)!=6:
                continue
            try:
                data=datetime.strptime(line[0], "%Y-%m-%d %H:%M")
            except ValueError:
                continue
            if line[1]=="":
                continue
            try:
                line[2]=int(line[2])
                if line[2]<0:
                    continue
                line[3]=int(line[3])
                if line[3]<0:
                    continue
            except ValueError:
                continue
            if line[2]<line[3]:
                continue
            try:
                line[4]=float(line[4])
                if line[4]<0:
                    continue
            except ValueError:
                continue
            if line[5]!="RUNNING" and line[5]!="STOPPED":
                continue
            valid.append(line)
    return valid

def machines_analyzer(machine):
    #trasforma le righe nel giusto dizionario
    machines={}
    for lines in machine:
        if lines[1] not in machines:
            machines[lines[1]]={
            "pieces": 0,
            "defects": 0,
            "defect_rate":0,
            "cycle_time": 0,
            "cycles":0,
            "stop":0
            }
        machines[lines[1]]["pieces"]+=lines[2]
        machines[lines[1]]["defects"]+=lines[3]
        if lines[5]!="STOPPED":
            machines[lines[1]]["cycle_time"]+=lines[4]
            machines[lines[1]]["cycles"]+=1
        else:
            machines[lines[1]]["stop"]+=1
    for m in machines:
        if machines[m]["pieces"]!=0:
            machines[m]["defect_rate"]=machines[m]["defects"]/machines[m]["pieces"]*100
    return machines

def result(analysis):
    #stampa i risultati voluti
    for i in analysis:
        print(i)
        print(f"pieces: {analysis[i]["pieces"]}")
        print(f"defects: {analysis[i]["defects"]}")
        if analysis[i]["pieces"]!=0:
            print(f"defect rate: {analysis[i]["defect_rate"]:.2f}%")
        if analysis[i]["cycles"]!=0:
            print(f"average cycle time: {(analysis[i]["cycle_time"]/analysis[i]["cycles"]):.2f}s")
        if analysis[i]["stop"]==1:
            print(f"this machine has stopped 1 time")
        elif analysis[i]["stop"]>1:
            print(f"This machine has stopped {analysis[i]["stop"]} times")
        
        print()

def save_report(analysis,filename):
    with open(filename,"w") as my_file:
        my_file.write(f"machine;pieces;defects;defect_rate;average_cycle_time;downtime_period\n")
        for machine in analysis:
            string=[machine]
            for info in analysis[machine]:
                if info=="cycle_time":
                    if analysis[machine]["cycles"]!=0:
                        string.append(f"{analysis[machine][info]/analysis[machine]["cycles"]:.2f}s")
                    else:
                        string.append("N/A")
                elif info=="cycles":
                    continue
                elif info=="defect_rate":
                    string.append(f"{analysis[machine][info]:.2f}%")
                else:
                    string.append(str(analysis[machine][info]))
            riga=";".join(string)
            my_file.write(f"{riga}\n")
        print(f"DATA SAVED in {filename}")