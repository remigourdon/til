# Netlify Deployment via GitHub Action

## Initialize Netlify site for manual deployment

In order to initialize a new Netlify site to use for [manual deployment using their CLI tool](https://docs.netlify.com/cli/get-started/#manual-deploys), do the following:

```sh
npm install netlify-cli -g
netlify login
netlify deploy --dir site/
```

The tool will then prompt you to create and configure the new site and it will store that configuration in `.netlify/state.json`, as well as append that file to `.gitignore` automatically.

## Deploy from GitHub Action

Create 2 secrets in the GitHub repository settings:

+ `NETLIFY_SITE_ID`: found on the Netlify under `Site settings -> Site details -> Site information -> Site ID`
+ `NETLIFY_AUTH_TOKEN`: personal access token created on Netlify, as explained [on this page](https://docs.netlify.com/cli/get-started/#obtain-a-token-in-the-netlify-ui)

```yaml
name: Publish with Netlify

on:
  push:
    branches:
      - main

env:
  NETLIFY_CLI_VERSION: "^12.2.1"

jobs:
  publish:
    runs-on: ubuntu-22.04
    steps:
      - name: Get npm cache directory
        id: npm-cache-dir
        run: |
          echo "dir=$(npm config get cache)" >> $GITHUB_OUTPUT
      - uses: actions/cache@v3
        id: npm-cache # use this to check for `cache-hit` ==> if: steps.npm-cache.outputs.cache-hit != 'true'
        with:
          path: ${{ steps.npm-cache-dir.outputs.dir }}
          key: ${{ env.NETLIFY_CLI_VERSION }}
          restore-keys: |
            ${{ runner.os }}-node-
      - name: Install Netlify CLI
        run: npm install -g "netlify-cli@${NETLIFY_CLI_VERSION}"
      - name: Publish to Netlify
        run: netlify deploy --dir site --prod
        env:
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
```