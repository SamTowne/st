# AgentCore User Guide Review
These are notes from the user guide. 

need to dig deeper into bedrock and agentcore build enough of a foundation to enable a PoC that is aligned with AI policy and security requirements:
- align to sso, people must be logging in as themselves
- we will need to take a whitelist approach on the permission set, 
- force use of a role-per-model/fm
- set up a limited execution role/trust
- no public endpoint use, we need to do vpc endpoint / privatelink with a policy for the per-model-role(s)
- we can probably provision a reusable module where we can pass the model name/version and build all the named resources to support least privilege for a single FM in a single account, curious if there is also an org-wide implementation guide for approved models
- have a feeling we are going to eval multiple models here so repeatability of the permission set is important, ideally minimal inputs required besides picking a model name/version
- do we need a separate module for agentcore resources or can that be included?
- probably take a map of maps as input and then build the config off that for the multiple agents use case
- to keep things really light here, perhaps we just keep IAM/network/identity/guardrail in-scope for the module and as long as they use the roles provisioned by this they can do whatever they want and remain aligned to requirements from security
- suspect the guardrail is a one-time config (per region?) and we can likely enforce using it on invocations to the services with an IAM conditional for the header, there's an example in their least privilege blog post of that on a VPC endpoint policy, good guardrail to have
- how to reduce risk of keys being leaked? not something gitleaks would catch, people are logging into an ec2/containers with keys to validate... we can recommend as-code secretsmanager use as well as limiting key scopes for any integrations for agentcore agents
- TODO:
  - review the use case with the app team and ask a lot of questions
    - can you walk us through the solution?
    - what FMs/models are you planning to use? let's pick one to start with for an initial validation of the permission set, then we can reuse that code for any other models
    - can you walk me through the components in the architecture diagram and agent configuration? ec2, lambda, s3, 6 agentcore agents, couple external systems
    - Are you wanting to validate Agent to Agent features? 
    - I am thinking about how we can best support this work and gain faster cycle times for progress. This is the first bedrock and agentcore use case so all of the platform-level security controls need to be put in place before org data can be leveraged. This represents a large amount of work which we are happy to do once we have working PoC. I am looking to understand how far along we are in this process, and how far along we can go without using org data.
    - This seems like a sandbox exploratory use-case to me. Sandboxes are off the company network. Because of that, With sandbox aws accounts, we can follow any of the aws guides for exploring bedrock and agentcore with broad permission sets. I am not understanding how we got to needing the prod requirements for a PoC evaluation. This is the exact situation where sandbox makes sense (to enable rapid iteration for project). Am I understanding?
    - do you know if SSO integration into agentcore was addressed in the solution review with architecture? can integrate with our stuff just curious if this came up, adds a pretty big additional scope for a PoC here so is there a chance we can do all this prep work in a sandbox where that won't be required and then promote after we do a bunch of fast iterations so we can scope out the pltform products to support this?
  - determine agentcore protocol type HTTP/MCP/A2A
  - get clear about integrations to external things
  - 

## What can you build with Amazon Bedrock AgentCore?
- agents, tools and MCP servers and agent platforms
- we probably need to jump straight towards an agent platform approach here to meet controls
- **agent platforms** Provide your internal developers or customers with a paved path to build and deploy agents using approved tools, shared memory stores, and governed access to enterprise services. Centralize observability, authentication, and compliance while enabling teams to ship agent-powered features faster.

## Pricing
- [link](https://aws.amazon.com/bedrock/agentcore/pricing/)

## Regions
- US East 1 and 2, US west Oregon
- **warning** us-east-2 does not support AgentCore Evaluations, use1 and oregon do though...
- evaluations are a way to measure performance on your model use, doubt this is critical for PoC

## Get started with Amazon Bedrock AgentCore
- diagram of the quickstart process
- step 1 creates an agent via cli, then you pick a start script, framework, integrations, IaC provider and additional configurations
  - TODO: is this configuration leveraging the aws provided examples? those are basically using * permissions everywhere from an initial look
- ohhh, its in pip `pip install bedrock-agentcore-starter-toolkit`
- with it installed `agentcore create`
- The above command: bootstraps a simple agent in Strands Agents, LangGraph, OpenAI Agents Software Development Kit or Google Agent ToolkitDevelopment Kit (you can pick which framework) uses a foundation model from model providers including Amazon Bedrock, OpenAI, Google's Gemini, Anthropic's Claude, Amazon Nova, Meta Llama, and Mistral (you can pick which model provider) produces either a project folder in Python with a simple agent, or Infrastructure as Code (IaC) ready code in Terraform or Cloud Development Kit (CDK) (you can pick) automatically creates Gateway, Memory, and enables Observability automatically configures role, entrypoint, requirements and auth model

## Understand the available interfaces for using Amazon Bedrock AgentCore
- Amazon Bedrock AgentCore supports various interfaces for developing and deploying your agent code. The simplest approach is to use the AgentCore Python SDK to create your agent code and use the AgentCore starter toolkit to deploy your agent. The AgentCore starter toolkit and AgentCore Python SDK don't support all AgentCore operations that the AWS SDK supplies. If they don't support a specific AgentCore operation, use the AWS SDK.

## Amazon Bedrock AgentCore starter toolkit
- AgentCore [starter toolkit](https://github.com/aws/bedrock-agentcore-starter-toolkit)
- abstractions for create, deploy, import agent, gateway integration, memory management, configuration management, observabiltiy, evals

## AgentCore Python SDK
- python [sdk](https://github.com/aws/bedrock-agentcore-sdk-python)
- has support for runtime, memory, tools, identity, evals

## Amazon Bedrock AgentCore MCP server
- The AgentCore Model Context Protocol (MCP) server helps you transform, deploy, and test AgentCore-compatible agents directly from your preferred development environment. With built-in support for runtime integration, gateway connectivity, and agent lifecycle management, the MCP server simplifies moving from local development to production deployment on AgentCore services.
- we probably want this as part of the "agent platform"
- not quite understanding the qmetry use case, but using MCP seems like a fast way to start trying things out from the normal dev setup
- they link to an article about [vibe coding with bedrock agentcore mcp server](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/mcp-getting-started.html) nice

## AWS SDK
- You can use the AWS SDK to achieve the same results as the AgentCore Python SDK, as well as other tasks that the AgentCore Python SDK doesn't support. You'll need to use the AWS SDK to interact with other AWS services such as AWS Lambda and Amazon S3. You'll also need to the AWS SDK if you aren't using Python as your coding language.
- they link to a document for AgentCore data plane API and as of Feb 21 2026 the page only has 3 sentances, looks like a WIP page

## Amazon Bedrock AgentCore console
- Suspect this is what the PoC group wants to do
- need to discuss the diagrams and get expectations alignment
- if sec requires least privilege and role-per-FM permission sets with no * permissions for actions, and app team wants console use and has not provided specific simplified implementation plan... I have little detail about the workload, model selected, etc. we cannot actually do what everyone is wanting here
- we can just watch them get access denieds, clarify if they actually need it, then add to permissions scope? lol, but then we need a repeatable set of IAM for switching between FMs, perhaps they know which one they'd like to start with
- diagram is super high-level about the use case
- has like 6 agents, an ec2, lambda, and a couple external services jira and qmetry, glad to help but we are going to need to walk through this together, one diagram super high level in a powerpoint is not going to cut it for me to make everyone happy
-  thinking we need to get controls in place at network level sufficient for security to let this team try things out
- vpc + endpoint + endpoint policy with conditions to enfore
  - principal arn (they must use the role provisioned)
  - guardrail use (they must use the guardrail on actions that support it)
  - actions restricted to a limited set of FMs (single FM per role)
  - review all IAM actions for bedrock and bedrock-agentcore to try and align with the use case and be sure to not include any actions that would go against sec guidance, need to set this up so that I can provide a general path forward and let the app team and security negotiate IAM scope, cannot be in the middle other than to facilitate expectations alignment here, it is completely understandble why least privilege is important here, we cant just throw data around
- more details required, and a better understanding of the use case
- console [link](https://console.aws.amazon.com/bedrock-agentcore/home#)

## Host agent or tools with Amazon Bedrock AgentCore Runtime
Amazon Bedrock AgentCore Runtime provides a secure, serverless and purpose-built hosting environment for deploying and running AI agents or tools. It offers the following benefits:
- framework agnostic
- model flexibility
- protocol support
- **session isolation** In AgentCore Runtime, each user session runs in a dedicated microVM with isolated CPU, memory, and filesystem resources. This helps create complete separation between user sessions, safeguarding stateful agent reasoning processes and helps prevent cross-session data contamination. After session completion, the entire microVM is terminated and memory is sanitized, delivering deterministic security even when working with non-deterministic AI processes.
- Extended execution time AgentCore Runtime supports both real-time interactions and long-running workloads up to 8 hours
- consumption based pricing
- **Built-in authentication** AgentCore Runtime, powered by AgentCore Identity, assigns distinct identities to AI agents and seamlessly integrates with your corporate identity provider such as Okta, Microsoft Entra ID, or Amazon Cognito, enabling your end users to authenticate into only the agents they have access to. In addition, Runtime lets outbound authentication flows to securely access third-party services like Slack, Zoom, and GitHub - whether operating on behalf of users or autonomously (using either OAuth or API keys).
- agent specific observability
- enhanced payload handling
- bidirectional streaming w/ http and websocket
- unified set of agent-specific capabilities (memory, tools, gateway)

## How it works
The Amazon Bedrock AgentCore Runtime handles scaling, session management, security isolation, and infrastructure management, allowing you to focus on building intelligent agent experiences rather than operational complexity. By leveraging the features and capabilities described here, you can build, deploy, and manage sophisticated AI agents that deliver value to your users while helping to maintain enterprise-grade security and reliability.

## Key components
- **AgentCore Runtime** An AgentCore Runtime is the foundational component that hosts your AI agent or tool code. It represents a containerized application that processes user inputs, maintains context, and executes actions using AI capabilities. When you create an agent, you define its behavior, capabilities, and the tools it can access. For example, a customer support agent might answer product questions, process returns, and escalate complex issues to human representatives. You can build and deploy agents to AgentCore Runtime using the AgentCore Runtime starter toolkit, the AgentCore Python SDK or directly through AWS SDKs. With the AgentCore Python SDK, you can define your agent using popular frameworks like LangGraph, CrewAI, or Strands Agents. The SDK handles infrastructure complexities, allowing you to focus on the agent's logic and capabilities.
- Each AgentCore Runtime: Has a unique identity and Is versioned to support controlled deployment and updates

## Versions
- Each AgentCore Runtime maintains immutable versions that capture a complete snapshot of the configuration at a specific point in time: When you create an AgentCore Runtime, Version 1 (V1) is automatically created Each update to configuration (container image, protocol settings, network settings) creates a new version Each version contains all necessary configuration needed for execution This versioning system provides reliable deployment history and rollback capabilities.

## Endpoints
- Endpoints provide addressable access points to specific versions of your AgentCore Runtime. Each endpoint: Has a unique ARN for invocation References a specific version of your Agent Runtime Provides stable access to your agent even as you update implementations
- Key endpoint details: The "DEFAULT" endpoint is automatically created when you call CreateAgentRuntime and points to the latest version When you update your AgentCore Runtime, a new version is created but the DEFAULT endpoint automatically updates to reference it
You can create custom endpoints with the CreateAgentRuntimeEndpoint operation for different environments (dev, test, prod) When a user makes a request to an endpoint, the request is resolved to the specific agent version referenced by that endpoint
- Endpoints have distinct lifecycle states:CREATING - Initial state during endpoint creation CREATE_FAILED - Indicates creation failure due to permissions or other issues READY - Endpoint is operational and accepting requests UPDATING - Endpoint is being modified to reference a new version UPDATE_FAILED - Indicates update operation failure You can update endpoints without downtime, allowing for seamless version transitions and rollbacks.
- feels like lambda aliasing or ecr

## Sessions
- Sessions represent individual interaction contexts between users and your AgentCore Runtime. Each session: Is identified by a unique `runtimeSessionId` provided by your application, or by the Runtime itself in the first invocation if the `runtimeSessionId` is left empty Runs in a dedicated microVM with completely isolated CPU, memory, and filesystem resources Preserves context across multiple interactions within the same conversation Can persist for up to 8 hours of total runtime
- After session termination, the entire microVM is terminated and memory is sanitized
- sessions are isolated
- Session state is ephemeral and should not be used for long-term durability (use AgentCore Memory for context durability)

## Authentication and security
Inbound authentication controls who can access your agents through AWS Identity and Access Management or OAuth 2.0, validating bearer tokens from identity providers before allowing requests to proceed. Outbound authentication enables your agents to securely access third-party services using OAuth or API keys, with AgentCore Identity managing credentials in either user-delegated or autonomous modes. For more information, see Authenticate and authorize with Inbound Auth and Outbound Auth.
- inbound auth is what they call AgentCore Identity
- auth methods AWS IAM and OAuth
- OAuth configuration options: Discovery URL: Your identity provider's OpenID Connect discovery endpoint Allowed Audiences: List of valid audience values your tokens should contain Allowed Clients: List of client identifiers that can access this agent

## Authentication flow
1. End users authenticate with your identity provider (Amazon Cognito, Okta, Microsoft Entra ID)
2. Your client application receives a bearer token after successful authentication
3. The client passes this token in the authorization header when invoking the agent
4. AgentCore Runtime validates the token with the authorization server
5. If valid, the request is processed; if invalid, it's rejected
This ensures only authenticated users with proper authorization can access your agents.

## Outbound authentication
- Outbound Auth, powered by Amazon Bedrock AgentCore Identity, lets your agents hosted on AgentCore Runtime securely access third-party services, not going to put all of the additional stuff here but there are a couple built in integrations and then you use api keys, we will need to make sure we make them aware of the secretsmanager module they can use for those

## Additional features
- async processing, streaming responses, websocket api, protocol support for HTTP MCP and A2A
- there are additional docs for each of these available

## Implementation overview
- prpare your agent or tool code, deploy your agent or tool, invoke your agent or tool, manage and observe sessions and make updates
- perhaps there is agent code for the use case or some pseudocode started here that we can leverage for the permision sets and getting them started

## Understand the AgentCore Runtime service contract
The AgentCore Runtime service contract defines the standardized communication protocol that your agent application must implement to integrate with the Amazon Bedrock agent hosting infrastructure. This contract ensures seamless communication between your custom agent code and AWS's managed hosting environment
- theres a table with th protocol comparisons, ports, mount paths, msf format and more
- we will need to determine which type of protocols are needed for the use case, suspect http from the diagram in the ppt

## HTTP protocol contract
- Your agent must be deployed as a containerized application meeting these specifications: Host: 0.0.0.0Port: 8080 - Standard port for HTTP-based agent communicationPlatform: ARM64 container - Required for compatibility with the AgentCore Runtime environment
- path, /invocations POST primary endpoint recievies icoming requests from users or apps and processes them w the agents business logic
The /invocations endpoint serves several key purposes:Direct user interactions and conversations API integrations with external systems Batch processing of multiple requestsReal-time streaming responses for long-running operations
- websocket available at /ws also on 8080
- /ping route is basically status check or test route
- will return 401s for oauth failure or auth header missing
- sigv4 will return 403 and will not include WWW-Authenticate headers

## MCP
skip for now

## A2A
skip for now

## IAM Permissions for AgentCore Runtime
The following are IAM permissions you need to create an agent in an AgentCore Runtime and the execution role permissions that an agent needs to run in an AgentCore Runtime. You can also use resource-based policies to control access to your runtime resources.
- the managed policy BedrockAgentCoreFullAccess is broad, we will need to scope something down.
- the starter toolkit is also broad permissions
- The IAM policies created by the starter toolkit are designed for development and testing purposes. These permissions grant broad access to facilitate rapid prototyping and are not suitable for production environments. For production deployments, create custom IAM policies that follow the principle of least privilege and restrict permissions to only the specific resources and actions required by your Bedrock AgentCore application.
- there is a plocy statement jsno here
- statements for agentcore role, service-role, starter kit uses codebuild
- perhaps we can just update the scope of the PoC to not include any cmopany data, and then use broad permission set in a lower env or sandbox for now, I am not understanding the neeed to do cmopany data right away when the scope is clearly at spike-level from what I can tell, just mock some of the jira apis/qmetry for now>????
- then, when we are ready and know the approach and solution I will be able to scope some guardrails an roles that match the use case in alignment with sec requirements
- I think that the expectation is that we give full access and let them run
- We need to uncover that and align
- Lab provides full access by default
- It is up to them what they do beyond that
- If they want a least-privilege guardrails enforced environment, I can help provision for that but need more detail on the model in use and naming convention for resources, and the app-flow diagram or something else to help me understand the use case
- agentcore execution role is another control for action limiting...
- trust example
```json
{
  "Version":"2012-10-17",		 	 	 
  "Statement": [
    {
      "Sid": "AssumeRolePolicy",
      "Effect": "Allow",
      "Principal": {
        "Service": "bedrock-agentcore.amazonaws.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
            "StringEquals": {
                "aws:SourceAccount": "123456789012"
            },
            "ArnLike": {
                "aws:SourceArn": "arn:aws:bedrock-agentcore:us-east-1:123456789012:*"
            }
       }
    }
  ]
}
```

## Get started with AgentCore Runtime
- getting started guides here for python, typescript and without the starter toolkit, direct code deployment and websocket too


## Get started with the Amazon Bedrock AgentCore starter toolkit in Python
- uses anthropic claude sonnet 4.0
- agentcore runtime uses arm64

## Get started with the Amazon Bedrock AgentCore starter toolkit in TypeScript
- does not specify a model, only that you need to have selected model enabled in bedrock

## Get started without the starter toolkit
- suspect this is the path we'd want to align with
- You can create a AgentCore Runtime agent without the starter toolkit. Instead you can use a combination of command line tools to configure and deploy your agent to an AgentCore Runtime. This tutorial shows how to deploy a custom agent without using the starter toollkit. A custom agent is an agent built without using the AgentCore Python SDK. In this tutorial, the custom agent is built using FastAPI and Docker. The custom agent follows the AgentCore Runtime requirements, meaning the agent must expose /invocations POST and /ping GET endpoints and be packaged in a Docker container. Amazon Bedrock AgentCore requires ARM64 architecture for all deployed agents.
- still need to ask questions to the team to determine scope on the agent containers, seems like theres no way around ECR footprint here with everything so far, which is fine just another thing to add to the heap, aws example tf implementation repo has all the stuff we can go use that as a baseline and then least-privilege-align it
- they us uv package manager, thats a new one, nice
- this does the same thing as the other guides but w fastapi
- pretty sure we like fastapi so this might be the path
- [link](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/getting-started-custom.html)

## Add memory to your Amazon Bedrock AgentCore agent
AgentCore Memory is a fully managed service that gives your AI agents the ability to remember past interactions, enabling them to provide more intelligent, context-aware, and personalized conversations. It provides a simple and powerful way to handle both short-term context and long-term knowledge retention without the need to build or manage complex infrastructure.

AgentCore Memory addresses a fundamental challenge in agentic AI: statelessness. Without memory capabilities, AI agents treat each interaction as a new instance with no knowledge of previous conversations. AgentCore Memory provides this critical capability, allowing your agent to build a coherent understanding of users over time.

- diagram showing how mem allows agent to respon to user w/ contextual awareness

## Memory types
- short and long term memory
- long term spans across sessions, persistent knowledge retention across multiple sessions

## Memory key benefits
- conversational agents
- skipping the rest of this for now, memory use cases pretty obvious

## How it works
AgentCore Memory provides a set of APIs that let your AI agents seamlessly store, retrieve, and utilize both short-term and long-term memory. The architecture is designed to separate the immediate context of a conversation from the persistent knowledge that should be retained over time.
- fairly confident there are sequrity requirements for mem-use

# Memory terminology
- agentcore memory, primary top level container for mem resource
- memory strategy, configurable rules about how to process short-term memory into long-term memory, what type of information is kept
- namespace, structured path used to logically group and organize long-term memories
- memory record, structured unit of info within the memory resouce, each record has a unique identifier and is stored within a specified namespace
- session, single continuous interaction between a user and agent
- actor, represents the entity interacting with the agent
- event, fundamental unit of short-term memory
- event metadata, supplemntary information that provides context about an event in AgentCore memory

## Memory types
- short-term, stores raw interactions that help the agent maintain context within a single session
- longer-term, extracts structured information from short term memory to be retained across multiple sessions, preserves only the key insights such as sumamries of the conversations, facts and knowledge, or user preferences
- long-term memory extraction is an async process that runs in the background and automatically extracts insights after raw conversation/context is stored in short-term memory via `CreateEvent`, this efficiently consolidates key inforamtion with interrupting live interactions. here's what happens during long-term memory formation
- extraction: extract info from raw interactions
- consolidation: consolidate newly extracted information with existing information in agentcore memory
- long term memory records can be extracted to enhance agent responses, `RetrieveMemoryRecords` operation can be used to perform a semantic search to find memory records that are most relevant

## Memory strategies
In AgentCore Memory, you can add memory strategies to your memory resource. These strategies determine what types of information to extract from raw conversations. Strategies are configurations that intelligently capture and persist key concepts from interactions, sent as events in the CreateEvent operation. You can add strategies to the memory resource as part of CreateMemory or UpdateMemory operations. Once enabled, these strategies are automatically executed on raw conversation events associated with that memory resource to extract long-term memories.

## Built-in strategies
AgentCore handles all memory extraction and consolidation automatically with predefined algorithms.
AgentCore handles all memory extraction and consolidation automatically
No configuration required beyond basic trigger settings
Uses predefined algorithms optimized and benchmarked for common use cases
Suitable for standard conversational AI applications
Limited customization options
Higher cost for storage

## Built-in overrides
Extends built-in strategies with targeted customization while using an AgentCore managed extraction pipeline.

Extends built-in strategies with targetted customization
Allows modification of prompts while still using AgentCore managed extraction pipeline
Provides support for bedrock models (invoked in your account)
Lower cost for storage than built-ins

## Self-managed strategies
You have complete ownership of memory processing pipeline with custom extraction and consolidation algorithms.

Complete ownership of memory processing pipeline
Custom extraction and consolidation algorithms using any model, prompts, etc.
Full control over memory record schemas, namespaces etc.
Integration with external systems and databases
Requires infrastructure setup and maintenance
Lower cost for storage than built-in strategies
A single memory resource can be configured to utilize both built-in and custom strategies simultaneously, providing flexibility to address diverse memory requirements.

## Built-in strategies
AgentCore Memory provides built-in strategies to create memories. Each built-in strategy consists of steps to handle memory creation, including the following (different strategies employ different steps):

Extraction – Identifies useful insights from short-term memory to place into long-term memory as memory records.
Consolidation – Determines whether to write useful information to a new record or an existing record.
Reflection – Insights are generated across episodes.
Each step is defined by a system prompt, which is a combination of the following:

Instructions – Guide the LLM's behavior. Can include step-by-step processing guidelines (how the model should reason and extract or consolidate information).
Output schema – How the model should present the result.
Each memory strategy provides a structured output format tailored to its purpose. The output is not uniform across strategies, because the type of information being stored and retrieved differs. This maintains that each memory type exposes only the fields most relevant to its strategy. You can find the output formats in the system prompts for each strategy.

You can combine multiple strategies when creating memories.

## Semantic memory strategy
The semantic memory strategy is designed to identify and extract key pieces of factual information and contextual knowledge from conversational data. This lets your agent to build a persistent knowledge base about the entities, events, and key details discussed during an interaction.

## System prompt for semantic memory strategy
Extraction instructions
```
You are a long-term memory extraction agent supporting a lifelong learning system. Your task is to identify and extract meaningful information about the users from a given list of messages.

Analyze the conversation and extract structured information about the user according to the schema below. Only include details that are explicitly stated or can be logically inferred from the conversation.

- Extract information ONLY from the user messages. You should use assistant messages only as supporting context.
- If the conversation contains no relevant or noteworthy information, return an empty list.
- Do NOT extract anything from prior conversation history, even if provided. Use it solely for context.
- Do NOT incorporate external knowledge.
- Avoid duplicate extractions.

IMPORTANT: Maintain the original language of the user's conversation. If the user communicates in a specific language, extract and format the extracted information in that same language.
```
Extraction output schema
```
Your output must be a single JSON object, which is a list of JSON dicts following the schema. Do not provide any preamble or any explanatory text.

<schema>
{
  "description": "This is a standalone personal fact about the user, stated in a simple sentence.\\nIt should represent a piece of personal information, such as life events, personal experience, and preferences related to the user.\\nMake sure you include relevant details such as specific numbers, locations, or dates, if presented.\\nMinimize the coreference across the facts, e.g., replace pronouns with actual entities.",
  "properties": {
    "fact": {
      "description": "The memory as a well-written, standalone fact about the user. Refer to the user's instructions for more information the prefered memory organization.",
      "title": "Fact",
      "type": "string"
    }
  },
  "required": [
    "fact"
  ],
  "title": "SemanticMemory",
  "type": "object"
}
</schema>
```
consolidation instructions
```
You are a conservative memory manager that preserves existing information while carefully integrating new facts.

Your operations are:
- **AddMemory**: Create new memory entries for genuinely new information
- **UpdateMemory**: Add complementary information to existing memories while preserving original content
- **SkipMemory**: No action needed (information already exists or is irrelevant)

If the operation is "AddMemory", you need to output:
1. The `memory` field with the new memory content

If the operation is "UpdateMemory", you need to output:
1. The `memory` field with the original memory content
2. The update_id field with the ID of the memory being updated
3. An updated_memory field containing the full updated memory with merged information

## Decision Guidelines

### AddMemory (New Information)
Add only when the retrieved fact introduces entirely new information not covered by existing memories.

**Example**:
- Existing Memory: `[{"id": "0", "text": "User is a software engineer"}]`
- Retrieved Fact: `["Name is John"]`
- Action: AddMemory with new ID

### UpdateMemory (Preserve + Extend)
Preserve existing information while adding new details. Combine information coherently without losing specificity or changing meaning.

**Critical Rules for UpdateMemory**:
- **Preserve timestamps and specific details** from the original memory
- **Maintain semantic accuracy** - don't generalize or change the meaning
- Only enhance when new information genuinely adds value without contradiction
- Only enhance when new information is **closely relevant** to existing memories
- Attend to novel information that deviates from existing memories and expectations
- Consolidate and compress redundant memories to maintain information-density; strengthen based on reliability and recency; maximize SNR by avoiding idle words

**Example**:
- Existing: `[{"id": "1", "text": "Caroline attended an LGBTQ support group meeting that she found emotionally powerful."}]`
- Retrieved: `["Caroline found the support group very helpful"]`
- Action: UpdateMemory to `"Caroline attended an LGBTQ support group meeting that she found emotionally powerful and very helpful."`

**When NOT to update**:
- Information is essentially the same: "likes pizza" vs "loves pizza"
- Updating would change the fundamental meaning
- New fact contradicts existing information (use AddMemory instead)
- New fact contains new events with timestamps that differ from existing facts. Since enhanced memories share timestamps with original facts, this would create temporal contradictions. Use AddMemory instead.

### SkipMemory (No Change)
Use when information already exists in sufficient detail or when new information doesn't add meaningful value.

## Key Principles

- Conservation First: Preserve all specific details, timestamps, and context
- Semantic Preservation: Never change the core meaning of existing memories
- Coherent Integration: Lets enhanced memories read naturally and logically
```

- there are multiple memory strategies and I am going to skip through the rest of this part for now, just good to know there is a lot of flexibility and tuning when it comes to memory, definitely an important cost control item as well as user experience, one interesting one was **episodic memory strategy**, it basically retains a snippet of meaningful slices of user/system interactions and then uses those in a focused way as opposed to storing every event, note that there are namespaces where memories are stored and there are a few conventions in place depending on what startegy is in use
- also, self-managed strategy available, seems like you need to manage kms/CMK for this approach
- has infra documented for doing it yourself in this section and we can come back here as needed

## Memory organization in AgentCore Memory
You can set how short-term and long-term memories are organized in an AgentCore Memory. This lets you isolate memories by session and by actor. For long-term memory, you can also set a namespace to organize the extracted memories for a memory strategy.

Actor – Refers to entities such as end users or agent/user combinations. For example, in a coding support chatbot, the actor is usually the developer asking questions. Using the actor ID helps the system know which user the memory belongs to, keeping each user's data separate and organized.
Session – A single conversation or interaction period between the user and the AI agent. It groups all related messages and events that happen during that conversation.
Strategy (Long-term memory only) – Shows which long-term memory strategy is being used. This strategy identifier is auto-generated when you create an AgentCore Memory
- goes deeper into short term and long term organization, short-term memories happen via **CreateEvent**, long-term memories are where memory strategies are created
- Every time AgentCore Memory extracts a new long-term memory with a memory strategy, the long-term memory is saved under the namespace you set. This means that all long-term memories are scoped to their specific namespace, keeping them organized and preventing any conflicts with other users or sessions. You should use a hierarchical format separated by forward slashes /, ending with a trailing slash. The trailing slash prevents prefix collisions in multi-tenant applications—for example, use /actors/Alice/ instead of /actors/Alice. As needed, you can use the following pre-defined variables within braces in the namespace based on your application's organization needs: actorId strategyId sessionId
- path based schema for accessing long term memories
- convention: /strategy/{memoryStrategyId}/actor/{actorId}/session/{sessionId}/
- example memory within: /strategy/summarization-93483043/actor/actor-9830m2w3/session/session-9330sds8/

## Restrict access with IAM
You can create IAM policies to restrict memory access by the scopes you define, such as actor, session, and namespace. Use the scopes as context keys in your IAM polices.

The following policy restricts access to retrieving memories to a specific namespace prefix. In this example, the policy allows access only to memories in namespaces starting with summaries/agent1/, such as summaries/agent1/session1/ or summaries/agent1/session2/.

```json
{
  "Version":"2012-10-17",		 	 	 
  "Statement": [
    {
      "Sid": "SpecificNamespaceAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:RetrieveMemoryRecords"
      ],
      "Resource": "arn:aws:bedrock-agentcore:us-east-1:123456789012:memory/memory_id",
      "Condition": {
        "StringLike": {
          "bedrock-agentcore:namespace": "summaries/agent1/"
        }
      }
    }
  ]
}
```

## Compare long-term memory with Retrieval-Augmented Generation
- Long-term memory in Amazon Bedrock AgentCore Memory serves as persistent storage for session-specific context, enabling agents to maintain continuity and personalization across interactions. Use long-term memory to store user preferences, past decisions, conversation history, and behavioral patterns that help agents adapt and feel personal without repeatedly requesting the same information. This memory type is ideal for tracking who the user is, what has happened in previous sessions, and maintaining state across multi-step workflows.

- Retrieval-Augmented Generation (RAG) complements long-term memory by providing access to authoritative, current information from large-scale repositories. Use these system to retrieve up-to-date documentation, technical specifications, policies, and domain expertise that may be too large or volatile for long-term storage. RAG ensures factual accuracy by pulling directly from curated sources at query time, making it ideal for accessing what authoritative sources say right now. One option for integrating RAG into your agent is to use an Amazon Bedrock Knowledge Base. For more information, see Retrieve data and generate AI responses with Amazon Bedrock Knowledge Bases in the Amazon Bedrock user guide.

- The key distinction lies in their complementary roles: long-term memory handles personal context and session continuity, while RAG provides current factual knowledge and domain expertise. Long-term memory answers "who is the user and what happened before," while RAG answers "what do trusted sources say currently." This separation allows agents to maintain personal relationships with users while ensuring access to accurate, authoritative information.

- By using long-memory and RAG together, your agent can deliver both personalized experiences through remembered context and reliable information through real- time knowledge retrieval. To your customers, your agents are both familiar and factually grounded.

## Get started with AgentCore Memory
There's another quick start guide here
- pip install bedrock-agentcore bedrock-agentcore-starter-toolkit
- there are a few more articles about short-term, long-term, some examples, built-in overrides, skipping those and starting back at observability

## Observability
- cloudwatch metrics
- can see memory extraction process in cloudwatch logs
- TODO: does datadog integration consider agentcore or just bedrock?

## Best practices
Encrypting your memory
Memory poisoning or prompt injection
- **Memory poisoning** represents a threat where attackers embed false information in conversations to corrupt long-term memory stores. This can manifest as context pollution, where misleading context influences future memory retrieval, or as deliberate data integrity attacks designed to degrade service quality over time.
- **Prompt injection** attacks occur when users attempt to override system prompts during memory extraction or when malicious content in conversational data manipulates LLM behavior. These attacks can also involve privilege escalation attempts to access or modify memory beyond user permissions.
- prevention techniques
  - input validation at CreateEvent API level, sanitize with guardrails prior to persistence to memory (we are looking to enforce guardrail in all API calls via VPC endpoint policy)
  - security testing
Least-privilege principle

## Amazon Bedrock AgentCore Gateway: Securely connect tools and other resources to your Gateway
Amazon Bedrock AgentCore Gateway provides an easy and secure way for developers to build, deploy, discover, and connect to tools at scale. AI agents need tools to perform real-world tasks—from querying databases to sending messages to analyzing documents. With Gateway, developers can convert APIs, Lambda functions, and existing services into Model Context Protocol (MCP)-compatible tools and make them available to agents through Gateway endpoints with just a few lines of code. Gateway supports OpenAPI, Smithy, and Lambda as input types, and is the only solution that provides both comprehensive **ingress authentication and egress authentication** in a fully-managed service. Gateway also provides 1-click integration with several popular tools such as Salesforce, Slack, Jira, Asana, and Zendesk. Gateway eliminates weeks of custom code development, infrastructure provisioning, and security implementation so developers can focus on building innovative agent applications.
- Manage both inbound authentication (verifying agent identity) and outbound authentication (connecting to tools) in a single service. Handle OAuth flows, token refresh, and secure credential storage for third-party services.
- serverless, managed, built-in observaility and auditing
- key capabilities (these are the sec/platform ones only)
- Security Guard - Manages OAuth authorization to ensure only valid users and agents can access tools and resources.
- Secure Credential Exchange - Handles credential injection for each tool, enabling agents to use tools with different authentication requirements seamlessly.
- Infrastructure Manager - Provides a serverless solution with built-in observability and auditing, eliminating infrastructure management overhead.
We will probably need to plan to include this in the PoC

## Supported gateway targets
- lambda, api gateway stages, openapi schemas, mcp servers, smithy models, integration provider templates

## Prerequisites for using the Amazon Bedrock AgentCore gateway service
- there is a [set up guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-building.html)
- we will probably need to scope this into a reusable component, does not discuss at what level this is implemented (account vs centralized), assume its local or per-workload/agent config
- can provide fine-grained access control via interceptors
- REQUEST interceptors execute before the gateway makes a call to the target, allowing you to:
  - Validate user permissions based on JWT claims or custom logic
  - Control access to specific tools or MCP operations
  - Implement role-based or attribute-based access control
  - Filter or modify requests based on user context
  - Return authorization errors for unauthorized requests
- there are levels at which these controls can be implemented
  - gateways (which users/agents can connect and auth with the gw)
  - tool-level (which tools can be used w the gateway)
  - operation-level (access to specific MCP operations like tools/list or tools/call)
  - parameter level (csan validate request parameters, and data within operations)
- implementation approaches are JWT claims validation, external authorization services, and request context filtering
- we are probably aligning to SSO sourcing from Entra for this, so suspect we need external authoriation for that unless it considers IAM Identity center something else

## Best practices
- PoLP
- use structed claims
- implement fail-safe defaults, deny by default when auth is not determined
- log authorization decisions

## Provide identity and credential management for agent applications with Amazon Bedrock AgentCore Identity
- need to skim this, I'm out of time and need to spike out this work today, we need to keep the scope as tiny as possible to get started
- have noticed multiple typos in these docs so far, these must be pretty fresh off the press
- Amazon Bedrock AgentCore Identity is an identity and credential management service designed specifically for AI agents and automated workloads. It provides secure authentication, authorization, and credential management capabilities that enable agents and tools to access AWS resources and third-party services on behalf of users while helping to maintain strict security controls and audit trails. Agent identities are implemented as workload identities with specialized attributes that enable agent-specific capabilities while helping to maintain compatibility with industry-standard workload identity patterns. The service integrates natively with Amazon Bedrock AgentCore to provide identity and credential management for agent applications, including Host agent or tools with Amazon Bedrock AgentCore Runtime and Amazon Bedrock AgentCore Gateway: Securely connect tools and other resources to your Gateway.
- centralized
- Each agent identity receives a unique ARN (such as `arn:aws:bedrock-agentcore:region:account:workload-identity/directory/default/workload-identity/agent-name`) that enables precise access control and resource management. This centralization also enables hierarchical organization and group-based access controls, making it easier to implement enterprise-wide governance policies and maintain compliance across all agent operations.
- secure credential storage
- its called token vault
- The token vault provides security for storing OAuth 2.0 tokens, OAuth client credentials, and API keys with comprehensive encryption at rest and in transit. All credentials are encrypted using either customer-managed or service-managed AWS KMS keys and access-controlled to prevent unauthorized retrieval. The vault implements strict access controls, ensuring that credentials can only be accessed by authorized agents for specific purposes and only when they present verifiable proof of workload identity.
- Agent identity and access controls, supports impersonation flow where agents can access resources using credentials provided to them
- built into sdk, add annotations to turn it on such as @requires_access_token and @requires_api_key

## Get started with AgentCore Identity
- does it rely on cognito? seems like it, but maybe that's just the getting started guide where they always use aws-native, we are going to need to have integration w/ entra

## Notes
- This thing is massive and this is just one half of the total product we will need to role out bedrock + agentcore
- Best practices implementation with all the guardrails, PoLP + access controls, integration w entra and all the other components will take time
- the requirements for security apply in lab and beyond
- to me, that forces our decision about target environment for getting started, and we will need to align with the customer about that, or they are welcome to go to security and push for exceptions but I would never sponsor that personally, way too much risk surface here without careful implementation planning for guardrails and repeatable as-code infra configs which will take time to release as a set of products w/ a user path
- what do I need to do today so we can have some expectations alignment here?
1. map security essentials to a timeline, if we take the skip-sandbox approach here how long until we can start developing? make a list of the essential implementation items
2. I like a different approach, you use a sandboxes, I have a working session with you to configure network and validate bedrock and bedrock agentcore ops, and you can start rapidly iterating with full admin role because the sandbox is off net
