from WriteRead import WR
from Storage import ST

class MvCC :
    content = []
    IDfailed = []
    failed = []
    antrian = {}

    def __init__(self, filename :str) :
        self.content = open(filename,"r").read().split("\n")
        self.storage = ST(len(self.content))
        print("\nDaftar Transaksi : ", self.content)
        print("\nMemulai transaksi...")

    def MVCC(self) :
        count = 0
        countTx = 0
        while (self.content != []) or (self.failed != []) :
            # transaksi yg gagal akan dimasukkan kembali untuk dikerjakan saat semua transaksi telah selesai
            if self.content == [] :
                self.content = self.failed.copy()
                self.antrian.clear()
                self.IDfailed.clear()
                self.failed.clear()
            
            # mengambil transaksi yang akan dikerjakan
            tx = self.content.pop()

            # mengecek jenis transaksi
            if tx.find("R") != -1 :
                jnsTx = "R"
            elif tx.find("W") != -1 :
                jnsTx = "W"
            
            # mengambil key dan id transaksi
            if jnsTx == "R" :
                key = int(tx.split("R")[1])
                IDTx = int(tx.split("R")[0])
            elif jnsTx == "W" :
                valkey = tx.split("W")[1].split(",")
                key = int(valkey[0])
                IDTx = int(tx.split("W")[0])
                value = int(valkey[1])
            else :
                print("ERROR")
                break

            # mengambil timestamp transaksi
            if IDTx in self.antrian.keys() :
                tsTx = self.antrian[IDTx]
            else :
                tsTx = count
                count = count + 1
                self.antrian[IDTx] = tsTx
            
            # melakukan transaksi
            if IDTx in self.IDfailed :
                self.failed.append(tx)
            else :
                if jnsTx == "W" :
                    act = WR.write(key, value, self.storage, tsTx)
                elif jnsTx == "R" :
                    act = WR.read(key, self.storage, tsTx)
                
                if not act :
                    self.IDfailed.append(IDTx)
                if IDTx in self.IDfailed :
                    self.failed.append(tx)
            
            countTx += 1

            print("\nMVCC Transaksi ke-"+str(countTx))
            print("-------------------")
            print("Transaksi berlangsung : "+str(tx))
            print("Transaksi berikutnya : "+str(self.content))
            print("Storage : "+str(self.storage.data_transaksi))