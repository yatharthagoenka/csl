import lexer

print("""
Welcome to <no_name> CLI!

Enter 'exit' to exit.
""")

while(True):
    text = input('>>> ')
    if text == "exit":
        break
    result, error = lexer.run('<stdin>',text)
    
    if error: print(error.as_string())
    else: print(result)