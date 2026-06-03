const fs = require('fs');
const execSync = require('child_process').execSync;

const commit = process.argv[2] || 'ceb4402';
const target = process.argv[3] || 'scratch/app_rev.tsx';

try {
    const fileContent = execSync(`git show ${commit}:src/App.tsx`, { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 });
    fs.writeFileSync(target, fileContent, 'utf8');
    console.log(`Successfully wrote ${commit}:src/App.tsx to ${target}`);
} catch (e) {
    console.error("Error running git show:", e.message);
}
