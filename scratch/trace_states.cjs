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
            console.log(`Line ${lineNum}: Exited string. Content: ${lines[lineNum-1].trim()}`);
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
        console.log(`Line ${lineNum}: Entered string with quote ${char}. Content: ${lines[lineNum-1].trim()}`);
        continue;
    }
    
    if (char === '{') braceLevel++;
    else if (char === '}') braceLevel--;
    else if (char === '(') parenLevel++;
    else if (char === ')') parenLevel--;
}
