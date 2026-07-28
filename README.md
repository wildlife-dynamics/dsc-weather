# DSC Weather — User Guide

This guide walks you through configuring and running the DSC Weather workflow, which ingests weather station observations from EarthRanger, tags each station with the conservancy boundary it falls within, and exports analysis-ready station metadata and per-station, per-year weather reading files.

---

## Overview

Unlike a per-survey pipeline, this workflow performs a single, station-centric ingestion pass each run — it isn't scoped to any survey or activity period. Each run produces:

- A **station metadata file** — one row per weather station, with its conservancy and coordinates
- **Per-station, per-year weather reading files** — precipitation, temperature, humidity, and wind speed observations

Both outputs are also rendered as browsable **table widgets** on the workflow run's dashboard, so reviewers can inspect the data without downloading the files.

---

## Prerequisites

Before running the workflow, ensure you have:

- An **EarthRanger connection with a weather station subject group** (e.g. a `TAHMO Stations` group) whose subjects log periodic observations carrying `precipitation`, `surface_air_temperature`, `relative_humidity`, and `wind_speed` fields
- Weather station subjects with valid point locations — a station is dropped from the output if it doesn't spatially fall within any conservancy boundary in the reference conservancies file used by the workflow

---

## Step-by-Step Configuration

### Step 1 — Add the Workflow Template

In Ecoscope, go to **Workflow Templates** and click **Add Workflow Template**. Paste the GitHub repository URL into the **Github Link** field:

```
https://github.com/wildlife-dynamics/dsc-weather.git
```

Then click **Add Template**. The card may show **Initializing…** briefly while the environment is set up.

---

### Step 2 — Select the Workflow

After the template is added it appears in the **Workflow Templates** list as **dsc_weather**. Click the card to open the workflow configuration form.

---

### Step 3 — Set Workflow Details and Time Range

The configuration form opens with two sections at the top.

**Set Workflow Details**

| Field | Description |
|-------|-------------|
| Workflow Name | A short name to identify this run (required) |
| Workflow Description | Optional notes, e.g. the year or region covered |

**Time Range**

This field is required on all Ecoscope workflows. It controls which weather observations are fetched: observations on or after **Since** and up to **Until** are retrieved from EarthRanger, and it is also used for timestamp display and UTC conversion.

| Field | Description |
|-------|-------------|
| Timezone | Local timezone for display and UTC conversion, e.g. `Africa/Nairobi (UTC+03:00)` |
| Since | Start of the data fetch window |
| Until | End of the data fetch window |

---

### Step 4 — Configure Weather Station Connection

| Field | Description |
|-------|-------------|
| Data Source | The EarthRanger connection that hosts the weather station subject group |
| Weather Station Subject Group | EarthRanger subject group name containing the weather stations, e.g. `TAHMO Stations` (defaults to `TAHMO Stations`) |

---

## Running the Workflow

Once all parameters are configured, click **Submit**. The workflow will:

1. Fetch observations from the configured weather station subject group over the Time Range.
2. Extract precipitation, temperature, humidity, and wind speed from each reading.
3. Download and load the reference conservancy boundaries, and tag each weather station with the conservancy it falls within — stations outside every boundary are dropped.
4. Rename station identity columns and extract station latitude/longitude from the point geometry.
5. Split each reading's timestamp into date, time, and year components.
6. Select and deduplicate station identity columns to one row per station, and export the **station metadata** file.
7. Select the weather reading columns and split them by station and calendar year, exporting one **weather readings** file per station per year.
8. Render both outputs as table widgets and attach them to the run's dashboard.

---

## Output Files

All outputs are written to `$ECOSCOPE_WORKFLOWS_RESULTS/`.

| File | Description |
|------|-------------|
| `station_metadata.parquet` | One row per weather station: `Station ID`, `Conservancy`, `Latitude`, `Longitude` |
| `{station_id}_{year}.parquet` | One file per weather station per calendar year covered by the Time Range: `Station ID`, `Precipitation`, `Humidity`, `Temperature`, `Windspeed`, `fixtime_year`, `fixtime` — join back to `station_metadata.parquet` on `Station ID` for coordinates and conservancy |

> If the weather station subject group returns no observations for the configured Time Range, the run completes without producing these files rather than raising an error.

---

## Dashboard Widgets

In addition to the two output files, the run's dashboard includes:

| Widget | Source |
|--------|--------|
| **Station Metadata** | `station_metadata.parquet` contents, rendered as a sortable/filterable table |
| **Station Year Weather Data** | The combined weather readings (before they're split per station/year), rendered as a sortable/filterable table |

---

## Further Reading

For an implementation-level breakdown of every task in the compiled workflow spec, see the [Technical Guide](technical_guide/dsc_weather_technical_guide.pdf).
