def inverti_righe(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        righe = file.readlines()
    
    righe_invertite = righe[::-1]
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(righe_invertite)

input_file = 'input.txt'  
output_file = 'output.txt' 
inverti_righe(input_file, output_file)
print(f"File invertito con successo e salvato come {output_file}")