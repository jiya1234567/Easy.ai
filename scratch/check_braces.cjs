const fs = require('fs');
const path = require('path');

function checkBraces(filepath) {
    const content = fs.readFileSync(filepath, 'utf8');

    const braces = [];
    const parentheses = [];
    const brackets = [];
    
    let i = 0;
    const length = content.length;
    let line = 1;
    let col = 1;
    
    while (i < length) {
        const char = content[i];
        
        if (char === '\n') {
            line += 1;
            col = 1;
            i += 1;
            continue;
        }
        
        // Skip single line comments
        if (char === '/' && i + 1 < length && content[i+1] === '/') {
            while (i < length && content[i] !== '\n') {
                i += 1;
            }
            continue;
        }
        
        // Skip multi-line comments
        if (char === '/' && i + 1 < length && content[i+1] === '*') {
            i += 2;
            while (i + 1 < length && !(content[i] === '*' && content[i+1] === '/')) {
                if (content[i] === '\n') {
                    line += 1;
                    col = 1;
                }
                i += 1;
            }
            i += 2;
            continue;
        }
        
        // Skip string literals
        if (char === "'" || char === '"' || char === '`') {
            const quote = char;
            i += 1;
            while (i < length && content[i] !== quote) {
                if (content[i] === '\\' && i + 1 < length) {
                    i += 2;
                } else {
                    if (content[i] === '\n') {
                        line += 1;
                        col = 1;
                    }
                    i += 1;
                }
            }
            i += 1;
            continue;
        }
        
        if (char === '{') {
            braces.push({ line, col, index: i });
        } else if (char === '}') {
            if (braces.length > 0) {
                braces.pop();
            } else {
                console.log(`Extra closing brace '}' at line ${line}, col ${col}`);
            }
        } else if (char === '(') {
            parentheses.push({ line, col, index: i });
        } else if (char === ')') {
            if (parentheses.length > 0) {
                parentheses.pop();
            } else {
                console.log(`Extra closing parenthesis ')' at line ${line}, col ${col}`);
            }
        } else if (char === '[') {
            brackets.push({ line, col, index: i });
        } else if (char === ']') {
            if (brackets.length > 0) {
                brackets.pop();
            } else {
                console.log(`Extra closing bracket ']' at line ${line}, col ${col}`);
            }
        }
        
        i += 1;
        col += 1;
    }
    
    console.log(`File check complete.`);
    console.log(`Unclosed braces: ${braces.length}`);
    braces.forEach(b => {
        console.log(`  Unclosed '{' at line ${b.line}, col ${b.col}`);
    });
    console.log(`Unclosed parentheses: ${parentheses.length}`);
    parentheses.forEach(p => {
        console.log(`  Unclosed '(' at line ${p.line}, col ${p.col}`);
    });
    console.log(`Unclosed brackets: ${brackets.length}`);
    brackets.forEach(br => {
        console.log(`  Unclosed '[' at line ${br.line}, col ${br.col}`);
    });
}

const target = process.argv[2] || path.join(__dirname, '../src/App.tsx');
checkBraces(target);
