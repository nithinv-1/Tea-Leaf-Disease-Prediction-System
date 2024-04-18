const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');
const app = express();
const PORT = 3001;
const { spawn } = require('child_process');

app.use(express.json());
app.use(cors());

const uploadDir = path.join(__dirname, '../public/uploads');

// Endpoint to handle saving the captured image
app.post('/save-image', (req, res) => {
  const { imageData } = req.body;

  if (!imageData) {
    return res.status(400).send('No image data provided');
  }

  const base64Data = imageData.replace(/^data:image\/jpeg;base64,/, '');

  const fileName = `captured_image_${Date.now()}.jpg`;
  
  
  console.log("up",uploadDir);
  if (!fs.existsSync(uploadDir)) {
    fs.mkdirSync(uploadDir);
  }

  // Write the file to the uploads directory
  const filePath = path.join(uploadDir, fileName);
  fs.writeFile(filePath, base64Data, 'base64', (err) => {
    if (err) {
      console.error('Error saving image:', err);
      return res.status(500).send('Error saving image');
    }
    console.log('Image saved successfully:', fileName);
    res.send('Image saved successfully');
  });
});

//view image
app.get('/images', (req, res) => {
    console.log(uploadDir)
    fs.readdir(uploadDir, (err, files) => {
      if (err) {
        console.error('Error reading directory:', err);
        res.status(500).send('Internal Server Error');
      } else {
        const imageDetailsPromises = files.map((file, index) => {
          const filePath = path.join(uploadDir, file);
          return new Promise((resolve, reject) => {
            fs.stat(filePath, (err, stats) => {
              if (err) {
                console.error('Error getting file stats:', err);
                reject(err);
              } else {
                const formattedDate = stats.birthtime.toLocaleString(); // Format the creation date and time
                resolve({
                  serialNumber: index + 1,
                  fileName: file,
                  imageUrl: `uploads/${file}`,
                  uploadDateTime: formattedDate
                });
              }
            });
          });
        });
  
        Promise.all(imageDetailsPromises)
          .then(imageDetails => {
            res.json(imageDetails);
          })
          .catch(error => {
            res.status(500).send('Internal Server Error');
          });
      }
    });
  });

// DELETE endpoint for deleting an image
app.delete('/images/:fileName', (req, res) => {
    const fileName = req.params.fileName;
    const filePath = path.join(uploadDir, fileName);
    console.log('Deleting file:', filePath);
    fs.unlink(filePath, (err) => {
      if (err) {
        console.error('Error deleting file:', err);
        res.status(500).send('Internal Server Error');
      } else {
        res.status(200).send('File deleted successfully');
      }
    });
  });



//Compute model
app.get('/compute/:fileName', (req, res) => {
  try {
    const fileName = req.params.fileName;
    const filePath = path.join(uploadDir, fileName);

    // Spawn a child process to run Pred.py with the file path parameter
    const pythonProcess = spawn('python', ['../public/Pred.py', filePath], {
      stdio: ['pipe', 'pipe', 'pipe'] // Pipe stderr as well
    });

    // Collect stdout and stderr data
    let stdoutData = '';
    let stderrData = '';

    // Listen for data from stdout
    pythonProcess.stdout.on('data', (data) => {
      stdoutData += data.toString();
    });

    // Listen for data from stderr
    pythonProcess.stderr.on('data', (data) => {
      stderrData += data.toString();
    });

    // Listen for process exit event
    pythonProcess.on('exit', (code) => {
      if (code === 0) {
        // If the process exits successfully (code 0), log the stdout data
        console.log('Python script output:', stdoutData);

        // Extract JSON data from stdout
        const jsonData = stdoutData.match(/\{.*\}/s);

        if (jsonData) {
          try {
            // Parse the matched JSON data
            const output = JSON.parse(jsonData[0]);
            console.log(output);
            res.json(output);
          } catch (error) {
            console.error('Error parsing JSON:', error);
            console.log('stdoutData:', stdoutData); // Log the stdoutData for inspection
            res.status(500).json({ success: false, error: 'Internal Server Error' });
          }
        } else {
          console.error('No JSON data found in stdout:', stdoutData);
          res.status(500).json({ success: false, error: 'Internal Server Error' });
        }
      } else {
        // If the process exits with an error (non-zero code), send an error response including stderr data
        console.error(`Python script execution failed with code ${code}. stderr: ${stderrData}`);
        res.status(500).json({ success: false, error: 'Internal Server Error', stderr: stderrData });
      }
    });
  } catch (error) {
    console.error('Error running Python script:', error);
    res.status(500).json({ success: false, error: 'Internal Server Error' });
  }
});



  
  

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
  });
  