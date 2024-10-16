const express = require('express');
const bodyParser = require('body-parser');
const AWS = require('aws-sdk');
const cors = require('cors');

const app = express();
app.use(bodyParser.json());

app.use(cors());

require('dotenv').config();


AWS.config.update({
  region: process.env.AWS_REGION, 
});

const sqs = new AWS.SQS({
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    region: process.env.AWS_REGION,
  });


app.post('/users', async (req, res) => {
  const { name, email, age } = req.body;

  const isValidEmail = (email) => /\S+@\S+\.\S+/.test(email);
  if (!name || !email || !age || !isValidEmail(email) || isNaN(age)) {
    return res.status(400).send('Invalid input data');
  }


  const params = {
    MessageBody: JSON.stringify({ name, email, age }),
    QueueUrl: process.env.QUEUE_URL,
  };

  try {
    await sqs.sendMessage(params).promise();
    res.status(201).send('Message sent to SQS');
  } catch (error) {
    console.error('Error sending message to SQS:', error);
    res.status(500).send('Failed to send message');
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
