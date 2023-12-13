const { usersRef } = require('../db/firebase');
const { v4: uuidv4 } = require('uuid');
const { bucket } = require('../db/cloudStorage');

const addFiles = async (req, res) => {
  try {
    const uploadedFile = req.files;
    const documentId = req.user.uid;
    if (!uploadedFile || uploadedFile.length === 0) {
      return res.status(400).json({ error: 'File not Found' });
    }

    const uploadedData = [];

    for (const file of uploadedFile) {
      const fileId = uuidv4();
      const fileName = `${fileId}_${file.originalname}`;
      const storageFile = bucket.file(fileName);
      await storageFile.save(file.buffer);
      const publicUrl = `https://storage.googleapis.com/${bucket.name}/${fileName}`;

      const fileData = {
        fileId: fileId,
        fileName: file.originalname,
        fileType: file.mimetype,
        storageUrl: publicUrl,
        createdAt: new Date(),
      };

      await usersRef
        .doc(documentId)
        .collection('files')
        .doc(fileId)
        .set(fileData);

      uploadedData.push(fileData);
    }

    res.json({
      message: 'Document successfully uploaded',
      data: uploadedData,
    });
  } catch (err) {
    console.log(err);
    res
      .status(500)
      .json({ error: 'An error occured while uploading document' });
  }
};

const getFiles = async (req, res) => {
  try {
    const documentId = req.user.uid;

    const querySnapshot = await usersRef
      .doc(documentId)
      .collection('files')
      .get();

    const files = [];
    querySnapshot.forEach((doc) => {
      files.push(doc.data());
    });

    res.json({
      message: 'Files successfully retrieved',
      data: files,
    });
  } catch (err) {
    console.log(err);
    res.status(500).json({ error: 'An error occurred while fetching files' });
  }
};

const getFileById = async (req, res) => {
  try {
    const documentId = req.user.uid;
    const fileId = req.params.fileId;

    const fileDoc = await usersRef
      .doc(documentId)
      .collection('files')
      .doc(fileId)
      .get();

    if (!fileDoc.exists) {
      return res.status(404).json({ error: 'File not found' });
    }

    const fileData = fileDoc.data();

    res.json({
      message: 'File successfully retrieved',
      data: fileData,
    });
  } catch (err) {
    console.log(err);
    res
      .status(500)
      .json({ error: 'An error occurred while fetching the file' });
  }
};

const deleteFile = async (req, res) => {
  try {
    const documentId = req.user.uid;
    const fileId = req.params.fileId;

    // Periksa apakah file ada sebelum dihapus
    const fileDoc = await usersRef
      .doc(documentId)
      .collection('files')
      .doc(fileId)
      .get();

    if (!fileDoc.exists) {
      return res.status(404).json({ error: 'File not found' });
    }

    // Hapus file dari storage
    const fileName = `${fileId}_${fileDoc.data().fileName}`;
    const storageFile = bucket.file(fileName);
    await storageFile.delete();

    // Hapus file dari Firestore
    await usersRef.doc(documentId).collection('files').doc(fileId).delete();

    res.json({
      message: 'File successfully deleted',
    });
  } catch (err) {
    console.log(err);
    res
      .status(500)
      .json({ error: 'An error occurred while deleting the file' });
  }
};

module.exports = { addFiles, getFiles, getFileById, deleteFile };