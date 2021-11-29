# Implementation for Simple Locking (exclusive locks only)
import copy

lockTableList = []
transactionTableList = []
waitingTransactions = []
RL = "readlock"
WL = "writeLock"
inputList = []
A = "Abort "
W = "Waiting"
C = "Committed"
AC = "Active"
returnflag = 1

class transactionTable():
    def __init__(self, transactionID, timestamp, transactionState):
        self.transactionID = transactionID
        self.timestamp = timestamp
        self.transactionState = transactionState
        self.lockedResoures = []
        self.blockedOperation = []
        # self.blockedOperation=blockedOperations

    def changeTransactionState(self, state):
        self.transactionState = state

    def addBlockedOperation(self, operation):
        self.blockedOperation.append(operation)

    def addLockedResource(self, resourceName):
        self.lockedResoures.append(resourceName)

class lockTable:
    def __init__(self, lockedDataItem, transactionID, lockState):
        self.lockedDataItem = lockedDataItem
        self.lockState = lockState
        self.waitingTransactions = []
        self.lockHeldBy = []
        self.lockHeldBy.append(transactionID)

    def addWaitingTransaction(self, transactionID):
        self.waitingTransactions.append(transactionID)

    def addLockHeld(self, transactionID):
        self.lockHeldBy.append(transactionID)

    def changeLockState(self, LS):
        self.lockState = LS


# this method takes a string and returns the digit in that string.
# This wa used in the program to get the transaction number form the input string
def get_digit(str1):
    c = ""
    for i in str1:
        if i.isdigit():
            c += i
    return int(c)


# this method adds a new object to the transactionTableObject every time a new transaction is started
def beginTransaction(str):
    tranNumber = get_digit(str)
    print ("Begin Transaction %d" % (tranNumber))
    temp = int(len(transactionTableList)) + 1
    transactionTableList.append(transactionTable(tranNumber, temp, AC))


# fungsi untuk mengembalikan objek dalam transaksi
def resourcenID(inputLine):
    if inputLine.find("X") != -1:
        resourceName = "X"
    elif inputLine.find("Y") != -1:
        resourceName = "Y"
    elif inputLine.find("Z") != -1:
        resourceName = "Z"
    transactionID = get_digit(inputLine)
    return resourceName, transactionID


# menaruh transaksi id pada transactiontable
def searchTransactionID(transactionID):
    for transaction in transactionTableList:
        if transaction.transactionID == transactionID:
            return transaction


def readLock(inputLine):
    resourceName = resourcenID(inputLine)[0]
    transactionID = resourcenID(inputLine)[1]
    flag = 0
    length = len(lockTableList)
    if length != 0:
        for i in range(0, length):
            if lockTableList[i].lockedDataItem == resourceName:
                flag = 1
                if lockTableList[i].lockState == WL:  # This checks if the resource that's been requested in on a writeLock by any other transaction anfd if thats the case, wound wait is called
                    print("Conflicting Write lock: data item " + resourceName + " is on ReadLock by Transaction %d" %(lockTableList[i].lockHeldBy[0]))
                    print("calling wound-wait mechanism")
                    woundWait(searchTransactionID(transactionID), searchTransactionID(lockTableList[i].lockHeldBy[0]), lockTableList[i], inputLine)
                elif lockTableList[i].lockState == RL:  # if resources is just on readLock, the new transaction is added to the list of transactions that hold a readLock on the resource
                    lockTableList[i].addLockHeld(transactionID)
                    searchTransactionID(transactionID).addLockedResource(resourceName)
                    print("Putting the data item " + resourceName + " on ReadLock by Transaction %d" %(lockTableList[i].lockHeldBy[0]))
        if flag == 0:
            lockTableList.append(lockTable(resourceName, transactionID, RL))  # adding a new resource to the locktable if its not already in the lockTable
            searchTransactionID(transactionID).addLockedResource(resourceName)
            print("Putting the data item " + resourceName + " on ReadLock by Transaction %d" %transactionID)
    else:
        lockTableList.append(lockTable(resourceName, transactionID, RL))
        searchTransactionID(transactionID).addLockedResource(resourceName)
        print("Putting the data item " + resourceName + " on ReadLock by Transaction %d" % (lockTableList[0].lockHeldBy[0]))


def writeLock(inputLine):
    resourceName = resourcenID(inputLine)[0]
    transactionID = resourcenID(inputLine)[1]
    flag = 0
    length = len(lockTableList)
    if length != 0:
        for i in range(0, length):
            if lockTableList[i].lockedDataItem == resourceName:
                flag = 1
                if lockTableList[i].lockState == RL:
                    if len(lockTableList[i].lockHeldBy) == 1:
                        if lockTableList[i].lockHeldBy[
                            0] == transactionID:  # checks to see if the resources is on readLock by the same transaction
                            lockTableList[i].lockState = WL
                            print("Upgrading Readlock to WriteLock on data item " + resourceName + " for transaction %d" %transactionID)
                        else:
                            print("data item " + resourceName + "is on ReadLock by multiple transaction. ")
                            print("call Wound Wait")  # call wound wait if its on readlock by another transaction
                            woundWait(searchTransactionID(transactionID), searchTransactionID(lockTableList[i].lockHeldBy[0]), lockTableList[i], inputLine)
                    else:
                        count = 0
                        for lockedresource in lockTableList:
                            if lockedresource.lockedDataItem == resourceName:
                                for tempheldby in lockedresource.lockHeldBy:
                                    if tempheldby == transactionID:
                                        count += 1
                        # calling wound wait if its on readLock by multiple transactions
                        woundWait(searchTransactionID(transactionID),
                                  searchTransactionID(lockTableList[i].lockHeldBy[count]), lockTableList[i], inputLine)
                elif lockTableList[i].lockState == WL:
                    print ("Conflicting WriteLock: data item " + resourceName + " is on WriteLock by Transaction %d" %(lockTableList[i].lockHeldBy[0]))
                    print ("call wound wait")
                    woundWait(searchTransactionID(transactionID), searchTransactionID(lockTableList[i].lockHeldBy[0]), lockTableList[i], inputLine)
        if flag == 0:
            lockTableList.append(lockTable(resourceName, transactionID, WL))  # appending a new resource to the lockTable
            searchTransactionID(transactionID).addLockedResource(resourceName)
            print ("data item " + resourceName + " is on WriteLock by Transaction %d" %(lockTableList[0].lockHeldBy[0]))
    else:
        lockTableList.append(lockTable(resourceName, transactionID, WL))
        searchTransactionID(transactionID).addLockedResource(resourceName)


def woundWait(requestingTransaction, holdingTransaction, lockedResource, operation):
    if requestingTransaction.timestamp < holdingTransaction.timestamp:
        holdingTransaction.changeTransactionState(A)
        print("Aborting Transaction %d" % holdingTransaction.transactionID)
        requestingTransaction.changeTransactionState(W)
        requestingTransaction.addBlockedOperation(operation)
        waitingTransactions.append(requestingTransaction)
        unlock(
            holdingTransaction.transactionID)  # unlocking all the resources of the transaction that was aborted by wound wait
    else:
        requestingTransaction.changeTransactionState(W)  # adds the transaction to the waitingTransactions list
        print("changing transaction state for transaction %d to blocked" % requestingTransaction.transactionID)
        if checkDuplicateOperation(operation, requestingTransaction):
            requestingTransaction.addBlockedOperation(operation)
        if checkDuplicateTransaction(requestingTransaction):
            waitingTransactions.append(requestingTransaction)


# this method checks to see if the transaction is already in the waitingTransactions list
def checkDuplicateTransaction(transaction):
    for t in waitingTransactions:
        if t.transactionID == transaction.transactionID:
            return 0
    return 1


def checkDuplicateOperation(operation, transaction):
    for blockedOperation in transaction.blockedOperation:
        if blockedOperation == operation:
            return 0
    return 1


# this method checks the state of the transaction the method is for so that if the transaction is aborted, the operation  can be ignored
def checkState(operation):
    resourceName = resourcenID(operation)[0]
    transactionID = resourcenID(operation)[1]

    length = len(transactionTableList)
    if length != 0:
        for i in range(0, length):
            if transactionTableList[i].transactionID == transactionID and transactionTableList[i].transactionState == W:
                transactionTableList[i].addBlockedOperation(operation)
            elif transactionTableList[i].transactionState == A:
                operation = ""
                print("Operation Ignored")
    return operation


# This method deletes unlocks all the resourced held by the transactionID passed to it
def unlock(transactionID):
    print("Unlocking all resources held by transaction %d" %transactionID)
    for transaction in transactionTableList:
        if transaction.transactionID == transactionID:
            for lock in transaction.lockedResoures:
                for resource in lockTableList:
                    if resource.lockedDataItem == lock:
                        if len(resource.lockHeldBy) == 1:
                            lockTableList.remove(resource)  # if the same sources is held by multiple transactions, remove this transaction from a that list of transactions holding the lock
                        else:
                            resource.lockHeldBy.remove(transactionID)  # if only this transaction has any kind of lock on the resource, remove the resource from the lockTable completely.
    startWaitingTrans()


# see if any transactions that were waiting for resources can now be resumed
def startWaitingTrans():
    print("checking if there are any transactions waiting on the freed resources")
    for transaction in waitingTransactions:
        if transaction.transactionState == A:
            waitingTransactions.remove(transaction)
        else:
            blockOpCopy = copy.deepcopy(transaction.blockedOperation)
            for blockedOperation in transaction.blockedOperation:
                transaction.transactionState = AC  # we activate the transaction in the waitingTransactions list and pull the operations that are in the waitlist
                print("attempting operation " + blockedOperation)
                assignFunction(
                    blockedOperation)  # call the assignFunction method on the waiting operation and see if the transaction can now continue
                if transaction.transactionState != W:
                    blockOpCopy.remove(blockedOperation)
            transaction.blockedOperation = blockOpCopy
            if len(transaction.blockedOperation) == 0:
                waitingTransactions.remove(transaction)


# called when the function reaches its end. This method commits the transaction and frees all its resources.
def functionEnd(operation):
    tranNumber = get_digit(operation)
    for transactoin in transactionTableList:
        try:
            if transactoin.transactionID == tranNumber and transactoin.trasnsactionState != A:
                print("Committing transaction %d" % tranNumber)
                transactoin.transactionState = C
        except AttributeError:
            print("Committing transaction %d" % tranNumber)
            transactoin.transactionState = C
    unlock(tranNumber)


# fungsi untuk memanggil handling input per baris
def assignFunction(operation):
    if operation.find('B') == 1:
        operation = checkState(operation)
    if operation.find('B') != -1:
        beginTransaction(operation)
    elif operation.find('R') != -1:
        print("Read operation")
        readLock(operation)
    elif operation.find('W') != -1:
        print("write operation")
        writeLock(operation)
    elif operation.find("C") != -1:
        print("end")
        functionEnd(operation)


# specify the input file.

with open("transaction2.txt", 'r') as text:
    for line in text:
        inputList.append(line)
for operation in inputList:
    assignFunction(operation)
        