# TMT Combined IUU Fishing Vessel List

**Source:** https://iuu-vessels.org/
**Type:** Structured database (searchable, downloadable as Excel)
**Maintained by:** Trygg Mat Tracking (TMT), Norwegian non-profit

## What It Is

The Combined IUU Fishing Vessel List merges blacklists from 13 Regional Fisheries Management Organisations (RFMOs) into one reference point. It covers vessels that are **currently listed** and those **historically delisted** (name changes, ownership changes, decommissioned).

## Contributing RFMOs

- CCAMLR (Antarctic)
- CCSBT (Southern Bluefin Tuna)
- GFCM (Mediterranean)
- IATTC (Inter-American Tropical Tuna)
- ICCAT (Atlantic Tunas)
- IOTC (Indian Ocean Tuna)
- NAFO (Northwest Atlantic)
- NEAFC (Northeast Atlantic)
- NPFC (North Pacific)
- SEAFO (Southeast Atlantic)
- SPRFMO (South Pacific)
- SIOFA (Southern Indian Ocean)
- WCPFC (Western/Central Pacific)

## Key Features

- Updated continuously (unlike individual RFMO lists which may update annually)
- Tracks identity changes: name, flag, callsign, IMO, owner, operator
- Includes last known AIS position for tracked vessels
- Downloadable in Excel format
- Historical record of all IUU-listed vessels retained

## Relevance to Our Project

**Join key:** Match vessels in our `iuu_risk_cleaned.csv` by IMO number or MMSI to identify which vessels in our behavioral dataset are also formally blacklisted by RFMOs. This closes the loop between *behavioral* risk indicators (AIS gaps, encounters) and *official* enforcement outcomes.

**Dashboard use:** Add a "Formally IUU-Listed" badge to the Vessel Profile sheet. Highlight TMT-listed vessels on the AIS Disabling Map with a distinct marker.

**Note:** INTERPOL Purple Notices were previously included but are no longer public, so they're excluded from the current site.
