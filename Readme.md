# Top Contributors to the DCPPC

This script uses the Github API to iterate through all repos in the DCPPC organization and count contributions (opening an issue or a pull request) by user.

This requires an API key for an account that can access both public and private repositories in the DCPPC. (We used one of our own, as Florence Python runs Centillion and our Github authorization protection layers, and we don't want to bork those.)

Create an API access token in the Settings page on Github, and pass that into the script with the environment variable `GITHUB_TOKEN`:

```
$ GITHUB_TOKEN="AAAAAAAAAAAA" python top_contributors.py
```

This will create a new timestamped directory named `output_YYYYMMDD_HHMMDD` that will contain the following files:

Logs:

* `log_top25.log` - Output log file
* `repos.txt` - list of repos that were indexed/counted

Contributions:

* `dcppc_all_contributors.csv` - sorted CSV list of all contributors to all DCPPC repos
* `dcppc_top25_contributors.csv` - sorted CSV list of top 25 contributors to all DCPPC repos

Breakdown:

* `dcppc_issues_contributors.csv` - sorted CSV list of top issues contributors to all DCPPC repos
* `dcppc_pulls_contributors.csv` - sorted CSV list of top pull request contributors to all DCPPC repos
