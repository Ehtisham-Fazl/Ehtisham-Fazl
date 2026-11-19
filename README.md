# Ehtisham Fazal — Senior AI Engineer

A responsive personal portfolio focused on production AI, multi-agent systems, RAG, computer vision, and applied research.

## Local preview

Requires Node.js 18 or newer. No package installation or build is needed.

```powershell
cd "C:\Users\Ehtisham Fazal\Desktop\projects\Ehtisham-Fazl"
npm run dev
```

Open http://localhost:4173. Stop with Ctrl+C. Set the `PORT` environment variable to choose a different port. Refresh the browser after editing files.

You can also open `index.html` directly, although clipboard support works best on localhost or HTTPS.

## Checks

```powershell
npm run check
```

## Files

- `index.html`: page structure, biography, projects, and experience.
- `styles.css`: responsive design, typography, and conceptual project illustrations.
- `script.js`: navigation, project filters, clipboard, and original canvas visual.
- `assets/portrait.png`: portrait from the existing portfolio.
- `assets/Ehtisham-Fazal-Resume.pdf`: original four-page resume template with the Stewart description updated.
- `CONTENT-NOTES.md`: source provenance and content review notes.
- `server.mjs`: dependency-free local preview server; not required by GitHub Pages.

The page uses Google Fonts with local system fallbacks. All primary images and documents are local. No analytics, tracking scripts, or application dependencies are included. Animation pauses offscreen and when the browser tab is hidden, and respects reduced-motion preferences.

## Publish when ready

This checkout is a clone of `Ehtisham-Fazl/Ehtisham-Fazl`, which is also the special GitHub profile README repository. Publishing a website here will not automatically replace the separate `ehtisham-fazal.github.io` website.

1. Review the portfolio and `CONTENT-NOTES.md` locally.
2. Commit and push the changes yourself when satisfied.
3. In this repository on GitHub, open **Settings → Pages**.
4. Set **Source** to **Deploy from a branch**, choose the branch containing these files, choose **/(root)**, and save.
5. Use the published URL shown by GitHub Pages. For this repository it is normally `https://ehtisham-fazl.github.io/Ehtisham-Fazl/`.

To replace the existing `https://ehtisham-fazal.github.io/` site, these files must instead be pushed to that site's source repository under the `ehtisham-fazal` account. All site asset URLs are relative to support both a repository subpath and a root domain.

No changes have been pushed or published by the agent.

## Original profile template

<!--
**Ehtisham-Fazl/Ehtisham-Fazl** is a ✨ _special_ ✨ repository because its `README.md` (this file) appears on your GitHub profile.

Here are some ideas to get you started:

- 🔭 I’m currently working on ...
- 🌱 I’m currently learning ...
- 👯 I’m looking to collaborate on ...
- 🤔 I’m looking for help with ...
- 💬 Ask me about ...
- 📫 How to reach me: ...
- 😄 Pronouns: ...
- ⚡ Fun fact: ...
-->

## Resume maintenance

The website links to `assets/Ehtisham-Fazal-Resume.pdf`. The original LinkedIn export is retained at its original path for reference. A text reference is in `resume/Ehtisham-Fazal-Resume.md`.

The generator is `resume/build_resume.py`; it requires Python with pypdf. It edits only the Stewart description in the original `assets/Ehtisham-Fazal-Profile.pdf`, retaining the four-page layout, embedded font, original text coordinates, and all other content. It writes directly to `assets/Ehtisham-Fazal-Resume.pdf` and checks that other content remains unchanged. Editing the Markdown alone does not regenerate the PDF. Do not redesign or reflow the resume template.

The website and updated resume use the confirmed GitHub profile: https://github.com/Ehtisham-Fazl.

## Published writing

The Writing section in index.html features four verified Medium articles and links to the author profile. Update article URLs, titles, dates, and descriptions there when featuring new work. It is a curated list rather than an automatically synchronized feed.
