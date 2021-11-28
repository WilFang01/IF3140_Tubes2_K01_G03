class Tx(object):
    """docstring for Tx"""
    def __init__(self, id, start, validation, finish):
        super(Tx, self).__init__()

        self.id = id
        self.startTS = start
        self.validationTS = validation
        self.finishTS = finish
        self.writeVar = [] #write variables held by this transaction
        self.readVar = [] #read variables held by this transaction
        
    def __str__(self):
        string = f""
        string = string + (f"id: {self.id}\n")
        string = string + (f"startTS: {self.startTS}\n")
        string = string + (f"validationTS: {self.validationTS}\n")
        string = string + (f"finishTS: {self.finishTS}\n")
        string = string + (f"writeVar: \n")
        string = string + self.writeVar.__str__()
        string = string + (f"\nreadVar: \n")
        string = string + self.readVar.__str__()


        return string

# tx = Tx(1,None,None,None)
# print(tx)

# T2 = Tx(2,None,None,None)
# T2.writeVar.append('X')
# T2.writeVar.append('Y')

# T3 = Tx(3,None,None,None)
# T3.readVar.append('X')

# print(T3.readVar)
# for var in T2.writeVar:
#     print(var)
#     if var in T3.readVar:
#         print("True")

# if 'X' in ['X', 'Y']:
#     print("True")
# else:
#     print("False")