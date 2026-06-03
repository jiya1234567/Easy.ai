const fs = require('fs');
const path = require('path');
const parser = require('@babel/parser');

const code = fs.readFileSync(path.join(__dirname, '../src/App.tsx'), 'utf8');

try {
    const ast = parser.parse(code, {
        sourceType: 'module',
        plugins: ['typescript', 'jsx'],
        tokens: true
    });
    
    console.log("Parsed AST successfully, checking tokens...");
    const tokens = ast.tokens;
    const stack = [];
    
    for (const token of tokens) {
        const type = token.type.label;
        if (type === '{' || type === '(' || type === '[' || type === '${') {
            stack.push({ type, loc: token.loc.start });
        } else if (type === '}') {
            if (stack.length === 0) {
                console.log(`Extra closing '}' at line ${token.loc.start.line}, col ${token.loc.start.column}`);
            } else {
                const last = stack.pop();
                if (last.type !== '{' && last.type !== '${') {
                    console.log(`Mismatched close '}': expected matching for '${last.type}' from line ${last.loc.line}, col ${last.loc.column}`);
                }
            }
        } else if (type === ')') {
            if (stack.length === 0) {
                console.log(`Extra closing ')' at line ${token.loc.start.line}, col ${token.loc.start.column}`);
            } else {
                const last = stack.pop();
                if (last.type !== '(') {
                    console.log(`Mismatched close ')': expected matching for '${last.type}' from line ${last.loc.line}, col ${last.loc.column}`);
                }
            }
        } else if (type === ']') {
            if (stack.length === 0) {
                console.log(`Extra closing ']' at line ${token.loc.start.line}, col ${token.loc.start.column}`);
            } else {
                const last = stack.pop();
                if (last.type !== '[') {
                    console.log(`Mismatched close ']': expected matching for '${last.type}' from line ${last.loc.line}, col ${last.loc.column}`);
                }
            }
        }
    }
    
    console.log(`Tokens check complete. Stack length: ${stack.length}`);
    if (stack.length > 0) {
        console.log("Unclosed tokens:");
        stack.forEach(t => {
            console.log(`  '${t.type}' from line ${t.loc.line}, col ${t.loc.column}`);
        });
    }
} catch (error) {
    // If parse fails, get the tokens we can
    console.log("Initial parse failed, trying to tokenize directly...");
    try {
        const tokens = parser.tokTypes;
        // Unfortunately tokenizer is not exported simply, but we can do a simplified check
        console.log("Error details:", error.message);
    } catch(e) {
        console.log(e);
    }
}
