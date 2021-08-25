import lexer

print("""
Welcome to <no_name> CLI!

Enter 'exit' to exit.
""")

while(True):
    text = input('>>> ')
    if text.strip() == "": continue
    if text == "exit":
        break
    result, error = lexer.run('<stdin>',text)
    
    if error: print(error.as_string())
    elif result: 
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))