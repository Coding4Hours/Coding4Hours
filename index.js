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
    return "{"  + progressBar "}";
}

const readmeContent = fs.readFileSync(`./README.md`, "utf-8").split("\n");
readmeContent[2] = `<p align="center"> <a href="https://octoprofile.vercel.app/user?id=Coding4Hours"><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&vCenter=true&center=true&width=435&lines=%F0%9D%99%B7%F0%9D%9A%92%2C+%F0%9D%99%B8'%F0%9D%9A%96+%F0%9D%99%B2%F0%9D%9A%98%F0%9D%9A%8D%F0%9D%9A%92%F0%9D%9A%97%F0%9D%9A%90%F0%9D%9F%BA%F0%9D%99%B7%F0%9D%9A%98%F0%9D%9A%9E%F0%9D%9A%9B%F0%9D%9A%9C%F0%9F%91%8B;%F0%9D%99%B8'%F0%9D%9A%96+%F0%9D%9A%8A+%F0%9D%9A%A0%F0%9D%9A%8A%F0%9D%9A%97%F0%9D%9A%97%F0%9D%9A%8A%F0%9D%9A%8B%F0%9D%9A%8E+%F0%9D%9A%91%F0%9D%9A%8A%F0%9D%9A%8C%F0%9D%9A%94%F0%9D%9A%8E%F0%9D%9A%9B+%F0%9D%9A%8A%F0%9D%9A%97%F0%9D%9A%8D+%F0%9D%9A%8D%F0%9D%9A%8E%F0%9D%9A%9F%F0%9D%9A%8E%F0%9D%9A%95%F0%9D%9A%98%F0%9D%9A%99%F0%9D%9A%8E%F0%9D%9A%9B.;%F0%9D%99%B8+%F0%9D%9A%95%F0%9D%9A%98%F0%9D%9A%9F%F0%9D%9A%8E+%F0%9D%99%B8%F0%9D%9A%83.;%F0%9D%99%BF%F0%9D%9A%9B%F0%9D%9A%8E%F0%9D%9A%9C%F0%9D%9A%9C+%F0%9D%9A%8F%F0%9D%9A%98%F0%9D%9A%9B+%F0%9D%9A%96%F0%9D%9A%98%F0%9D%9A%9B%F0%9D%9A%8E+%F0%9D%9A%92%F0%9D%9A%97%F0%9D%9A%8F%F0%9D%9A%98!;%E2%8F%B3+%F0%9D%9A%88%F0%9D%9A%8E%F0%9D%9A%8A%F0%9D%9A%9B+%F0%9D%9A%99%F0%9D%9A%9B%F0%9D%9A%98%F0%9D%9A%90%F0%9D%9A%9B%F0%9D%9A%8E%F0%9D%9A%9C%F0%9D%9A%9C+${encodeURIComponent(progressBarOfThisYear)}+${encodeURIComponent(progressOfThisYear)}%25" alt="Typing SVG" /></a> </p>`;
const readme = readmeContent.join("\n");

fs.writeFile('./README.md', readme, function (err) {
    if (err) throw err;
    console.log('Saved!');
});
