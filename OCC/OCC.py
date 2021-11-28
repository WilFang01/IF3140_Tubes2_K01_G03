from Transaksi import Tx 
import time

def checkformat(schedule_array):
    for i in range (len(schedule_array)):
        word = schedule_array[i]
        first_letter = word[0]

        if (first_letter != "R"):
            if (first_letter != "W"):
                if (first_letter != "C"):
                    return False

        if (first_letter == "R" or first_letter == "W"):
            if (len(word) != 3) :
                return False
            if not(word[1].isnumeric()):
                return False
            if not(word[2].isalpha()):
                return False
        else :
            if (len(word) != 2) :
                return False
            if not(word[1].isnumeric()):
                return False
    return True


def validationTest(j, listOfTransactions) -> bool:
    '''
    If for all Ti with TS (Ti) < TS (Tj) either one of the following condition holds:
        • finishTS(Ti) < startTS(Tj)
        • startTS(Tj) < finishTS(Ti) < validationTS(Tj) and the set of data items written by Ti
        does not intersect with the set of data items read by Tj
    '''

    for i in listOfTransactions:
        if (i.id == j.id):
            continue

        if (i.validationTS == None):
            continue

        if (i.validationTS < j.validationTS):
            if(i.finishTS < j.startTS):
                pass
            elif((j.startTS < i.finishTS) and (i.finishTS < j.validationTS)):
                for var in i.writeVar:
                    if var in j.readVar:
                        return False
            else:
                return False


    return True


def OCC(total_transaction, schedule_array):

    print("Serial Optimistic Concurrency Control :")

    # List All Available Transaction
    listOfTransactions = []
    for i in range (total_transaction):
        tx = Tx(i+1,None,None,None)
        listOfTransactions.append(tx)
    
    # Read Phase
    for i in range (len(schedule_array)):
        print("--Sekarang lagi bagian", schedule_array[i])
        if (schedule_array[i][0] == "R" or schedule_array[i][0] == "W"):
            id = int(schedule_array[i][1]) - 1

            # Kasus timestamp transaksi belum dimulai
            if (listOfTransactions[id].startTS == None):
                print("Inisiasi")
                listOfTransactions[id].startTS = time.time()
            
            if (schedule_array[i][0] == "R"):
                print("Masuk Read")
                listOfTransactions[id].readVar.append(schedule_array[i][2])
            else:
                print("Masuk Write")
                listOfTransactions[id].writeVar.append(schedule_array[i][2])
        
        elif (schedule_array[i][0] == "C"):
            print("Masuk Commit")
            id = int(schedule_array[i][1]) - 1
            listOfTransactions[id].validationTS = time.time()
            # Validation Phase
            validateResult = validationTest(listOfTransactions[id], listOfTransactions)
            # Write Phase
            if (validateResult):
                listOfTransactions[id].finishTS = time.time()
                print(listOfTransactions[id])
                print(f"Transaction with id {id+1} success")
            else:
                print(listOfTransactions[id])
                print(f"Transaction with id {id+1} failed")
                return False
    
    return True

    
def main():
    
    print("Starting Serial Optimistic Concurrency Control (OCC)")
    total_transaction = int(input("Total Transaction : "))

    schedule = []

    total_schedule = int(input("Total Schedule : "))

    print("Format : 'R1X', 'W1X', 'C1'")
    for i in range (total_schedule) :
        print("Schedule", (i+1),": ",end="")
        x = str(input())
        schedule.append(x)

    if not(checkformat(schedule)):
        print("Format Salah !")
    
    if (OCC(total_transaction, schedule)):
        print("Validasi Sukses")
    else :
        print("Validasi Gagal")


if __name__ == '__main__':
    main()