# badnest

Updated (completely rethought) fork of [badnest](https://github.com/USA-RedDragon/badnest).
A Nest integration that uses the Nest Web API (after Works with Nest was shut down).

## Features

- Doesn't use the now defunct Works with Nest API
- Works with migrated/new accounts via Google auth
- Nest Protect support
- Nest Thermostat support
- Nest Camera support

## Configuration

### Example configuration.yaml

```yaml
badnest:
  issue_token: "https://accounts.google.com/o/oauth2/iframerpc....."
  cookie: "OCAK=......"

binary_sensor:
  - platform: badnest

climate:
  - platform: badnest
    scan_interval: 10

camera:
  - platform: badnest

sensor:
  - platform: badnest

switch:
  - platform: badnest
```

The values of `"issue_token"` and `"cookie"` are specific to your Google Account. To get them, follow these steps (only needs to be done once, as long as you stay logged into your Google Account).

1. Open a Chrome browser tab in Incognito Mode (or clear your cache).
2. Open Developer Tools (View/Developer/Developer Tools).
3. Click on 'Network' tab. Make sure 'Preserve Log' is checked.
4. In the 'Filter' box, enter `issueToken`
5. Go to `home.nest.com`, and click 'Sign in with Google'. Log into your account.
6. One network call (beginning with `iframerpc`) will appear in the Dev Tools window. Click on it.
7. In the Headers tab, under General, copy the entire `Request URL` (beginning with `https://accounts.google.com`, ending with `nest.com`). This is your `"issue_token"` in `configuration.yaml`.
8. In the 'Filter' box, enter `oauth2/iframe`
9. Several network calls will appear in the Dev Tools window. Click on the last `iframe` call.
10. In the Headers tab, under Request Headers, copy the entire `cookie` (beginning `OCAK=...` - **include the whole string which is several lines long and has many field/value pairs** - do not include the `cookie:` name). This is your `"cookie"` in `configuration.yaml`.
