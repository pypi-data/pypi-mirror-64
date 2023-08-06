# Complex Number Encryptor

This package is capable of encoding messages into lists of numbers using algebra and complex numbers

## Complex_Number_Encryptor.ComplexNumber
An example of how to use this is as follows:
```python
from Complex_Number_Encryptor.ComplexNumber import Encoder
msg = "Hello World"
Encryption_factors = [(1+1j), (2+2j), (3+3j)]
Encoded_Message = Encoder(msg, Encryption_factors, d=1).enc()
print(Encoded_Message)
```
The Encoder object requires two things, the first being the string of the message, and the second being the tuple of
three numbers which are the encryption factors.
There is a third factor 'd', which is also an encryption factor, but is at default 1. A list of complex numbers would be
printed and could be reversed in the Decoder object with the same encryption factors.

```python
from Complex_Number_Encryptor.ComplexNumber import Decoder
Input_list = [the, list, recieved, from, the, encoder]
Encryption_factors = [(1+1j), (2+2j), (3+3j)]
Decoded_Message = Decoder(Input_list, Encryption_factors, d=1).dec()
print(Decoded_Message)
```
This would print out the original message.