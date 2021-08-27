## Data Types

- int
- float
- string

## Data Structures

- Array (multiple data types)

## Operators

- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division
- `^` Exponentiation

## Comparison Operators

- `>` Greater than
- `>=` Greater than or equals to
- `<` Less than
- `<=` Less than or equals to
- `==` Equals to
- `!=` Not equals to

## Keywords

- `let` -> Assign variables
- `true`|`false` = 1 | 0
- `if` | `else` | `then` | `else if` -> conditions
- `for` | `to` | `inc` | `while` | `then` -> loops
- `and` | `or` | `not`-> logical operators
- `continue` | `break`-> loops control keywords
- `inc` -> Define increment of variable in for loop (Optional)
- `and` | `or` | `not`-> logical operators
- `continue` | `break`-> loops control keywords
- `fnc` -> Function
- `#` -> Comments

### For loop

```
    for i=1 to 10 inc 2 then
        if i==4 then continue else if i>8 then break else print(i)
    end
```

### While loop

```
    while <condition1> and/or <condition2> then
        print(1)
    end
```

### Function

```
    fnc foo()
        return "hello"
    end

    fnc bar() -> print("world")
```

### For loop

```
    let a= [];

    for i=0 to 10 then
        if i==4 then continue elseif i==8 then break;
        let a=a+i;
    end

    print(a);
```

### While loop

```
    while <condition1> and/or <condition2> then
        print(1)
    end
```

### Function

```
    # Function Definitions

    fnc foo()
        return "hello"
    end

    fnc bar() -> print("world")

    ##############

    # Function Calls

    let greet = foo()
    bar()
```

## List Operations

- `+` Add element to list
- `-` Remove element at specified index
- `*` Concatenate two lists
- `/` Access element at specified index

### Lists

```
    let arr = [1,"element"]
    let arr = arr + 3       # arr => [1,"element",3]
    let arr = arr * [4, 5]       # arr => [1,"element",3, 4, 5]
    let arr = arr - 4       # arr => [1,"element",3, 4]

    print(arr/2)            # prints 3
```

## Built-in Functions

- `print(a: any)` Prints the value
- `print_ret(a: any)` Prints and return the value
- `input()` Takes input from user as string
- `input_int()` Takes input from user as integer
- `clear()` Clears the terminal
- `is_num(a: any)` Returns true if type of argument is int or float else returns false
- `is_string(a: any)` Returns true if type of argument is string else returns false
- `is_list(a: any)` Returns true if type of argument is array else returns false
- `is_function(a: any)` Returns true if given argument is a function else returns false
- `append(a: array, b: int/float/string)` Appends element at the end of array
- `pop(a: array, b: int)` Removes element at index b
- `extend(a: array, b: array)` Merge the 2nd array into the 1st array
- `len(a: array)` Returns the length of array
- `run(file_path: string)` Runs the program from file
