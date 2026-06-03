const fs = require('fs');
const path = require('path');
const parser = require('@babel/parser');

const code = fs.readFileSync(path.join(__dirname, '../src/App.tsx'), 'utf8');

try {
    parser.parse(code, {
        sourceType: 'module',
        plugins: ['typescript', 'jsx']
    });
    console.log("Successfully parsed!");
} catch (error) {
    console.error("Parse error:", error.message);
    if (error.loc) {
        console.error(`At line ${error.loc.line}, col ${error.loc.column}`);
    }
}
