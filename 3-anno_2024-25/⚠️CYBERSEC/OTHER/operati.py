alfa = 0
beta = 0
op = ''

alfa = int(input('Enter first number: '))
beta = int(input('Enter second number: '))
op = input('Enter operator: ')

if op != '+' and op != '-' and op != '*' and op != '/' and op != '%' and op != '**' and op != '<<' and op != '>>':
    print('Invalid operator')
    exit(1)

def op(a, b, oper):
    match oper:
        case '-':
            return a - b
        case '+':
            return a + b
        case '*':
            return a * b
        case '/':
            return a / b
        case '%':
            return a % b
        case '**':
            return a ** b
        case '<<':
            return a << b
        case '>>':
            return a >> b
        
print(op(alfa, beta, '+'))
print(op(alfa, beta, '-'))
print(op(alfa, beta, '*'))
print(op(alfa, beta, '/'))
print(op(alfa, beta, '%'))
print(op(alfa, beta, '**'))
print(op(alfa, beta, '<<'))
print(op(alfa, beta, '>>'))

pip3 install chepy
# optionally with extra requirements
