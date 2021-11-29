class ST :
    data_transaksi = {}
    def __init__(self, data_length) :
        length = data_length + 1
        for i in range (length) :
            self.data_transaksi[i] = {"Value" : 0, "Timestamp" : 0}