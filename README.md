# SWC JAWS (Southwestern College Wellness & Aquatics Complex) — unofficial preview

A mock-up of [swcjaws.com's Aquatics pages](https://swcjaws.com/aquatics/) (Aquatics, Swimming Lessons, Aquatics FAQ, Contact) with
JAWS's Fast Pool, Flex Pool and Teaching Pool on one live [Pool Relay](https://www.poolrelay.com) schedule. Not operated by or affiliated
with Southwestern College.

No schedule is typed into the pages, except the site's own three conflicting sets of pool hours, quoted and labeled in "What this
replaces". Lap swim hours and closures are filled by `finder.js` from the live Pool Relay view; `build.py` holds only rates, policies and
facts about the water.

- `build.py`: generates the four pages.
- `finder.js`: `#today`, `#week`, and `data-live` elements (`hours`, `exceptions`, `closures`).
- Pool Relay view: `JSJFJ9CDLOoPHTfA7ElM0N` (SWC JAWS, lane by lane).
