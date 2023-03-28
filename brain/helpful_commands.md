## Splunk

### Filters
- index=aws | filters out non-aws logs, depends on the splunk configuration but is pretty common to use multiple indexes to split data by source environment
- eventSource="lambda.amazonaws.com" | filter to events origininating from a specific AWS service
- eventName | the API action being invoked in the event
- errorCode=* | wildcard search for any errors

### Example queries
1. Find non_compliant config rules
  - index=aws eventSource="config.amazonaws.com" eventName=PutEvaluations "requestParameters.evaluations{}.complianceType"=NON_COMPLIANT
  - to filter by account add: recipientAccountId=123456789123
2. Find errors with IAM User Roles assumed by a user id
  - index=aws errorCode=* repientAccount=123456789123 "userIdentity.arn"="arn:aws:sts::123456789123:assumed-role/role_name_here/user_id_here"
3. Service role events
  - index=aws "userIdentity.arn"="arn:aws:sts::123456789123:assumed-role/role_name_here"
  - use eventName to search for event type: eventName=StartQueryExecution
  - arn supports wildcards
4. Getting Athena Query by execution ID (sts assumed role in use)
  - index=aws "userIdentity.arn"="arn:aws:sts::123456789123:assumed-role/role_name_here/user_id_here" eventName=StartQueryExecution queryExecutionId=eus8s8k-aghfiah-safhsadfb-aksdf
5. To get a quicksight dashboard ID
  - index=aws "userIdentity.arn"="arn:aws:sts::123456789123:assumed-role/role_name_here/user_id_here" eventName=CreateDashboard