const fs = require('fs');
const path = require('path');
const parser = require('@babel/parser');

const code = fs.readFileSync(path.join(__dirname, '../src/App.tsx'), 'utf8');

try {
    const ast = parser.parse(code, {
        sourceType: 'module',
        plugins: ['typescript', 'jsx'],
        tokens: true,
        errorRecovery: true
    });
    
    console.log("AST parsed with error recovery. Found", ast.errors.length, "errors.");
    ast.errors.forEach((err, idx) => {
        console.log(`Error #${idx+1}: ${err.message} at line ${err.loc.line}, col ${err.loc.column}`);
    });

    const tokens = ast.tokens;
    const stack = [];
    
    for (const token of tokens) {
        const type = token.type.label;
        if (type === '{' || type === '(' || type === '[' || type === '${') {
            stack.push({ type, loc: token.loc.start });
        } else if (type === '}') {
            if (stack.length === 0) {
                // Ignore extra closing since parser errors might have caused it
            } else {
                const last = stack.pop();
                if (last.type !== '{' && last.type !== '${') {
                    console.log(`Mismatched close '}': expected matching for '${last.type}' from line ${last.loc.line}, col ${last.loc.column} vs '}' at line ${token.loc.start.line}, col ${token.loc.start.column}`);
                }
            }
        } else if (type === ')') {
            if (stack.length === 0) {
                // Ignore
            } else {
                const last = stack.pop();
                if (last.type !== '(') {
                    console.log(`Mismatched close ')': expected matching for '${last.type}' from line ${last.loc.line}, col ${last.loc.column} vs ')' at line ${token.loc.start.line}, col ${token.loc.start.column}`);
                }
            }
        } else if (type === ']') {
            if (stack.length === 0) {
                // Ignore
            } else {
                const last = stack.pop();
                if (last.type !== '[') {
                    console.log(`Mismatched close ']': expected matching for '${last.type}' from line ${last.loc.line}, col ${last.loc.column} vs ']' at line ${token.loc.start.line}, col ${token.loc.start.column}`);
                }
            }
        }
    }
    
    console.log(`Tokens check complete. Stack length: ${stack.length}`);
    if (stack.length > 0) {
        console.log("Unclosed tokens:");
        stack.forEach((t, idx) => {
            console.log(`  #${idx+1}: '${t.type}' from line ${t.loc.line}, col ${t.loc.column}`);
        });
    }
} catch (error) {
    console.error("Fatal error:", error.message);
}
