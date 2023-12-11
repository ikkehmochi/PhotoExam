const express = require('express');
const fileRoutes = require('./routes/fileRoutes');
const app = express();
const port = 3030;

app.use('/api', fileRoutes);

app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
