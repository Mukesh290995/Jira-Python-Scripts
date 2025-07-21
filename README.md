Jira expresionn

(
  issue.issueType.name == "USE Framework" ||
  (
    (issue.issueType.name == "Story" || issue.issueType.name == "Improvement") &&
    issue.customfield_XXXXX == "Y"
  )
)
? issue.customfield_YYYYY != null
: true
