const fs = require('fs');
const { execSync } = require('child_process');

// We can launch Chrome in headless mode with --screenshot or evaluate script
console.log("Checking if headless chrome can render pr.html...");
try {
    const cmd = `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --remote-debugging-port=9222 --dump-dom http://localhost:8080/pr.html`;
    const out = execSync(cmd, { encoding: 'utf-8', maxBuffer: 10 * 1024 * 1024 });
    console.log("HTML length received:", out.length);
} catch (e) {
    console.error("Error:", e.message);
}
