const fs = require('fs');
const path = require('path');

const sharedStringsPath = path.join(__dirname, 'xlsx_unzipped', 'xl', 'sharedStrings.xml');
const sheet1Path = path.join(__dirname, 'xlsx_unzipped', 'xl', 'worksheets', 'sheet1.xml');

// Helper to extract text from simple tag structures
function getTags(str, tag) {
    const regex = new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\/${tag}>`, 'g');
    const matches = [];
    let match;
    while ((match = regex.exec(str)) !== null) {
        matches.push(match[1]);
    }
    return matches;
}

function getAttr(tagStr, attr) {
    const regex = new RegExp(`${attr}="([^"]*)"`);
    const match = regex.exec(tagStr);
    return match ? match[1] : null;
}

// 1. Read Shared Strings
const sharedStringsContent = fs.readFileSync(sharedStringsPath, 'utf8');
const tTags = getTags(sharedStringsContent, 't');
console.log('Shared Strings Count:', tTags.length);

// 2. Read Sheet1
const sheetContent = fs.readFileSync(sheet1Path, 'utf8');

// Find all rows
const rows = getTags(sheetContent, 'row');
const grid = [];

for (const row of rows) {
    const rowNum = getAttr(row, 'r');
    const cells = [];
    const cellRegex = /<c([^>]+)>([\s\S]*?)<\/c>/g;
    let cellMatch;
    
    while ((cellMatch = cellRegex.exec(row)) !== null) {
        const cAttrs = cellMatch[1];
        const cValTag = getTags(cellMatch[2], 'v')[0];
        const cellRef = getAttr(cAttrs, 'r');
        const cellType = getAttr(cAttrs, 't');
        
        let value = '';
        if (cValTag !== undefined) {
            if (cellType === 's') {
                const idx = parseInt(cValTag, 10);
                value = tTags[idx] || '';
            } else {
                value = cValTag;
            }
        }
        cells.push({ ref: cellRef, val: value });
    }
    grid.push({ row: rowNum, cells });
}

// Print the grid
for (const rowData of grid) {
    const cellStrings = rowData.cells.map(c => `${c.ref}: ${c.val}`).join(' | ');
    console.log(`Row ${rowData.row}: ${cellStrings}`);
}
