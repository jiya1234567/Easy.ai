const fs = require('fs');
const path = require('path');
const ts = require('typescript');

const filePath = process.argv[2] 
    ? path.resolve(process.argv[2]) 
    : path.join(__dirname, '../src/App.tsx');
    
console.log("Parsing file:", filePath);
const code = fs.readFileSync(filePath, 'utf8');

const sourceFile = ts.createSourceFile(
    'App.tsx',
    code,
    ts.ScriptTarget.Latest,
    true, // setParentNodes
    ts.ScriptKind.TSX
);

console.log("Syntactic diagnostics count:", sourceFile.parseDiagnostics.length);
sourceFile.parseDiagnostics.forEach((diag, idx) => {
    const startPos = diag.start;
    const { line, character } = sourceFile.getLineAndCharacterOfPosition(startPos);
    
    // Get message text
    const message = typeof diag.messageText === 'string' 
        ? diag.messageText 
        : diag.messageText.messageText;
        
    console.log(`Error #${idx + 1}: ${message} at line ${line + 1}, col ${character + 1}`);
});
