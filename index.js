const fs = require("fs");
const thisYear = new Date().getFullYear();
const startOfYear = new Date(thisYear, 0, 1);
const endOfYear = new Date(thisYear + 1, 0, 1);
const totalDaysInYear = (endOfYear - startOfYear) / (1000 * 60 * 60 * 24);
const currentDay = Math.floor((Date.now() - startOfYear) / (1000 * 60 * 60 * 24));
const progressOfThisYear = ((currentDay / totalDaysInYear) * 100).toFixed(2);
const progressBarOfThisYear = generateProgressBar(progressOfThisYear);

function generateProgressBar(progress) {
    const progressBarCapacity = 30;
    const passedProgressBarIndex = Math.max(0, Math.min(Math.round(progress * progressBarCapacity / 100), progressBarCapacity));
    const progressBar =
        '█'.repeat(passedProgressBarIndex) + '▁'.repeat(progressBarCapacity - passedProgressBarIndex);
    return progressBar;
}

const readmeContent = fs.readFileSync(`./README.md`, "utf-8").split("\n");

readmeContent[2] = `<p align="center"><img width="100%" height="100%" src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&vCenter=true&center=true&width=700&lines=𝙷𝚒,+𝙸'𝚖+𝙲𝚘𝚍𝚒𝚗𝚐𝟺𝙷𝚘𝚞𝚛𝚜👋;𝙸'𝚖+𝚊+𝚠𝚊𝚗𝚗𝚊𝚋𝚎+𝚑𝚊𝚌𝚔𝚎𝚛+𝚊𝚗𝚍+𝚍𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛.;𝙸+𝚕𝚘𝚟𝚎+𝙸𝚃.;𝙿𝚛𝚎𝚜𝚜+𝚏𝚘𝚛+𝚖𝚘𝚛𝚎+𝚒𝚗𝚏𝚘!;⏳+𝚈𝚎𝚊𝚛+𝚙𝚛𝚘𝚐𝚛𝚎𝚜𝚜+{+${progressBarOfThisYear}+}+${progressOfThisYear}%+" alt="Typing SVG" /></p>`;

const readme = readmeContent.join("\n");

fs.writeFile('./README.md', readme, function (err) {
    if (err) throw err;
    console.log('Saved!');
});
