const fs = require('fs');
const path = require('path');

const code = fs.readFileSync(path.join(__dirname, '../src/App.tsx'), 'utf8');
const lines = code.split('\n');

let braceLevel = 0;
let parenLevel = 0;
let bracketLevel = 0;

let inSingleComment = false;
let inMultiComment = false;
let inString = false;
let quoteChar = '';

for (let i = 0; i < code.length; i++) {
    const char = code[i];
    const nextChar = code[i+1] || '';
    
    const lineNum = code.substring(0, i).split('\n').length;
    const colNum = code.substring(0, i).split('\n').pop().length + 1;
    
    if (inSingleComment) {
        if (char === '\n') inSingleComment = false;
        continue;
    }
    
    if (inMultiComment) {
        if (char === '*' && nextChar === '/') {
            inMultiComment = false;
            i++;
        }
        continue;
    }
    
    if (inString) {
        if (char === '\\') {
            i++;
        } else if (char === quoteChar) {
            inString = false;
        }
        continue;
    }
    
    if (char === '/' && nextChar === '/') {
        inSingleComment = true;
        i++;
        continue;
    }
    if (char === '/' && nextChar === '*') {
        inMultiComment = true;
        i++;
        continue;
    }
    
    if (char === "'" || char === '"' || char === '`') {
        inString = true;
        quoteChar = char;
        continue;
    }
    
    if (char === '{') {
        braceLevel++;
    } else if (char === '}') {
        braceLevel--;
        if (braceLevel < 0) {
            console.log(`Braces went negative at Line ${lineNum}, col ${colNum}: }`);
            console.log(`Context: ${lines[lineNum - 1]}`);
            break;
        }
    } else if (char === '(') {
        parenLevel++;
    } else if (char === ')') {
        parenLevel--;
        if (parenLevel < 0) {
            console.log(`Parens went negative at Line ${lineNum}, col ${colNum}: )`);
            console.log(`Context: ${lines[lineNum - 1]}`);
            break;
        }
    } else if (char === '[') {
        bracketLevel++;
    } else if (char === ']') {
        bracketLevel--;
        if (bracketLevel < 0) {
            console.log(`Brackets went negative at Line ${lineNum}, col ${colNum}: ]`);
            console.log(`Context: ${lines[lineNum - 1]}`);
            break;
        }
    }
}
