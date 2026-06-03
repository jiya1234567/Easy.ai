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
    
    // Track lines to report position
    const lineNum = code.substring(0, i).split('\n').length;
    
    if (inSingleComment) {
        if (char === '\n') {
            inSingleComment = false;
        }
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
            i++; // skip escaped char
        } else if (char === quoteChar) {
            inString = false;
        }
        continue;
    }
    
    // Check start of comments
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
    
    // Check start of strings
    if (char === "'" || char === '"' || char === '`') {
        inString = true;
        quoteChar = char;
        continue;
    }
    
    // Check braces/brackets/parentheses
    if (char === '{') {
        braceLevel++;
    } else if (char === '}') {
        braceLevel--;
    } else if (char === '(') {
        parenLevel++;
    } else if (char === ')') {
        parenLevel--;
    } else if (char === '[') {
        bracketLevel++;
    } else if (char === ']') {
        bracketLevel--;
    }
    
    // Print level when entering/exiting tabs
    const remainingLine = lines[lineNum - 1] || '';
    if (char === '{' && remainingLine.includes('activeTab ===')) {
        console.log(`Line ${lineNum}: Entering tab block. Levels -> Braces: ${braceLevel}, Parens: ${parenLevel}, Brackets: ${bracketLevel}. Content: ${remainingLine.trim()}`);
    }
    if (char === '}' && remainingLine.includes('activeTab ===')) {
        console.log(`Line ${lineNum}: Exiting tab block. Levels -> Braces: ${braceLevel}, Parens: ${parenLevel}, Brackets: ${bracketLevel}. Content: ${remainingLine.trim()}`);
    }
}

console.log(`End of file levels -> Braces: ${braceLevel}, Parens: ${parenLevel}, Brackets: ${bracketLevel}`);
