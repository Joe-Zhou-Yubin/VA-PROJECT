# Mongabay: "The Ocean's Enforcement Gap" (March 2026)

**Source:** https://news.mongabay.com/2026/03/the-oceans-enforcement-gap/
**Published:** March 2026
**Type:** Environmental journalism feature article

## Summary

Governments have designated vast marine protected areas and pledged to conserve 30% of the ocean by 2030, but enforcement lags far behind commitments. The article argues that the problem is not a shortage of rules but the unevenness of enforcement.

## Key Points

### The designation vs. enforcement gap
- Creating MPAs is politically attractive (signals ambition, low cost)
- Policing them is harder: patrol vessels expensive, legal cases drag on, agencies underfunded
- A 2014 Nature paper shows ecological benefits depend more on whether rules are monitored than on MPA size

### Technology is changing the economics of monitoring
- **AIS transponders** provide continuous vessel tracking
- **Satellite imagery** detects ships that switch AIS off ("dark vessels")
- **Machine learning** identifies likely fishing behavior from speed/course patterns
- Result: authorities no longer scan vast ocean areas blindly — they can target specific vessels and coordinates

### Case studies
- **Indonesia (mid-2010s):** Combined satellite tracking with publicized crackdowns. Seized boats were dramatically scuttled. Illegal fishing declined in several regions.
- **Palau:** Small Pacific nation, vast EEZ, no budget for at-sea patrols. Partnered with NGOs and tech providers for remote satellite monitoring. Inspections happen at port instead.

### Ports as enforcement chokepoints
- **Port State Measures Agreement:** Countries can deny entry to suspected IUU vessels
- Shifts burden from chasing ships at sea to controlling infrastructure on land
- Cities like Vigo (Spain), Busan (South Korea) — inspections tied to catch documentation

### Transparency as enforcement tool
- Platforms that publish vessel tracks (i.e., Global Fishing Watch) allow journalists, researchers, and civil society to scrutinize activity independently
- Makes enforcement a response to documented facts rather than political will alone

## Key Insight

> "AIS signals can be spoofed, satellites may miss small wooden boats, and data analysis requires trained personnel. Enforcement remains a human enterprise, not merely a digital one."

## Relevance to Our Project

**Frames the entire motivation for our dashboard:** We are building exactly the kind of tool this article describes — using AIS data, satellite-derived patterns, and behavioral indicators to narrow the enforcement gap.

**Connects to our Disabling Map:** The article explicitly discusses AIS disabling and dark vessels as a key challenge. Our Sheet 11 (Disabling Map Enriched) visualizes precisely this.

**Port State Measures → our Anchorages data:** The article's point about ports as chokepoints connects to our `anchorages_cleaned.csv` and the concept of flagging ports frequented by high-risk vessels.

**Good for the Introduction section of the report:** Sets the stage for why visual analytics of fishing data matters for ocean governance.
