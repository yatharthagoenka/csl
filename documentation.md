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
<<<<<<< HEAD
- `for` | `to` | `inc` | `while` | `then` -> loops
- `and` | `or` | `not`-> logical operators
- `continue` | `break`-> loops control keywords
=======
- `for` | `to`| `inc` | `while` | `then` -> loops
>>>>>>> 36e06c6... add documention
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
<<<<<<< HEAD


### Lists
```
    let arr = [1,"element"]
    let arr = arr + 3       # arr becomes [1,"element",3]

    print(arr/2)            # prints 3
```
=======
>>>>>>> 36e06c6... add documention
