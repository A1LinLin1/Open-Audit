// initialize the php parser factory class
const fs = require("fs");
const path = require("path");
const engine = require("php-parser");

// initialize a new parser instance
const parser = new engine({
  // some options :
  parser: {
    extractDoc: true,
    php7: true,
  },
  ast: {
    withPositions: true,
  },
});

process.stdin.on('data', function(data) {
    const filePath = data.toString().trim();
    if (fs.existsSync(filePath)) {
        const phpFileContent = fs.readFileSync(filePath, "utf8");
        const tokens = parser.tokenGetAll(phpFileContent);
        console.log(JSON.stringify(tokens));
    } else {
        console.log("File not found");
    }
});