go read `Get Started.md` for the sincera api documentation

my api key is in the repo secrets as `SINCERA_API_KEY`

aws role to assume is in the repo secrets as `AWS_ROLE_TO_ASSUME`

Never expose these keys via a commit even if you know them.

To run the workflow that fetches new sellers lists and ecosystem data,
edit `trigger_data_pull.txt`, update the value after `last_pull =` to a
new date or version, commit the change to `main`, and push it. Each
increment triggers the GitHub Action.
