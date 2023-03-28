## Splunk

### Filters
- index=aws | filters out non-aws logs, depends on the splunk configuration but is pretty common to use multiple indexes to split data by source environment
- eventSource="lambda.amazonaws.com" | filter to events origininating from a specific AWS service
- eventName | the API action being invoked in the event
- errorCode=* | wildcard search for any errors

### Example queries
1. find non_compliant config rules
  - index=aws eventSource="config.amazonaws.com" eventName=PutEvaluations "requestParameters.evaluations{}.complianceType"=NON_COMPLIANT
  - to filter by account add: recipientAccountId=123456789123
2. find errors with IAM User Roles assumed by a user id
  - index=aws errorCode=* repientAccount=123456789123 "userIdentity.arn"="arn:aws:sts::123456789123:assumed-role/role_name_here/user_id_here"
3. service role events
  - index=aws "userIdentity.arn"="arn:aws:sts::123456789123:assumed-role/role_name_here"
  - use eventName to search for event type: eventName=StartQueryExecution
  - arn supports wildcards
4. getting Athena Query by execution ID (sts assumed role in use)
  - index=aws "userIdentity.arn"="arn:aws:sts::123456789123:assumed-role/role_name_here/user_id_here" eventName=StartQueryExecution queryExecutionId=eus8s8k-aghfiah-safhsadfb-aksdf
5. to get a quicksight dashboard ID
  - index=aws "userIdentity.arn"="arn:aws:sts::123456789123:assumed-role/role_name_here/user_id_here" eventName=CreateDashboard

## Mac tools
- install xcode
  - in terminal, do a `git status` to get a prompt to install it
- install homebrew (requires xcode)
  - `brew upgrade` for latest
  - `brew analytics off` to keep from sending usage data
  - add brew cellar to zsh (so that tools installed via homebrew can be accessed without fully qualifying the path to the binaries)
    - `echo 'export PATH=/usr/local/cellar:$PATH' >>~/.zshrc`
- use homebrew to install the cool kid stuff
    ```
    brew install go
    brew install python3
    brew install awscli
    brew install font-fira-code
    brew install git-lfs
    brew install pyenv
    brew install tfenf
    brew install gpg
    brew install gpg2
    brew install keychain
    brew install pinentry-mac
    ```

## Terraform
- injecting terraform-docs to a readme manually
  - `terraform-docs markdown table --output-file README.md --output-mode inject /path/to/terraform_code`
- conditionally creating resources using count + contains
  - `count = contains(["dev","preprod"], var.environment) ? 1 : 0`
  - creates the resource if the var.environment var contains the dev or preprod
  - allows you to build things in lower environments to test before moving them towards prod
- using dummy archive files for initial lambda source code when code deploy is in use
  ```terraform
  data "archive_file" "dummy_source" {
    output_path = "${path.module}/dist.zip"
    type        = "zip
    source {
      content  = "dummy  text"
      filename = "dummy.txt"
    }
  }
  ```
- pre-commit-terraform
  - https://github.com/antonbabenko/pre-commit-terraform
  - config .pre-commit-config.yaml
    ```yaml
      repos:
        - repo: https://github.com/antonbabenko/pre-commit-terraform
          rev: v1.68.0
          hooks:
            - id: terraform_fmt
              args:
                - --args=-recursive
            - id: terraform_docs
            - id: terraform_tflint
            - id: terraform_validate
        - repo: https://github.com/pre-commit/mirrors-prettier
          rev: "v2.6.2"
          hooks:
            - id: prettier
              types_or: [markdown]
        - repo: https://github.com/pre-commit/pre-commit-hooks
          rev: v2.3.0
          hooks:
            - id: check-yaml
            - id: end-of-file-fixer
            - id: trailing-whitespace
    ```

## Git
- commitizen is nice https://github.com/commitizen/cz-cli for commit formatting
- Commit Squashing when there's a lot of commits
  - `git rebase -i HEAD~35`
  - The number (35 above) should be adjusted to capture the amount of commits to include in the squash
  - Then, with vi, you can replace all the picks with s (for squash): `:%s/pick/s/g`
  - Then, just manually add p (for pick) for the commits that should stay
- rebasing example with a trunk branch called main and dev branch called dev_branch
  - `git checkout main`
  - `git pull`
  - `git checkout dev_branch`
  - `git rebase main`
  - `git push --force-with-lease` (only do this if you are the only one working on this remote/dev branch)
- unless otherwise specified, it's a nice idea to start development work by creating an issue on the remote repository side. Then, off that issue, create the branch and merge request. This allows the work to be tracked from the beginning.
- deleting local branches except specified ones
  - `git branch | grep -v "dev_branch" | grep -v "main" | xargs git branch -D`
  - deletes all branches except dev_branch and main
- find diff for specific services in a monorepo
  - `git diff --name-status SHA^ SHA | sort -u | awk 'begin {fs="services/"} {print $2}'`

## VSCode
- search all opened files and directories: ctrl+shift+f (this can be tuned using regex and/or omitting/including directories)
- regex to select every N line `(.*\n){N}` and there's a stackoverflow thread about this with additional context and tips
- regex to highlight occurrences of multiple individual words: `word1|word2|word3` , then press alt+enter to select all
- ctrl+shift+L to highlight all occurents of current selection
- ctrl+shift+alt+UP ARROW to make cursor go vertical (use option instead of alt for mac keyboard)
- ctrl+shift+~ to get a terminal
- hold alt (option for mac) and click to add more cursors, esc to get to normal state
