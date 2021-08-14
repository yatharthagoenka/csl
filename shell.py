import lexer

while(True):
    text = input('csl > ')
    result, error = lexer.run('<stdin>',text)

    if error: print(error.as_string())
    else: print(result)