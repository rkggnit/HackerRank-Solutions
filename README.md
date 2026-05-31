# HackerRank-Solutions

## 🔄 Maintenance: How to Renew the Session Cookie
HackerRank session cookies expire periodically. If the GitHub Action fails with an "Authorization failed" error, follow these steps to update the secret:

1. **Get the New Cookie:**
   * Log into [HackerRank](https://www.hackerrank.com).
   * Open Developer Tools (`F12` or `Right-Click -> Inspect`) and go to the **Network** tab.
   * Refresh the page and click on the first request (usually `dashboard` or `practice`).
   * Scroll down to **Request Headers**, find `cookie:`, and copy the **entire raw string** next to it.

2. **Update GitHub:**
   * Go to this repository's **Settings** > **Secrets and variables** > **Actions**.
   * Find the `HRANK_SESSION` secret and click the **Pencil icon** to edit.
   * Paste the new cookie string and click **Update secret**.

3. **Verify:**
   * Go to the **Actions** tab, select the **HackerRank Sync** workflow, and click **Run workflow** to test it.
