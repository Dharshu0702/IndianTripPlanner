"""PDF generation service using ReportLab."""

from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether,
)

PRIMARY = HexColor("#4F46E5")
DARK = HexColor("#1a1a2e")
GRAY = HexColor("#6B7280")
LIGHT_BG = HexColor("#F3F4F6")
WHITE = HexColor("#FFFFFF")
GREEN = HexColor("#059669")


def _get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="AppTitle", parent=styles["Title"], fontSize=26, textColor=PRIMARY, spaceAfter=6, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="AppSubtitle", parent=styles["Normal"], fontSize=11, textColor=GRAY, alignment=TA_CENTER, spaceAfter=20))
    styles.add(ParagraphStyle(name="SectionHeader", parent=styles["Heading2"], fontSize=16, textColor=PRIMARY, spaceBefore=16, spaceAfter=8, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="SubHeader", parent=styles["Heading3"], fontSize=13, textColor=DARK, spaceBefore=10, spaceAfter=6, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="Body2", parent=styles["Normal"], fontSize=10, textColor=DARK, spaceBefore=2, spaceAfter=2))
    styles.add(ParagraphStyle(name="CostTotal", parent=styles["Normal"], fontSize=14, textColor=GREEN, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="Footer", parent=styles["Normal"], fontSize=8, textColor=GRAY, alignment=TA_CENTER))
    return styles


def generate_trip_pdf(trip, plan, booking=None):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=2*cm, bottomMargin=2*cm)
    styles = _get_styles()
    story = []

    story.append(Paragraph("India Smart Trip Planner", styles["AppTitle"]))
    story.append(Paragraph("AI-Powered Travel Itinerary", styles["AppSubtitle"]))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY, spaceAfter=12))

    dest = trip.get("destination", {})
    origin = trip.get("origin_location", {})
    inputs = trip.get("inputs", {})

    # Trip Summary Table
    story.append(Paragraph("Trip Summary", styles["SectionHeader"]))
    summary = [
        ["Origin", origin.get("address", "N/A")],
        ["Destination", f"{dest.get('place','N/A')}, {dest.get('state','N/A')}"],
        ["Distance", f"{trip.get('distance_km',0):,.1f} km"],
        ["Travel Time", trip.get("travel_time", "N/A")],
        ["Travelers", str(inputs.get("travelers", "N/A"))],
        ["Duration", f"{inputs.get('days','N/A')} days"],
        ["Trip Type", inputs.get("trip_type", "N/A")],
        ["Plan", plan.get("plan_name", "N/A")],
    ]
    t = Table(summary, colWidths=[3.5*cm, 13*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(0,-1), LIGHT_BG), ("TEXTCOLOR", (0,0),(0,-1), GRAY),
        ("FONTNAME", (0,0),(0,-1), "Helvetica-Bold"), ("FONTSIZE", (0,0),(-1,-1), 10),
        ("TOPPADDING", (0,0),(-1,-1), 6), ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("GRID", (0,0),(-1,-1), 0.5, HexColor("#E5E7EB")),
    ]))
    story.append(t)
    story.append(Spacer(1, 16))

    # Travel & Hotel
    story.append(Paragraph("Travel Details", styles["SectionHeader"]))
    story.append(Paragraph(f"<b>Mode:</b> {plan.get('travel_mode','N/A')}", styles["Body2"]))
    story.append(Paragraph(f"<b>Hotel:</b> {plan.get('hotel_name','N/A')}", styles["Body2"]))
    story.append(Spacer(1, 12))

    # Cost Breakdown
    story.append(Paragraph("Cost Breakdown (INR)", styles["SectionHeader"]))
    days = inputs.get("days", 1)
    costs = [
        ["Category", "Amount"],
        ["Travel (Round Trip)", f"Rs.{plan.get('travel_cost',0):,.0f}"],
        ["Hotel", f"Rs.{plan.get('hotel_cost_per_night',0)*days:,.0f}"],
        ["Food", f"Rs.{plan.get('food_cost_per_day',0)*days:,.0f}"],
        ["Local Transport", f"Rs.{plan.get('local_transport_per_day',0)*days:,.0f}"],
    ]
    ct = Table(costs, colWidths=[10*cm, 6.5*cm])
    ct.setStyle(TableStyle([
        ("BACKGROUND", (0,0),(-1,0), PRIMARY), ("TEXTCOLOR", (0,0),(-1,0), WHITE),
        ("FONTNAME", (0,0),(-1,0), "Helvetica-Bold"), ("FONTSIZE", (0,0),(-1,-1), 10),
        ("TOPPADDING", (0,0),(-1,-1), 7), ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ("GRID", (0,0),(-1,-1), 0.5, HexColor("#E5E7EB")),
        ("ALIGN", (1,0),(1,-1), "RIGHT"),
    ]))
    story.append(ct)
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"<b>Grand Total: Rs.{plan.get('total_cost',0):,.0f}</b>", styles["CostTotal"]))
    story.append(Spacer(1, 16))

    # Places
    places = plan.get("places_to_visit", [])
    if places:
        story.append(Paragraph("Places to Visit", styles["SectionHeader"]))
        for i, p in enumerate(places, 1):
            story.append(Paragraph(f"  {i}. {p}", styles["Body2"]))
        story.append(Spacer(1, 12))

    # Itinerary
    itinerary = plan.get("day_wise_itinerary", [])
    if itinerary:
        story.append(Paragraph("Day-wise Itinerary", styles["SectionHeader"]))
        for day in itinerary:
            block = [Paragraph(f"Day {day.get('day','?')}: {day.get('title','')}", styles["SubHeader"])]
            for act in day.get("activities", []):
                block.append(Paragraph(f"  - {act}", styles["Body2"]))
            block.append(Spacer(1, 6))
            story.append(KeepTogether(block))

    # Map link
    story.append(Spacer(1, 12))
    ml = f"https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route={origin.get('lat','')},{origin.get('lng','')};{dest.get('place','')},+India"
    story.append(Paragraph("Route Map", styles["SectionHeader"]))
    story.append(Paragraph(f'<link href="{ml}" color="blue"><u>Open Route on OpenStreetMap</u></link>', styles["Body2"]))

    # Footer
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color=GRAY, spaceAfter=8))
    story.append(Paragraph("Generated by India Smart Trip Planner | All costs in INR (estimates)", styles["Footer"]))

    doc.build(story)
    buffer.seek(0)
    return buffer
