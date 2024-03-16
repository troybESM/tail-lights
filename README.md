<!--
title: 'AWS Serverless example in Python'
description: 'This template demonstrates how to make a simple HTTP API with Python running on AWS Lambda and API Gateway using the Serverless Framework.'
layout: Doc
framework: v3
platform: AWS
language: python
authorLink: 'https://github.com/serverless'
authorName: 'Serverless, inc.'
authorAvatar: 'https://avatars1.githubusercontent.com/u/13742415?s=200&v=4'
-->

# Serverless Framework Python on AWS

This repository serves as a demonstrative platform for showcasing the capabilities of Python lambdas and serverless architectures, providing developers with a reference for understanding these technologies.

It has examples of these services:

- API Gateway
- DynamoDB
- S3
- SNS
- SQS

For each of these (except s3 for policy reasons) we stand up all of the infrastructure that we need for a given environment.

## Usage


## Services

### API Gateway

```mermaid
  flowchart LR
    User(User)
    subgraph AWS
    API_Gateway(API_Gateway) --> /(/)
    API_Gateway --> /hello(/hello)
    API_Gateway --> A{Authorized}  
    A{Authorized} -->|Yes| /hello/$name(/hello/$name)
    / --> Lambda:API
    /hello --> Lambda:API
    /hello/$name --> Lambda:API
    end
    A{Authorized} -->|No| Forbidden
    style Forbidden stroke:#f66,stroke-width:2px,color:#fff,stroke-dasharray: 5 5
    User --> API_Gateway
```

### Deployment

This repo is setup to deploy `main` and `feature*` branches to the devs-sbx aws account via github actions (check the .github/workflows directory)

Should you want to deploy from local (not recommended) you would need to setup your aws credentials in your terminal before running anything.

```bash
serverless deploy
```

After deploying, you should see output similar to:

```bash
Deploying aws-python-http-api-project to stage dev (us-east-1)

✔ Service deployed to stack aws-python-http-api-project-dev (140s)

endpoint: GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/
functions:
  hello: aws-python-http-api-project-dev-hello (2.3 kB)
```

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


## Development

## git feature branch workflow

```mermaid
gitGraph TB:
   commit
   
   branch feature/feature1
   checkout feature/feature1
   commit tag: "Stand up ephemeral dev"
   commit tag: "Modify env based on changes"
   checkout main
   merge feature/feature1 tag: "Deploy main and destroy feature branch"
   branch feature/feature2
   checkout feature/feature2
   commit tag: "Stand up ephemeral dev"
   commit tag: "Modify env based on changes"
   checkout main
   branch feature/feature3
   checkout feature/feature3
   commit tag: "Stand up ephemeral dev"
   commit tag: "Modify env based on changes"
   checkout main
   merge feature/feature3 tag: "Deploy main and destroy feature branch"
   checkout feature/feature2
   commit tag: "Pull in upstream changes"
   checkout main
   merge feature/feature2 tag: "Deploy main and destroy feature branch"
```