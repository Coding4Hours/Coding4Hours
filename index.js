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
    return progressBar;
}

const readmeContent = fs.readFileSync(`./README.md`, "utf-8").split("\n");
readmeContent[2] = `<p align="center"> <a href="https://octoprofile.vercel.app/user?id=Coding4Hours"><img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&vCenter=true&center=true&width=435&lines=𝙷𝚒,+𝙸'𝚖+𝙲𝚘𝚍𝚒𝚗𝚐𝟺𝙷𝚘𝚞𝚛𝚜👋;𝙸'𝚖+𝚊+𝚠𝚊𝚗𝚗𝚊𝚋𝚎+𝚑𝚊𝚌𝚔𝚎𝚛+𝚊𝚗𝚍+𝚍𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛.;𝙸+𝚕𝚘𝚟𝚎+𝙸𝚃.;𝙿𝚛𝚎𝚜𝚜+𝚏𝚘𝚛+𝚖𝚘𝚛𝚎+𝚒𝚗𝚏𝚘!;⏳+𝚈𝚎𝚊𝚛+𝚙𝚛𝚘𝚐𝚛𝚎𝚜𝚜+{+${progressBarOfThisYear}+}+52.72%" alt="Typing SVG" /></a> </p>`;
const readme = readmeContent.join("\n");

fs.writeFile('./README.md', readme, function (err) {
    if (err) throw err;
    console.log('Saved!');
});
