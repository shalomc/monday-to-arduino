const AWS = require('aws-sdk');

exports.handler = async (event, context) => {
  // Check if the path is "/xxxxx", method is POST, and query string contains "key=yyyyyyyyy"
  const isRequestValid = (
    event.path === '/xxxxx' &&
    event.httpMethod === 'POST' &&
    event.queryStringParameters &&
    event.queryStringParameters.key === 'yyyyyyyyy'
  );

  if (isRequestValid) {
    // Get the SQS URL from an environment variable
    const sqsUrl = process.env.SQS_URL;

    // Create an SQS client
    const sqs = new AWS.SQS({ region: 'us-east-1' }); // Replace with the correct region

    // Get the number of messages on the SQS queue
    const numMessages = await sqs.getQueueAttributes({
      QueueUrl: sqsUrl,
      AttributeNames: ['ApproximateNumberOfMessages']
    }).promise()
      .then(data => data.Attributes.ApproximateNumberOfMessages);

    // Delete the messages on the SQS queue
    await sqs.purgeQueue({ QueueUrl: sqsUrl }).promise();

    // Return the number of deleted messages
    return {
      statusCode: 200,
      body: `Deleted ${numMessages} messages from the SQS queue`
    };
  } else {
    // Return an error if the request is invalid
    return {
      statusCode: 400,
      body: 'Invalid request'
    };
  }
};
