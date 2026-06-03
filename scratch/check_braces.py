def check_braces(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    braces = []
    parentheses = []
    brackets = []
    
    # We should skip strings and comments to avoid false matches
    i = 0
    length = len(content)
    line = 1
    col = 1
    
    while i < length:
        char = content[i]
        
        if char == '\n':
            line += 1
            col = 1
            i += 1
            continue
            
        # Skip single line comments
        if char == '/' and i + 1 < length and content[i+1] == '/':
            while i < length and content[i] != '\n':
                i += 1
            continue
            
        # Skip multi-line comments
        if char == '/' and i + 1 < length and content[i+1] == '*':
            i += 2
            while i + 1 < length and not (content[i] == '*' and content[i+1] == '/'):
                if content[i] == '\n':
                    line += 1
                    col = 1
                i += 1
            i += 2
            continue
            
        # Skip string literals
        if char in ["'", '"', '`']:
            quote = char
            i += 1
            while i < length and content[i] != quote:
                if content[i] == '\\' and i + 1 < length:
                    i += 2
                else:
                    if content[i] == '\n':
                        line += 1
                        col = 1
                    i += 1
            i += 1
            continue
            
        if char == '{':
            braces.append((line, col, i))
        elif char == '}':
            if braces:
                braces.pop()
            else:
                print(f"Extra closing brace '}}' at line {line}, col {col}")
        elif char == '(':
            parentheses.append((line, col, i))
        elif char == ')':
            if parentheses:
                parentheses.pop()
            else:
                print(f"Extra closing parenthesis ')' at line {line}, col {col}")
        elif char == '[':
            brackets.append((line, col, i))
        elif char == ']':
            if brackets:
                brackets.pop()
            else:
                print(f"Extra closing bracket ']' at line {line}, col {col}")
        
        i += 1
        col += 1
        
    print(f"File check complete.")
    print(f"Unclosed braces: {len(braces)}")
    for b in braces:
        print(f"  Unclosed '{{' at line {b[0]}, col {b[1]}")
    print(f"Unclosed parentheses: {len(parentheses)}")
    for p in parentheses:
        print(f"  Unclosed '(' at line {p[0]}, col {p[1]}")
    print(f"Unclosed brackets: {len(brackets)}")
    for br in brackets:
        print(f"  Unclosed '[' at line {br[0]}, col {br[1]}")

if __name__ == '__main__':
    import sys
    check_braces(sys.argv[1] if len(sys.argv) > 1 else '../src/App.tsx')
