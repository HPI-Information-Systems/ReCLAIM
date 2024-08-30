const puppeteer = require("puppeteer");
const fs = require("fs");

async function handleSingle(page, writeStream, laufNr) {
    const tableEntries = await page.$$("tr", row => row);
    if (tableEntries.length !== 0) {

        const mediaUrl = (await (await tableEntries[1].$("td")).$eval("img", img => `"${img.src.replaceAll('"', '""').replaceAll("\n", "\\n")}"`));
        const sammlung = (await tableEntries[2].$eval("th", th => `"${th.innerHTML.replaceAll('"', '""').replaceAll("\n", "\\n").slice(10)}"`));
        const objekttyp = (await tableEntries[3].$eval("th", th => `"${th.innerHTML.replaceAll('"', '""').replaceAll("\n", "\\n").replaceAll("<br><br>", "").slice(11)}"`));
        const titel = await (await tableEntries[4].$$("td"))[1].$eval("strong", s => `"${s.innerHTML.replaceAll('"', '""').replaceAll("\n", "\\n")}"`);
        const datierung = await (await tableEntries[5].$$("td"))[1].$eval("strong", s =>  `"${s.innerHTML.replaceAll('"', '""').replaceAll("\n", "\\n")}"`);
        const kuenstler = await (await tableEntries[6].$$("td"))[1].$eval("strong", s => `"${s.innerHTML.replaceAll('"', '""').replaceAll("\n", "\\n")}"`);
        const material = await (await tableEntries[7].$$("td"))[1].$eval("strong", s => `"${s.innerHTML.replaceAll('"', '""').replaceAll("\n", "\\n")}"`);
        const masse = await (await tableEntries[8].$$("td"))[1].$eval("strong", s => `"${s.innerHTML.replaceAll('"', '""').replaceAll("\n", "\\n")}"`);
        const munr = await (await tableEntries[9].$$("td"))[1].$eval("strong", s => `"${s.innerHTML.replaceAll('"', '""').replaceAll("\n", "\\n")}"`);
        const linznr = await (await tableEntries[10].$$("td"))[1].$eval("strong", s => `"${s.innerHTML.replaceAll('"', '""').replaceAll("\n", "\\n")}"`);
        const ereignisse = await (await tableEntries[11].$$("td"))[1].$eval("strong", s => `"${s.innerHTML.replaceAll('"', '""').replaceAll("\n", "\\n")}"`);

        const csvEntry = `\n${laufNr},${mediaUrl},${sammlung},${objekttyp},${titel},${datierung},${kuenstler},${material},${masse},${munr},${linznr},${ereignisse}`;
        writeStream.write(csvEntry);

        return true;
    }

    return false;
}

async function main() {
    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();

        // Old URL for search query
        //const urlBase = "https://www.dhm.de/datenbank/linzdbv2/queryresult.php?single_obj=";
        const urlBase = "https://www.dhm.de/datenbank/linzdbv2/queryresult.php?obj_no=";

        const csvStream = fs.createWriteStream("scraped_data.csv", { flags: "w" });

        // Schema in first line
        csvStream.write("Lauf-Nr.,BildURL,Sammlung,Objekttyp,Titel,Datierung,Künstler,Material/Technik,Maße,Mü-Nr.,Linz-Nr.,Ereignisse");

        for (let i = 1; i < 7000; i++) {
            const laufNr = "LI" + String(i).padStart(6, '0');
            await page.goto(urlBase + laufNr);
            const bodyText = await page.$eval("body", (body) => body.innerText);

            // no results found
            if (bodyText.includes("Keine Ergebnisse")) {
                console.log(`Kein Ergebnis für ${laufNr}`);
            }
            // one result found
            else if (await handleSingle(page, csvStream, laufNr)) {
                console.log("unique entry for " + laufNr);
            }
 
            /*// many results found??
            const galleryItems = await page.$$(".galery-item");
            if (galleryItems.length != 0) {
                const multiplePage = await browser.newPage();
                console.log("multiple entries for " + laufNr);
                for (item of galleryItems) {
                    let itemUrlPart = await item.evaluate(div => div.getAttribute("onclick"));
                    itemUrlPart = itemUrlPart.slice(17, itemUrlPart.length - 2);
                    await multiplePage.goto("https://www.dhm.de" + itemUrlPart);
                    if (await handleSingle(multiplePage, csvStream)) {
                        console.log("unique entry in multiple for " + laufNr);
                        await new Promise(resolve => setTimeout(resolve, 500));
                        continue;
                    }
                }
                multiplePage.close();
            } */
            await new Promise(resolve => setTimeout(resolve, 1200));
        }

        csvStream.end();
    } catch (error) {
        console.log(error);
    }
}

async function test() {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    const csvStream = fs.createWriteStream("scraped_data.csv", { flags: "a" });

    const urlBase = "https://www.dhm.de/datenbank/linzdbv2/queryresult.php?single_obj=0029";
    await page.goto(urlBase);

    const galleryItems = await page.$$(".galery-item");
    if (galleryItems.length != 0) {
        const testPage = await browser.newPage();
        for (item of galleryItems) {
            let itemUrlPart = await item.evaluate(div => div.getAttribute("onclick"));
            itemUrlPart = itemUrlPart.slice(17, itemUrlPart.length - 2);
            console.log("https://www.dhm.de" + itemUrlPart);
            await testPage.goto("https://www.dhm.de" + itemUrlPart);
            if (await handleSingle(testPage, csvStream)) {
                console.log("unique entry for ");
                await new Promise(resolve => setTimeout(resolve, 1000));
                continue;
            }
        }
    }
    console.log("multiple entries for ");
    await new Promise(resolve => setTimeout(resolve, 1000));
}

main();
