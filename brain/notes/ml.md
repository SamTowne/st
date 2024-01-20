## Machine Learning Engineering

### Objective
Understand machine learning to help with these types of things.
  - communicate and diagram the architecture and foundational components needed to implement a use case
  - influence ML engineering cost control, staying on budget and reducing financial risk
  - provide training cost estimates, given a dataset and ML infrastructure
  - build and continuously deploy a ML application in AWS

#### Hands on projects to consider
- https://towardsdatascience.com/a-weekend-ai-project-running-speech-recognition-and-a-llama-2-gpt-on-a-raspberry-pi-5298d6edf812

#### Stas00 online book
Practical strategy for large scale ML engineering.
- stopped at IO

#### Machine Learning Engineering in Action - Ben Wilson
- 2.4 The Foundation of ML engineering
- the MLOps paradigm and the similarities between it, DevOps, and agile development
- the data science flavor of devops is MLOps
- MLOps engages a lot of stuff to help avoid failed, cancelled and non-adopted solutions
  - Monitoring -> prediction accuracy, retraining performance, impact assessment, fallback/failure rate, logging
  - Release -> versioning + registration, change managenment, approvals, auditing, A/B testing + statistical evaluation, bandit algorithms
    - there is this concept of Data Version Control, DVC, which is basically git for data sets, https://towardsdatascience.com/introduction-to-data-version-control-59fabf447a60
  - CI/CD -> build tools for continuous integration, deployment tools for continuous deployment
  - Code development practices -> source code management, branching strategies, feature merging, parameter and metrics tracking, project experimentation and tuning tracking
  - Code review practices -> peer review, unit test coverage, metrics validation
  - Environment configuration -> Dev, QA, Prod, infrastructure management, platform management, dependency library management