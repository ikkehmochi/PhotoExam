const { Storage } = require('@google-cloud/storage');
const dotenv = require('dotenv');
dotenv.config();

const storage = new Storage({
  projectId: 'project-rafie-1',
  key: './storageKey.json',
});

const bucket = storage.bucket('photo_exam_try');

module.exports = { bucket, storage };
