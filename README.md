# sunpy-vcr-cassettes
Storage repository for sunpy remote test cassettes

## Workflow
All the cassettes are updated on a weekly basis by a GitHub Actions CRON job
which:
1. Clones the main sunpy repository
2. Runs all the tests marked with `vcr` to regenerate all the cassettes
3. If there are any additions or changes to the responses, the modified
   responses are automatically pushed to this repository.
