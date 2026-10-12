const fs = require("fs");
const path = require("path");

const CATEGORIES = ["tops", "bottoms", "shoes", "blush", "hair"];
const IMAGE_EXTENSIONS = /\.(png|jpe?g|webp|gif)$/i;

function formatName(filename) {
  return path
    .parse(filename)
    .name
    .replace(/[_-]+/g, " ")
    .trim()
    .replace(/\s+/g, " ")
    .replace(/\b\w/g, char => char.toUpperCase());
}

function generateWardrobe() {
  const wardrobe = {};

  for (const category of CATEGORIES) {
    const folder = path.join(__dirname, "images", category);

    if (!fs.existsSync(folder)) {
      wardrobe[category] = [];
      continue;
    }

    const files = fs
      .readdirSync(folder, { withFileTypes: true })
      .filter(file =>
        file.isFile() && IMAGE_EXTENSIONS.test(file.name)
      )
      .map(file => file.name)
      .sort((a, b) => a.localeCompare(b));

    wardrobe[category] = files.map((filename, index) => ({
      id: `${category}-${index + 1}`,
      name: formatName(filename),
      src: `images/${category}/${filename}`
    }));
  }

  fs.writeFileSync(
    path.join(__dirname, "wardrobe.json"),
    JSON.stringify(wardrobe, null, 2)
  );

  console.log("Wardrobe generated successfully!");
}

generateWardrobe();
