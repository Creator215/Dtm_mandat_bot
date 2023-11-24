class filter_json:

    def __init__(self,keys_,values_):
        self.keys_ = keys_
        self.values_ = values_
        self.ddata = []
        self.key_s = []
        self.val_s = []

        k = ""
        for i in self.keys_:
            if(i == "#"):
                self.key_s.append(k)
                k = ""
            else:
                k += str(i)

        v = ""
        for i in self.values_:
            if (i == "#"):
                self.val_s.append(v)
                v = ""
            else:
                v += str(i)

        for i in range(len(self.key_s)):
            self.ddata.append(self.key_s[i])
            if(self.val_s[i] == ""):
                self.ddata.append("--")
            else:
                self.ddata.append(self.val_s[i])


    def get_filter_data(self):
        return self.ddata
    def clear_data(self):
        self.ddata = []
        self.key_s = []
        self.val_s = []