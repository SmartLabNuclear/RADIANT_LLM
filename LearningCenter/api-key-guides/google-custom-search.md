> **Note:** Google's console UI reorganizes periodically, and the exact current screens weren't independently re-verified by browsing them live for this guide. The overall two-part structure (a Programmable Search Engine, plus a separate API key) is stable and well-documented by Google. If you're a new user, read the "Is this even worth doing?" section below before spending time on this.

# Getting a Google Custom Search API Key (legacy, optional)

RADIANT-LLM's live web search runs on [Tavily](tavily.md) by default. This key is an **optional legacy alternative** if you already have Google Custom Search access. Most users don't need this at all.

## Is this even worth doing, as a new user?

Probably not. Google closed the Custom Search JSON API to new customers in 2025, and will shut it down entirely for everyone on January 1, 2027 ([official deprecation notice](https://developers.google.com/custom-search/custom-search-api-list)). If you don't already have an existing Google Cloud project with this API enabled, you likely cannot sign up for it fresh today. If that's you, skip this guide entirely and leave `CUSTOM_SEARCH_ENGINE_API_KEY` / `CUSTOM_SEARCH_ENGINE_ID` blank in `.env`, RADIANT-LLM works fine without them.

This guide is here for the smaller group of users who already have access from before the 2025 cutoff.

## Steps (if you already have API access)

1. Create a Programmable Search Engine at the [Control Panel](https://programmablesearchengine.google.com/controlpanel/create). Configure it to search the entire web (rather than specific sites), unless you have a reason to scope it narrower.

   `[PLACEHOLDER: screenshot — Programmable Search Engine creation]`

2. Once created, open its **Overview** page and find the **Search Engine ID** in the Basic section. Copy it.

   `[PLACEHOLDER: screenshot — Search Engine ID location]`

3. Separately, get an API key from the [Google Cloud Console credentials page](https://console.cloud.google.com/apis/credentials), under whichever Google Cloud project already has the Custom Search API enabled.

   `[PLACEHOLDER: screenshot — Cloud Console API key]`

4. Paste both into your `.env` file:

   ```
   CUSTOM_SEARCH_ENGINE_API_KEY=...
   CUSTOM_SEARCH_ENGINE_ID=...
   ```

## Things to know

- This is two separate credentials from two different Google consoles (Programmable Search Engine control panel, and Cloud Console), not one combined signup, easy to get only half of it and wonder why it doesn't work.
- Even with existing access, the JSON API is billed at roughly $5 per 1,000 queries beyond any free quota, unlike Tavily.
- See the [Tavily guide](tavily.md) for the actual recommended path, this one is a legacy alternative only.
