
# Serverless Framework Python on AWS

This repo serves as the backend api for the oco front-end rewrite. 

It makes us of these services:

- API Gateway
- DynamoDB
- S3
- Lambda

For each of these we stand up all of the infrastructure that we need for a given environment.


### Deployment

This repo is setup to deploy `main` and `feature*` branches to the devs-sbx aws account via github actions (check the .github/workflows directory)

>⚠️
> In current form, after deployment, your API is public and can be invoked by anyone. For production deployments, you might want to configure an authorizer. For details on how to do that, refer to [http event docs](https://www.serverless.com/framework/docs/providers/aws/events/apigateway/).


### Invocation

After successful deployment, you can call the created application via HTTP:

```bash
curl https://xxxxxxx.execute-api.us-east-1.amazonaws.com/
```

Which should result in response similar to the following (removed `input` content for brevity):

```json
{
  "message": "Go Serverless v3.0! Your function executed successfully!",
  "input": {
    ...
  }
}
```

### Local development

You can invoke your function locally by using the following command:

```bash
serverless invoke local --function hello
```

There are also some example test events in the test directory. We created one for each of the processor lambdas. You can pass them into invoke local like this:

```bash
serverless invoke local --function sqsProcessor --path .\test\sqs.json
```

You can read more about invoke local here:
<https://www.serverless.com/framework/docs/providers/aws/cli-reference/invoke-local>
