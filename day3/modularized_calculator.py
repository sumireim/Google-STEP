#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def read_parentheses(line, index):
    token = {'type': 'PARENTHESIS'}
    return token, index + 1

def read_close_parentheses(line, index):
    token = {'type': 'CLOSEPARENTHESIS'}
    return token, index + 1

def read_abs(line, index):
    if line[index+1] == 'b' and line[index+2] == 's':
        token = {'type': 'ABS'}
        return token, index + 3
    else:
        print('Invalid character found: ' + line[index])
        return 0

def read_int(line, index):
    if line[index+1] == 'n' and line[index+2] == 't':
        token = {'type': 'INT'}
        return token, index + 3
    else:
        print('Invalid character found: ' + line[index])
        return 0
    
def read_round(line, index):
    if line[index+1] == 'o' and line[index+2] == 'u' and line[index+3] == 'n' and line[index+4] == 'd':
        token = {'type': 'ROUND'}
        return token, index + 5
    else:
        print('Invalid character found: ' + line[index])
        return 0

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index].isalpha():
            if line[index] == 'a':
                (token, index) = read_abs(line, index)
            if line[index] == 'i':
                (token, index) = read_int(line, index)
            if line[index] == 'r':
                (token, index) = read_round(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_parentheses(line, index)
        elif line[index] == ')':
            (token, index) = read_close_parentheses(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

def function_evaluate(tokens):
    updated_tokens = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'ABS': 
            if index >= len(tokens) or tokens[index]['type'] != 'PARENTHESIS':
                print('abs () is required')
                exit(1)
            
            index += 1  # skip '('
            temp_tokens = []
            
            while index < len(tokens) and tokens[index]['type'] != 'CLOSEPARENTHESIS':
                temp_tokens.append(tokens[index])
                index += 1
            
            if index >= len(tokens):
                print('Missing closing parenthesis for abs()')
                exit(1)
            
            temp_tokens = parentheses_evaluate(temp_tokens)
            arg_value = evaluate(temp_tokens)
            result = abs(arg_value)
            
            updated_tokens.append({'type': 'NUMBER', 'number': result})
            index += 1  # skip ')' 
    return updated_tokens

def eliminate_parentheses(tokens):
    if tokens[0]['type'] == 'PASENTHESIS':
        pass
    else:
        return tokens
    
def find_parenthesis(tokens):
    
    return 0

def find_closing_parenthesis(tokens, start_index):

    return 0


def parentheses_evaluate(tokens):
    updated_tokens = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'PARENTHESIS': # if there is a parenthesis
            index += 1 
            temp_tokens = []
            temp_answer = 0
            while index < len(tokens) and tokens[index]['type'] != 'CLOSEPARENTHESIS': # until find a closing parenthesis
                temp_tokens.append(tokens[index])
                index += 1 
            temp_answer = evaluate(temp_tokens)
            updated_tokens.append({'type': 'NUMBER', 'number': temp_answer})
            if index >= len(tokens):
                print('Missing closing parenthesis for parenthesis()')
                exit(1)
            index += 1  # Skip the closing parenthesis
        else:
            updated_tokens.append(tokens[index])
            index += 1
    return updated_tokens

def evaluate(tokens):
    answer = 0
    index = 1
    # Handle multiplication and division first
    while index < len(tokens):
        if tokens[index]['type'] == 'MULTIPLY':
            if index > 0 and index + 1 < len(tokens):
                tokens[index-1]['number'] *= tokens[index+1]['number'] # store the result in index-1
                del tokens[index:index+2] # remove the MULTIPLY token and the next number
            else:
                print('Invalid syntax for multiplication')
                exit(1)
        elif tokens[index]['type'] == 'DIVIDE':
            if index > 0 and index + 1 < len(tokens):
                tokens[index-1]['number'] = tokens[index-1]['number'] / tokens[index+1]['number'] # store the result in index-1
                del tokens[index:index+2] # remove the DIVIDE token and the next number
            else:
                print('Invalid syntax for division')
                exit(1)
        else:
            index += 1
    # handle addition and subtraction
    index = 1
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax for addition or subtraction')
                exit(1)
        index += 1
    return answer

def test(line):
    tokens = tokenize(line)
    tokens = parentheses_evaluate(tokens)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %g)" % (line, expected_answer)) # change
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1") # only integer
    test("1.0") # only float
    test("1+2") # simple addition
    test("1-2") # simple subtraction
    test("1*2") # simple multiplication
    test("1/2") # simple division
    test("1+2-3") # addition and subtraction
    test("1+2*3") # addition and multiplication
    test("1+2/3") # addition and division
    test("1.0+2.1-3") # float mix addition and subtraction
    test("1.0+2.1*3") # float mix addition and multiplication
    test("1.0+2.1/3") # float mix addition and division
    test("1+2*3-4/5") # integer ixed 
    test("1.0+2*3/4.0-5.0") # float mixed 
    test("1*2*3") # continuous multiplication
    test("1/2/3") # continuous division
    '''
    以下括弧ありのケース
    '''
    test("(1+2)*3") # parentheses with addition
    test("(1-2)*3") # parentheses with subtraction
    test("(1*2)*3") # parentheses with multiplication
    test("(1/2)*3") # parentheses with division
    test("1+(2*3)") # parentheses in multiplication
    test("1-(2/3)") # parentheses in division
    test("1+(2-3)*4") # parentheses in subtraction 
    test("1+(2*3-4)/5") # conplex
    test("1+(2-3*(5-3))*4") # parentheses in parentheses
    print("==== Test finished! ====\n")
    exit()

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    tokens = parentheses_evaluate(tokens)  # Handle parentheses first
    answer = evaluate(tokens)
    print("answer = %g\n" % answer) # change
