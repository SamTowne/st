## Machine Learning Engineering

### Objective
Understand machine learning to help with these types of things.
  - communicate and diagram the architecture and foundational components needed to implement a use case
  - influence ML engineering cost control, staying on budget and reducing financial risk
  - provide training cost estimates, given a dataset and ML infrastructure
  - build and continuously deploy a ML application in AWS

### Apache Airflow
- find some public, mature apache airflow usage with CICD that enables the promotion of DAGs from lower to higher envs https://github.com/jghoman/awesome-apache-airflow
- try and find out if people are shceduling to shut down environments after hours, and if any of those using the aws automation for off hours shutdown are also using terraform for iac

#### Hands on projects to consider
- https://towardsdatascience.com/a-weekend-ai-project-running-speech-recognition-and-a-llama-2-gpt-on-a-raspberry-pi-5298d6edf812

#### Stas00 online book
Practical strategy for large scale ML engineering.
- stopped at IO

#### Machine Learning Engineering in Action - Ben Wilson
- 2.4 The Foundation of ML engineering
- the MLOps paradigm and the similarities between it, DevOps, and agile development
- the data science flavor of devops is MLOps
- MLOps engages a lot of stuff to help avoid "failed, cancelled and non-adopted solutions"
  - Monitoring -> prediction accuracy, retraining performance, impact assessment, fallback/failure rate, logging
  - Release -> versioning + registration, change managenment, approvals, auditing, A/B testing + statistical evaluation, bandit algorithms
    - there is this concept of Data Version Control, DVC, which is basically git for data sets, https://towardsdatascience.com/introduction-to-data-version-control-59fabf447a60
  - CI/CD -> build tools for continuous integration, deployment tools for continuous deployment
  - Code development practices -> source code management, branching strategies, feature merging, parameter and metrics tracking, project experimentation and tuning tracking
  - Code review practices -> peer review, unit test coverage, metrics validation
  - Environment configuration -> Dev, QA, Prod, infrastructure management, platform management, dependency library management
  - Artifact management -> Artifact repositories, registration, QA simulation tests, UAT
  - Software engineering standards and Agile methods
- "ML engineering brings the core functional capabilities of a data scientist, a data engineer, and a software engineer into a hybrid role that supports the creation of ML solutions focused on solving a problem through the rigors of professional software development."
- "Delivering the simplest possible solution helps reduce development, computational, and operational costs for any given project."
- "Borrowing and adapting Agile fundamentals to ML project work helps shorten the development life cycle, forces development architectures that are easier to modify, and enforces testability of complex applications to reduce maintenance burdens."
- "Just as DevOps augments software engineering work, MLOps augments ML engineering work. While many of the core concepts remain the same for these paradigms, additional aspects of managing model artifacts and performing continuous testing of new versions introduce nuanced complexities."
- 3.0 Before you model: Planning and scoping a project
- find the simplest solution, early
- aren't project planning and agile at odds?
  - "A project plan is important, but it must not be too rigid to accomodate changes in technology or the environment, stakeholders' priorities, and people's understanding of the problem and its solution." - Scott Ambler, agile manifesto essay
  - "Planning is good in ML. It's just critical to not set those plans in stone."
- Tells a story of a data science team who has had multiple successesful projects at their company
  - However, all of their previous projects were able to be completed in isolation, for the most part, from the rest of the business
  - For the latest project, executives want them to add purchase recommendations to the company website
  - The team begins their work, as usual, studiously working in isolation and making assumptions that the executives are envisioning something siilar to the website recommendations which competition has implemented
  - They test dozens of implementations, consume hundreds of papers, and build out an MVP "using alternating least squares ALS that achieces a root mean squared error RMSE of 0.2334 along with a rough implementation of ordered scoring for relevance based on prior behavior."
  - The team is stoked as they head to meet with the business sponsors about the MVP
  - The response from the business is not great
  - They ask lots of questions and do not seem to understand the functionality of the solution
  - Attempts to make the solution more clear to the sponsors cause even more confusion and ambiguity about the solution
  - The team did not properly plan for the nuances of the project, and the MVP was received negatively due to this gap
  - They probably needed additional input from company sponsors, such as marketing, to frame the problem better during planning
  - The recommendations the solution made were not quite nuanced enough to impact customer decisions in a logical way
  - The DS team needed external input about the product being sold and typical customer behavior before getting too deep into the technical implementation
  - Don't blindly trust your metrics
  - Supplement the model-scoring metrics with other, subjective, means of understanding model efficacy
  - Sometimes just drawing a diagram of the solution, and the user experience of the solution, can bring improvement options into view
  - The data science team from the story would have done much better had they asked some of the marketing team to provide visualizations of what the new customer experience might look like with the new feature
  - A business analyst reviewed the proposed solution and found multiple problems "the nuances of the problem"
    - there was duplicated item data due to older product IDs
    - different divisions used different product IDs and this was not being accounted for
- 3.1.1 Basic planning for a project
- that first meeting
- there is a tendency to begin thinking about the "how" of a project in the first meeting
- avoid doing this, instead, listen carefully and take notes, really try to understand the current need with a 'teach me how you do it now please' approach
- 3.1.3 Plat for demos - lots of demos
- try and demo each feature as they are available if possible
  - for an MVP with 4 features, here would be a good demo strategy -> model testing , demo, feature 1 , demo, feature 2, demo, feature 3 demo, feature 4, full MVP demo
  - you don't want to build the entire MVP and then demo to stakeholders, what if something was missed? but this too is based upon MVP complexity, if it's simple it may make sense to whip it out and then demo
  - "without frequent demos as features are built out, the team at large is simply operating in the dark with respect to the ML aspect of the project. The ML team, meanwhile, is missing out on valuable time-saving feedback from SME members..."
  - keep individual feature demos lightweight! a slide deck to get the point across for each feature is BETTER than building a microservice or frontend that takes quadruple the time/effort and slows the project timeline... save that time for the bigger demos as multiple features come together
- 3.1.4 Experimentation by solution building: Wasting time for pride's sake
- avoid solution-building during experimentation such as software bake-offs where the team splits up into groups to explore each solution, this hackathon-like approach is not good for ml engineering
- concept of multiple-MVP development vs. experimentation culling development
- instead, leverage prototype experimentation enables the team to find an MVP to continue pursuing together, instead of wasting effort building 3 MVPs, then continuing with the winner
- experimentation culling is to consider the MVP options, and do low-cost prototypes as a team to decide which one to turn into the actual MVP for the project
- experimentation is important for ML projects, but "must be time-boxed"
- 3.2 Experimental scoping: Setting expectations and boundaries
- "Through setting these expectations and providing boundaries on each of them (for both time and level of implementation complexity), the ML team can provide the one thing that the business is seeking: an expected delivery date and a judgement call on what is or isn't feasible."
- 3.2.1 What is experimental scoping?
- After requirements gathering, it is absolutely essential to set an expectation with the larger team on how long the DS team will spend on vetting each of the ideas during research and experimentation.
- Having a target date helps bring focus.
- Having a date for something that is wholly unknowable (the best solution) may seem counterintuitive, but it forces simplicifty and focused thought around finding options within a time box
- The time box on the initial experimentation naturally forces teams to postpone evaluation of things that are "interesting" but not essential, jot them down somewhere, parking lot them, and reevaluate them down the road
- For complex stuff, it may require 2 weeks just for research followed by another 2 weeks for hacking
- the sole purpose of these exercises is to decide on a path, and to make that decision in the shortest time possible against the timeline of delivery for the MVP
- the amount of time required depends on the complexity of the business need, and as a team gets more comfortable with the business and each other, it becomes easier to provide a timeline to the business for the "experiment/hacking" phase
