from Storage import ST 

class WR :
    def write(key, value, st : ST, timestamp) :
        if (st.data_transaksi[key]['Timestamp'] <= timestamp) :
            st.data_transaksi[key]['Timestamp'] = timestamp
            st.data_transaksi[key]['Value'] = value
            return True
        else :
            return False
    
    def read(key, st : ST, timestamp) :
        if (st.data_transaksi[key]['Timestamp'] <= timestamp) :
            st.data_transaksi[key]['Timestamp'] = timestamp
            return True
        else :
            return False