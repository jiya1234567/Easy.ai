const fs = require('fs');
const execSync = require('child_process').execSync;

try {
    const diffContent = execSync('git diff 313a9f8 f9e0f4f -- src/App.tsx', { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 });
    fs.writeFileSync('scratch/diff_f9e0f4f.diff', diffContent, 'utf8');
    console.log("Successfully wrote diff to scratch/diff_f9e0f4f.diff");
} catch (e) {
    console.error("Error generating diff:", e.message);
}
