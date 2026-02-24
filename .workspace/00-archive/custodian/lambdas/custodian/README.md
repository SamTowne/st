# Custodian Lambda Function

This AWS Lambda function, named "custodian", serves two main purposes: data collection and policy enforcement. 

## Data Collection

The "custodian" Lambda function is configured to run Cloud Custodian, an open-source rules engine for AWS resource management. It collects data about AWS resources according to the policies defined in Cloud Custodian. 

The function is scheduled to run at regular intervals using Amazon CloudWatch Events. The data collected by the function is stored in an Amazon S3 bucket for further processing and analysis.

## Policy Enforcement

In addition to data collection, the "custodian" Lambda function also serves as a policy enforcement tool. 

Cloud Custodian policies define the desired state of AWS resources. When the "custodian" function runs, it evaluates the current state of AWS resources against these policies. If a resource is found to be non-compliant with a policy, the function takes action as defined in the policy. This could be anything from sending a notification to modifying the resource or even deleting it.

This "policy as code" approach allows for automated, scalable, and repeatable management of AWS resources.
