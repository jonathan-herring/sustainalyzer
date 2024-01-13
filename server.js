const express = require('express');
const multer = require('multer');
const app = express();
const port = 5000;
require('dotenv').config();

// Set up multer for handling file uploads
const upload = multer({
  dest: 'uploads/', // This is where the files will be saved. Make sure this directory exists!
});

app.post('/process', upload.single('file'), (req, res) => {
  // req.file is the uploaded file
  console.log(req.file);

  // TODO: Send the file to the Google Cloud Vision API, search for the product on eBay,
  // calculate the sustainability score, etc.

  // For now, just respond with a JSON object
  res.json({ message: 'File received' });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});