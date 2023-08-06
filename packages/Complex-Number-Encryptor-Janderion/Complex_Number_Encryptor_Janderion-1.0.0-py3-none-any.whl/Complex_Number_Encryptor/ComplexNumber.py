# This code was written by Jadenpaul M. Albay


class Encoder:
    def __init__(self, input_string, input_abc_list, d=1):
        self.input_str = input_string
        self.a = input_abc_list[0]
        self.b = input_abc_list[1]
        self.c = input_abc_list[2]
        self.d = d
    
    def enc(self):
        l1_encrypted_list = []
        for i in self.input_str:
            out = ord(i) * self.d
            l1_encrypted_list.append(out)
        l2_encrypted_list = []
        for x in l1_encrypted_list:
            h = (self.a * (x ** 2)) + (self.b * x) + self.c
            out0, out1 = round(h.real, 5), round(h.imag, 5)
            out = (out0 + (out1 * 1j)) * self.d
            
            l2_encrypted_list.append(out)
        return l2_encrypted_list


class Decoder:
    def __init__(self, input_list, input_abc_list, d=1):
        self.input = input_list
        self.a = input_abc_list[0]
        self.b = input_abc_list[1]
        self.c = input_abc_list[2]
        self.d = d
    
    def dec(self):
        from cmath import sqrt
        
        l2_decrypted_list = []
        l1_decrypted_list = []
        for i in self.input:
            output = ((-1 * self.b) + sqrt((self.b ** 2) - (4 * self.a * (self.c - (i / self.d))))) / (2 * self.a)
            l2_decrypted_list.append(output)
        for i in l2_decrypted_list:
            out = i.real
            l1_decrypted_list.append(chr(int(round(out / self.d))))
        output = ''
        for i in l1_decrypted_list:
            output += i
        return output
