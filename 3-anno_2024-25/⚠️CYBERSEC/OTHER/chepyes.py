from chepy import Chepy

data = str(input("Enter a string: "))

rot_13 = Chepy(data).rot_13()
to_hex = Chepy(data).to_hex()
to_base64 = Chepy(data).to_base64()
to_ascii = Chepy(data).to_string()
to_binary = Chepy(data).to_bytes()
to_x = Chepy(data).bit_shift_left()
print(f"Rot 13 = {rot_13}\n Hex = {to_hex}\n Base64 = {to_base64}\n ASCII = {to_ascii}\n Binary = {to_binary}\n Bit shift left = {to_x}")
