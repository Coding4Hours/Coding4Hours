const fs = require("fs");

const thisYear = new Date().getFullYear();
const startTimeOfThisYear = new Date(`${thisYear}-01-01T00:00:00+00:00`).getTime();
const endTimeOfThisYear = new Date(`${thisYear}-12-31T23:59:59+00:00`).getTime();
const progressOfThisYear = ((Date.now() - startTimeOfThisYear) / (endTimeOfThisYear - startTimeOfThisYear) * 100).toFixed(2);
const progressBarOfThisYear = generateProgressBar();

function generateProgressBar() {
    const progressBarCapacity = 30;
    const passedProgressBarIndex = Math.max(0, Math.min(parseInt(progressOfThisYear * progressBarCapacity / 100), progressBarCapacity));
    const progressBar =
        '█'.repeat(passedProgressBarIndex) + '▁'.repeat(progressBarCapacity - passedProgressBarIndex);
    return `&#123; ${progressBar} &#125;`;
}

const readmeContent = fs.readFileSync(`./README.md`, "utf-8").split("\n");
readmeContent[12] = `  ⏳ Year progress ${progressBarOfThisYear} ${progressOfThisYear}%`;
const readme = readmeContent.join("\n");

fs.writeFile('./README.md', readme, function (err) {
    if (err) throw err;
    console.log('Saved!');
});
