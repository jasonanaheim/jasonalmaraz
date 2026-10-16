# Jason Almaraz portfolio

Live site: https://jasonalmaraz.com

## Development and publishing

1. Start a short-lived branch from the latest `main`, named `codex/description` or `feature/description`.
2. Edit the website in `public/`.
3. Run `python3 scripts/check_site.py`. Preview locally with `python3 -m http.server 8000 --directory public`.
4. Push the branch and open a pull request into `main`.
5. Review the GitHub `Validate site` check and Netlify Deploy Preview.
6. Squash merge the reviewed PR. Netlify validates and publishes `main` automatically.

Do not push routine changes directly to `main`. No separate long-lived development branch is needed.

GitHub Actions checks local links, anchors, basic HTML structure, duplicate IDs, and image alt attributes. External URLs and visual layout still need manual review. Netlify runs the same validator before publishing, so invalid site output cannot replace production.

## Branch protection limitation

GitHub currently rejects branch-protection configuration for this private repository on the account's plan. The PR workflow is therefore a convention, not an enforced restriction. After upgrading to a supporting plan, protect `main`: require a pull request, require `Validate site` and the Netlify preview check, require resolved conversations, and block force pushes and deletion. Keep approvals optional for a solo-maintained portfolio.

## Rollback

Revert the problematic merge in GitHub and merge the revert PR. For urgent recovery, publish a previous successful deploy in Netlify, then revert the source change so the next deployment preserves the fix.

Netlify uses its existing GitHub integration; no deployment tokens are stored in GitHub Actions.
