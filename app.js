const express = require('express');
const multer = require('multer');
const { Storage } = require('@google-cloud/storage');
const { v4: uuidv4 } = require('uuid');
const dotenv = require('dotenv');
dotenv.config();

const app = express();
const port = 3030;
const upload = multer({ storage: multer.memoryStorage() });

//diisi sesuai akun google cloud
const storage = new Storage({
  projectId: process.env.GOOGLE_PROJECT_ID,
  key: process.env.CLOUD_STORAGE_KEY,
});

const bucket = storage.bucket(process.env.BUCKET_NAME);

app.post('/documents', upload.array('documents', 2), async (req, res) => {
  try {
    const uploadedFile = req.files;
    if (!uploadedFile || uploadedFile.length === 0) {
      return res.status(400).json({ error: 'File not Found' });
    }

    const uploadedUrl = [];

    for (const file of uploadedFile) {
      const fileName = `${uuidv4()}_${file.originalname}`;
      const storageFile = bucket.file(fileName);
      await storageFile.save(file.buffer);

      const publicUrl = `https://storage.googleapis.com/${bucket.name}/${fileName}`;
      uploadedUrl.push(publicUrl);
    }

    res.json({
      message: 'Document successfully uploaded',
      document: uploadedUrl,
    });
  } catch (err) {
    console.log(err);
    res
      .status(500)
      .json({ error: 'An error occured while uploading document' });
  }
});

app.get('/documents', async (req, res) => {
  try {
    const [files] = await bucket.getFiles();

    const documents = files.map((file) => {
      const fileNameParts = file.name.split('_');
      const originalName = fileNameParts.slice(1).join('_');

      return {
        filename: originalName,
        downloadUrl: `https://storage.googleapis.com/${bucket.name}/${file.name}`,
      };
    });

    res.json({
      message: 'List of uploaded documents',
      documents: documents,
    });
  } catch (err) {
    console.log(err);
    res
      .status(500)
      .json({ error: 'An error occured while uploading document' });
  }
});

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
