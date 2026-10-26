# Swish Tracker (installable, works offline)

Static app / PWA. iPhone camera needs HTTPS, so host these files ONCE on any free
HTTPS host (no computer needed afterwards):

## One-time hosting from the phone (GitHub Pages)
1. In Safari, sign in at github.com, create a new public repository.
2. Add file > Upload files, upload everything in this folder, commit.
3. Settings > Pages > Deploy from branch `main` / root. Open the https://<you>.github.io/<repo>/ URL.
(Netlify Drop or Cloudflare Pages work too if you have a computer handy.)

## Install on iPhone
1. Open the HTTPS URL in Safari, tap Start Camera once while online
   (this downloads and caches the AI model).
2. Share > Add to Home Screen.
3. From then on it launches like an app and works offline, no computer, no server.

Data is stored locally in the app (localStorage). Local testing: `python3 serve.py`.
Detection is a prototype; correct suggestions with the manual buttons.
