const fs = require("fs");

// Get the current year
const thisYear = new Date().getFullYear();

// Calculate the start of the year
const startOfYear = new Date(thisYear, 0, 1); // January 1st of this year

// Calculate the end of the year
const endOfYear = new Date(thisYear + 1, 0, 1); // January 1st of the next year

// Calculate the number of days in the year
const totalDaysInYear = (endOfYear - startOfYear) / (1000 * 60 * 60 * 24);

// Calculate the number of days passed so far
const currentDay = Math.floor((Date.now() - startOfYear) / (1000 * 60 * 60 * 24));

// Calculate the year's progress as a percentage
const progressOfThisYear = ((currentDay / totalDaysInYear) * 100).toFixed(2);

// Generate the progress bar
const progressBarOfThisYear = generateProgressBar(progressOfThisYear);

function generateProgressBar(progress) {
    const progressBarCapacity = 30;
    const passedProgressBarIndex = Math.max(0, Math.min(Math.round(progress * progressBarCapacity / 100), progressBarCapacity));
    const progressBar =
        '█'.repeat(passedProgressBarIndex) + '▁'.repeat(progressBarCapacity - passedProgressBarIndex);
    return progressBar;
}

// Read the README.md file
const readmeContent = fs.readFileSync(`./README.md`, "utf-8").split("\n");

// Update the third line with the new progress bar and progress percentage
readmeContent[2] = `<p align="center"> <a href="https://octoprofile.vercel.app/user?id=Coding4Hours"><img width="100%" height="100%" src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&vCenter=true&center=true&width=700&lines=𝙷𝚒,+𝙸'𝚖+𝙲𝚘𝚍𝚒𝚗𝚐𝟺𝙷𝚘𝚞𝚛𝚜👋;𝙸'𝚖+𝚊+𝚠𝚊𝚗𝚗𝚊𝚋𝚎+𝚑𝚊𝚌𝚔𝚎𝚛+𝚊𝚗𝚍+𝚍𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛.;𝙸+𝚕𝚘𝚟𝚎+𝙸𝚃.;𝙿𝚛𝚎𝚜𝚜+𝚏𝚘𝚛+𝚖𝚘𝚛𝚎+𝚒𝚗𝚏𝚘!;⏳+𝚈𝚎𝚊𝚛+𝚙𝚛𝚘𝚐𝚛𝚎𝚜𝚜+{+${progressBarOfThisYear}+}+${progressOfThisYear}%+" alt="Typing SVG" /></a> </p>`;

// Join the content back into a single string
const readme = readmeContent.join("\n");

// Write the updated content back to README.md
fs.writeFile('./README.md', readme, function (err) {
    if (err) throw err;
    console.log('Saved!');
});
