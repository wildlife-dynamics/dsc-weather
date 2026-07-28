"""
Generate the DSC Weather Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: dsc_weather_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "dsc_weather_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"DSC Weather — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("DSC Weather", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Weather Station Ingestion — Station Metadata &amp; Readings Pipeline", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>dsc_weather</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>dsc_weather</b> workflow ingests weather station observations from a "
      "configured EarthRanger subject group, tags each station with the conservancy "
      "boundary it falls within, and exports structured, analysis-ready station "
      "metadata and weather reading datasets. Unlike a per-survey pipeline, it "
      "performs a single, station-centric ingestion pass each run — there is no "
      "survey, activity-period, or connection fan-out; every task executes exactly "
      "once against the workflow's single Time Range."),
    sp(4),
    p("Each run delivers:"),
    bullet("A <b>station metadata file</b> — one row per weather station, with its "
           "conservancy and coordinates"),
    bullet("<b>Per-station, per-year weather reading files</b> — precipitation, "
           "temperature, humidity, and wind speed observations"),
    bullet("Two <b>dashboard table widgets</b> exposing both outputs for review "
           "directly from the run's Overview dashboard"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output type", "Format", "Description"],
            ["station_metadata", "Parquet",
             "One row per weather station: Station ID, Conservancy, Latitude, Longitude"],
            ["{station_id}_{year}", "Parquet",
             "One file per weather station per calendar year: Precipitation, Humidity, "
             "Temperature, Windspeed, fixtime_year, fixtime"],
        ],
        [5.5*cm, 2.5*cm, W - 8*cm],
    ),
    note("{station_id} and {year} are derived from the Station ID and fixtime_year "
         "columns respectively. Both output types are produced exactly once per "
         "workflow run — neither is prefixed with a survey or period name, since the "
         "workflow has no survey/period concept."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    p("The workflow declares six versioned packages from the Ecoscope "
      "prefix.dev channels:"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-platform",                      ">=2.15.0, <2.16.0", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",          "0.1.0rc14.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",             "0.0.0rc1.*",   "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-distance-sample-counts", "1.0.2.*", "ecoscope-workflows-custom"],
            ["pydeck",                                  "0.9.2", "conda-forge"],
            ["opentelemetry-sdk",                       ">=1.20.0, <2.0.0", "conda-forge"],
        ],
        [7*cm, 3.5*cm, W - 10.5*cm],
    ),
    note("ecoscope-workflows-ext-ste supplies the spatial_join task used for "
         "conservancy tagging (Section 4.3); ecoscope-workflows-ext-distance-sample-"
         "counts supplies dedupe_by_column and split_weather_by_station_year "
         "(Sections 4.5 and 4.6). Neither pydeck nor a Google Earth Engine connection "
         "is actually exercised by any task in this workflow — pydeck is pinned for "
         "parity with the sibling dsc_analysis workflow this was split out of."),
    sp(6),
    h2("2.2  Weather EarthRanger connection"),
    p("A single EarthRanger connection (<b>set_er_connection</b>, id: "
      "weather_er_client) plus a subject group name (<b>set_string_var</b>, id: "
      "weather_subject_group_name, default: \"TAHMO Stations\") configure the "
      "workflow's only data source."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. INPUT CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Input Configuration"),
    hr(),
    make_table(
        [
            ["Parameter", "Description"],
            ["workflow_details",  "Human-readable name and optional description for this "
                                  "workflow run — used for dashboard registration"],
            ["time_range",        "Required on all Ecoscope workflows. Controls which "
                                  "weather observations are fetched (Since/Until), and is "
                                  "used for timestamp display and UTC conversion"],
            ["groupers",          "Set to an empty list by default (partial: groupers: []) "
                                  "— the workflow does not group its dashboard by any "
                                  "categorical field"],
            ["weather_er_client", "EarthRanger connection hosting the weather station "
                                  "subject group"],
            ["weather_subject_group_name", "EarthRanger subject group name containing the "
                                  "weather stations. RJSF title: \"Weather Station Subject "
                                  "Group\", default: \"TAHMO Stations\""],
        ],
        [4*cm, W - 4*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. DATA INGESTION PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Data Ingestion Pipeline"),
    hr(),
    h2("4.1  Fetching station observations"),
    p("<b>get_subjectgroup_observations</b> (id: fetch_weather_obs) retrieves "
      "observations for the configured weather_subject_group_name from "
      "weather_er_client, over the workflow's time_range (filter: clean, "
      "include_details: true, include_subjectsource_details: false, "
      "raise_on_empty: false — an empty result does not raise an error, it simply "
      "skips every downstream task via the any_is_empty_df / any_dependency_skipped "
      "skip policy, see Section 6.1)."),
    sp(6),
    h2("4.2  Extracting weather variables"),
    p("Four chained calls to <b>extract_value_from_json_column</b> pull numeric "
      "fields out of the extra__observation_details JSON column into flat float "
      "columns:"),
    make_table(
        [
            ["Task id", "Output column", "Source JSON field"],
            ["extract_precipitation", "Precipitation", "precipitation"],
            ["extract_temperature",   "Temperature",   "surface_air_temperature"],
            ["extract_humidity",      "Humidity",      "relative_humidity"],
            ["extract_wind_speed",    "Windspeed",     "wind_speed"],
        ],
        [4.5*cm, 4*cm, W - 8.5*cm],
    ),
    sp(6),
    h2("4.3  Tagging stations with their conservancy"),
    p("A one-time conservancy boundaries file (mara_conservancies.parquet) is "
      "downloaded from Dropbox via <b>fetch_and_persist_file</b> (id: "
      "fetch_conservancy_boundaries; overwrite_existing: false, retries: 3), loaded "
      "with <b>load_df</b> (id: load_conservancy_boundaries), and reprojected to "
      "EPSG:4326 (<b>reproject_gdf</b>, id: reproject_conservancy_boundaries). Each "
      "weather reading is then spatially joined to a conservancy boundary via "
      "<b>ecoscope_workflows_ext_ste.tasks.spatial_operations.spatial_join</b> "
      "(id: weather_conservancy_join; how: inner, predicate: intersects) — stations "
      "that don't fall within any boundary in the file are dropped from the "
      "weather output."),
    sp(6),
    h2("4.4  Identity, coordinates, and date/time decomposition"),
    p("Station identity columns are renamed via <b>map_columns</b> (id: "
      "rename_weather_identity; extra__subject__name &rarr; Station ID, "
      "name &rarr; Conservancy). Latitude and longitude are extracted from the "
      "point geometry via <b>parse_df_point</b> (id: extract_weather_lat_long), "
      "and the fixtime timestamp is split into date, time, and year components via "
      "<b>decompose_datetime</b> (id: decompose_weather_fixtime; components: date, "
      "time, year), then renamed to Date and Time via a second <b>map_columns</b> "
      "call (id: rename_weather_datetime)."),
    sp(6),
    h2("4.5  Station metadata output"),
    p("Station ID, Conservancy, Latitude, and Longitude are selected via "
      "<b>select_columns</b> (id: select_station_metadata) and deduplicated to one "
      "row per station via <b>ecoscope_workflows_ext_distance_sample_counts.tasks."
      "transformation.dedupe_by_column</b> (id: dedupe_station_metadata; column: "
      "Station ID). The result is persisted as <b>station_metadata.parquet</b> via "
      "<b>persist_df</b> (id: persist_station_metadata) — the only persist step in "
      "the workflow that is not fanned out via mapvalues."),
    sp(6),
    h2("4.6  Weather readings output"),
    p("Station ID, Precipitation, Humidity, Temperature, Windspeed, fixtime_year, "
      "and fixtime are selected via <b>select_columns</b> (id: "
      "select_weather_readings) — deliberately omitting Conservancy/Latitude/"
      "Longitude, which live in station_metadata.parquet instead so the per-reading "
      "files stay slim. <b>ecoscope_workflows_ext_distance_sample_counts.tasks."
      "transformation.split_weather_by_station_year</b> (id: "
      "weather_station_year_split) groups the readings by (Station ID, "
      "fixtime_year) and emits one [filename, DataFrame] pair per group, keyed "
      "<b>{station}_{year}</b> (e.g. TAHMO001_2026). Each pair is persisted via "
      "<b>persist_df</b> (id: persist_station_year_weather, filetype: parquet) "
      "using the standard filename/df mapvalues pattern."),
    note("To reconstruct a station's full weather record with location, join a "
         "{station_id}_{year}.parquet file back to station_metadata.parquet on "
         "Station ID."),
    sp(6),
    h2("4.7  Dashboard table widgets"),
    p("Both outputs are additionally rendered as browsable table widgets and "
      "attached to the run's dashboard:"),
    make_table(
        [
            ["Widget", "Source DataFrame", "Task chain"],
            ["Station Metadata", "dedupe_station_metadata.return",
             "draw_table (id: station_metadata_table_html) → persist_text "
             "(id: station_metadata_table_html_url) → "
             "create_table_widget_single_view (id: station_metadata_table_widget)"],
            ["Station Year Weather Data", "select_weather_readings.return",
             "draw_table (id: syw_table_html) → persist_text "
             "(id: syw_table_html_url) → create_table_widget_single_view "
             "(id: syw_table_widget)"],
        ],
        [4*cm, 3.5*cm, W - 7.5*cm],
    ),
    note("The Station Year Weather Data widget renders select_weather_readings' "
         "combined output — the DataFrame as it exists before "
         "weather_station_year_split fans it out into individual per-station-year "
         "files — so the widget shows every reading in one sortable/filterable "
         "table rather than one tiny table per station/year. Both draw_table steps "
         "share the same table_config (enable_sorting: true, enable_filtering: "
         "true, enable_download: false, hide_header: false)."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Output Files"),
    hr(),
    p("All outputs are written to <b>$ECOSCOPE_WORKFLOWS_RESULTS</b>."),
    sp(6),
    make_table(
        [
            ["File", "Format", "Description"],
            ["station_metadata.parquet", "Parquet",
             "One row per weather station, produced once per run: Station ID, "
             "Conservancy, Latitude, Longitude"],
            ["{station_id}_{year}.parquet", "Parquet",
             "One file per weather station per calendar year covered by the Time "
             "Range: Station ID, Precipitation, Humidity, Temperature, Windspeed, "
             "fixtime_year, fixtime"],
        ],
        [5.5*cm, 2.5*cm, W - 8*cm],
    ),
    sp(6),
    note("If the configured weather station subject group returns no observations "
         "for the Time Range, fetch_weather_obs returns an empty DataFrame and the "
         "shared any_is_empty_df / any_dependency_skipped skip policy (Section 6.1) "
         "causes every downstream task — including both persist steps and both "
         "dashboard widgets — to be skipped gracefully rather than raising an error."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Workflow Execution Logic"),
    hr(),
    h2("6.1  Skip conditions"),
    p("All tasks share a global default skip policy defined in "
      "<b>task-instance-defaults</b>:"),
    bullet("<b>any_is_empty_df</b> — skips the task if any upstream DataFrame "
           "dependency is empty"),
    bullet("<b>any_dependency_skipped</b> — skips the task if any upstream "
           "task was itself skipped"),
    p("Because the workflow has a single linear chain from fetch_weather_obs "
      "through to the persist and widget steps, an empty observation fetch (or a "
      "conservancy join that drops every station) propagates a single skip signal "
      "all the way to station_metadata.parquet, every {station_id}_{year}.parquet "
      "file, and both dashboard widgets."),
    sp(6),
    h2("6.2  mapvalues fan-out for per-station-year persistence"),
    p("The workflow is otherwise unfanned — every task runs exactly once — with "
      "one exception: <b>persist_station_year_weather</b> uses <b>mapvalues</b> "
      "(argnames: filename, df) over weather_station_year_split's list of "
      "[filename, DataFrame] pairs, so persist_df runs once per (station, year) "
      "group rather than once for the whole DataFrame."),
    sp(6),
    h2("6.3  Dashboard assembly"),
    p("<b>gather_dashboard</b> (id: overall_dashboard) assembles the run's "
      "dashboard from workflow_details, time_range, groupers (empty), and both "
      "table widgets (station_metadata_table_widget, syw_table_widget). Since "
      "groupers is empty, both widgets use the *_single_view variant of their "
      "widget-creation task rather than a grouped/merged variant."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned"],
            ["ecoscope-platform",                      ">=2.15.0, <2.16.0"],
            ["ecoscope-workflows-ext-custom",          "0.1.0rc14.*"],
            ["ecoscope-workflows-ext-ste",             "0.0.0rc1.*"],
            ["ecoscope-workflows-ext-distance-sample-counts", "1.0.2.*"],
            ["pydeck",                                  "0.9.2"],
            ["opentelemetry-sdk",                       ">=1.20.0, <2.0.0"],
        ],
        [8*cm, W - 8*cm],
    ),
    sp(6),
    note("All packages are resolved from the prefix.dev Ecoscope conda channels. "
         "The wildcard patch-version pin (.*) allows bug-fix releases to be "
         "picked up automatically while keeping minor and major versions locked."),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Written → {OUTPUT_FILE}")
