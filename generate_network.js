const fs = require('fs');

const nodeCount = 70;
const m = 2;
const nodes = [];
const links = [];

function addNode(id) {
    nodes.push({ id, links: 0 });
}

function addLink(sourceId, targetId) {
    links.push({ source: sourceId, target: targetId });
    nodes[sourceId].links++;
    nodes[targetId].links++;
}

function selectAttachmentTargets(m, currentId) {
    const targets = new Set();
    const pool = [];
    nodes.slice(0, currentId).forEach(n => {
        for (let i = 0; i < n.links + 1; i++) pool.push(n.id);
    });

    while (targets.size < m && targets.size < currentId) {
        const id = pool[Math.floor(Math.random() * pool.length)];
        targets.add(id);
    }
    return Array.from(targets);
}

// Initial clique
for (let i = 0; i < 3; i++) {
    addNode(i);
    if (i > 0) addLink(i, i - 1);
}
addLink(2, 0);

// Preferential attachment
for (let i = 3; i < nodeCount; i++) {
    addNode(i);
    const targets = selectAttachmentTargets(m, i);
    targets.forEach(targetId => addLink(i, targetId));
}

const networkData = {
    nodes: nodes.map(n => ({ id: n.id })),
    links: links
};

fs.writeFileSync('data/network.json', JSON.stringify(networkData, null, 2));
console.log('Successfully generated data/network.json');
