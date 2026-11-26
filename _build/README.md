# Build notes

The site is plain static HTML/CSS; GitHub Pages serves the files as they are, with no build step.
`build.py` regenerates the three pages, `sitemap.xml`, `robots.txt` and `llms.txt` from `data.json`,
which holds the course data copied from the NSMG Member Portal components (certData.js, fellowshipData.js).

    NSMG_CONTACT_EMAIL='address shown on the site' python3 _build/build.py

The contact email is read from the environment so it is never stored in the script.
