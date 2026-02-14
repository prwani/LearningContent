"""Simple demo MCP server for general user management operations.

This server provides basic user CRUD operations, email sending,
and weather information retrieval capabilities.
"""

from datetime import datetime, timezone
import os
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field
from rich import print

mcp = FastMCP(
    name="Generic MCP Server",
)


@mcp.tool(name="get_user_info", description="Get user information by user ID.")
def get_user_info(user_id: Annotated[str, Field(description="The user id")]) -> dict:
    print(f"[red]invoking tool:get_user_info user_id={user_id}[/red]")
    return {
        "user_id": user_id,
        "name": "Jamie Rivera",
        "email": "jamie.rivera@example.com",
        "plan": "pro",
    }


@mcp.tool(name="add_new_user", description="Create a new user account in the system.")
def add_new_user(
    name: Annotated[str, Field(description="Full name of the user")],
    email: Annotated[str, Field(description="Email address of the user")],
    plan: Annotated[
        str, Field(description="Subscription plan (e.g., free, pro, enterprise)")
    ],
) -> dict:
    print(
        f"[green]invoking tool:add_new_user name={name}, email={email}, plan={plan}[/green]"
    )
    return {
        "status": "created",
        "user_id": "usr_789xyz",
        "name": name,
        "email": email,
        "plan": plan,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool(
    name="delete_user", description="Permanently delete a user account from the system."
)
def delete_user(
    user_id: Annotated[str, Field(description="The user id to delete")],
) -> dict:
    print(f"[red]invoking tool:delete_user user_id={user_id}[/red]")
    return {
        "status": "deleted",
        "user_id": user_id,
        "deleted_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool(
    name="update_user", description="Update one or more fields of a user's profile."
)
def update_user(
    user_id: Annotated[str, Field(description="The user id to update")],
    name: Annotated[
        str | None, Field(description="New name for the user (optional)")
    ] = None,
    email: Annotated[
        str | None, Field(description="New email for the user (optional)")
    ] = None,
    plan: Annotated[
        str | None, Field(description="New plan for the user (optional)")
    ] = None,
) -> dict:
    updates = {}
    if name:
        updates["name"] = name
    if email:
        updates["email"] = email
    if plan:
        updates["plan"] = plan

    print(
        f"[yellow]invoking tool:update_user user_id={user_id}, updates={updates}[/yellow]"
    )
    return {
        "status": "updated",
        "user_id": user_id,
        "updated_fields": list(updates.keys()),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool(name="get_weather", description="Get the current weather for a location.")
def get_weather(
    location: Annotated[str, Field(description="City, region, or landmark")],
) -> dict:
    print(f"[blue]invoking tool:get_weather location={location}[/blue]")
    return {
        "location": location,
        "condition": "clear",
        "temperature_c": 22,
        "wind_kph": 9,
    }


@mcp.tool(
    name="send_email", description="Send an email to a recipient with subject and body."
)
def send_email(
    to: Annotated[str, Field(description="Recipient email address")],
    subject: Annotated[str, Field(description="Email subject line")],
    body: Annotated[str, Field(description="Email body content")],
) -> dict:
    print(
        f"[magenta]invoking tool:send_email to={to}, subject={subject}, body={body}[/magenta]"
    )
    return {
        "status": "sent",
        "to": to,
        "subject": subject,
        "message_id": "msg-12345",
    }


@mcp.tool(
    name="receive_email", description="Fetch unread emails from the user's inbox."
)
def receive_email() -> dict:
    print(f"[yellow]invoking tool:receive_email fetching inbox[/yellow]")
    return {
        "status": "success",
        "unread_count": 3,
        "emails": [
            {
                "from": "alice@example.com",
                "subject": "Meeting tomorrow",
                "preview": "Just confirming our 2pm meeting...",
            },
            {
                "from": "support@service.com",
                "subject": "Your account update",
                "preview": "We've updated your account settings...",
            },
            {
                "from": "team@company.com",
                "subject": "Weekly summary",
                "preview": "Here's what happened this week...",
            },
        ],
    }


@mcp.tool(
    name="get_bus_route", description="Get bus route information between two locations."
)
def get_bus_route(
    from_location: Annotated[str, Field(description="Starting location")],
    to_location: Annotated[str, Field(description="Destination location")],
) -> dict:
    print(
        f"[cyan]invoking tool:get_bus_route from={from_location}, to={to_location}[/cyan]"
    )
    return {
        "route": "Bus 42",
        "from": from_location,
        "to": to_location,
        "duration_minutes": 25,
        "next_departure": "10:15",
        "fare": 2.50,
    }


@mcp.tool(
    name="list_available_movies",
    description="Get list of movies currently showing in theaters.",
)
def list_available_movies(
    location: Annotated[
        str | None, Field(description="City or area (optional)")
    ] = None,
) -> dict:
    print(f"[magenta]invoking tool:list_available_movies location={location}[/magenta]")
    return {
        "location": location or "nearby",
        "movies": [
            {
                "title": "The Adventure",
                "genre": "Action",
                "rating": "PG-13",
                "showtimes": ["14:00", "17:30", "20:00"],
            },
            {
                "title": "Cosmic Dreams",
                "genre": "Sci-Fi",
                "rating": "PG",
                "showtimes": ["15:00", "18:30"],
            },
            {
                "title": "Comedy Night",
                "genre": "Comedy",
                "rating": "R",
                "showtimes": ["16:00", "19:00"],
            },
        ],
    }


@mcp.tool(name="book_restaurant", description="Book a table at a restaurant.")
def book_restaurant(
    restaurant_name: Annotated[str, Field(description="Name of the restaurant")],
    date: Annotated[str, Field(description="Date for the reservation (YYYY-MM-DD)")],
    time: Annotated[str, Field(description="Time for the reservation (HH:MM)")],
    party_size: Annotated[int, Field(description="Number of people")],
) -> dict:
    print(
        f"[green]invoking tool:book_restaurant {restaurant_name}, {date} {time}, party={party_size}[/green]"
    )
    return {
        "status": "confirmed",
        "restaurant": restaurant_name,
        "date": date,
        "time": time,
        "party_size": party_size,
        "confirmation_code": "RSV-789123",
    }


@mcp.tool(
    name="get_news_headlines", description="Get latest news headlines by category."
)
def get_news_headlines(
    category: Annotated[
        str | None, Field(description="News category (e.g., world, tech, sports)")
    ] = None,
) -> dict:
    print(f"[blue]invoking tool:get_news_headlines category={category}[/blue]")
    return {
        "category": category or "general",
        "headlines": [
            {"title": "Markets hit record high", "source": "Finance Times"},
            {"title": "New tech breakthrough announced", "source": "Tech Daily"},
            {"title": "Weather alert issued for region", "source": "Local News"},
        ],
    }


@mcp.tool(
    name="translate_text", description="Translate text from one language to another."
)
def translate_text(
    text: Annotated[str, Field(description="Text to translate")],
    target_language: Annotated[
        str, Field(description="Target language (e.g., fr, es, de)")
    ],
) -> dict:
    print(f"[yellow]invoking tool:translate_text to {target_language}[/yellow]")
    return {
        "original": text,
        "translated": f"{text} (translated to {target_language})",
        "target_language": target_language,
        "confidence": 0.95,
    }


@mcp.tool(
    name="set_reminder", description="Set a reminder for a specific date and time."
)
def set_reminder(
    title: Annotated[str, Field(description="Reminder title")],
    date: Annotated[str, Field(description="Date (YYYY-MM-DD)")],
    time: Annotated[str, Field(description="Time (HH:MM)")],
) -> dict:
    print(f"[red]invoking tool:set_reminder {title} at {date} {time}[/red]")
    return {
        "status": "created",
        "reminder_id": "rem-456",
        "title": title,
        "scheduled_for": f"{date} {time}",
    }


@mcp.tool(
    name="check_calendar", description="Check calendar events for a specific date."
)
def check_calendar(
    date: Annotated[str, Field(description="Date to check (YYYY-MM-DD)")],
) -> dict:
    print(f"[cyan]invoking tool:check_calendar date={date}[/cyan]")
    return {
        "date": date,
        "events": [
            {"time": "09:00", "title": "Team meeting", "duration": "1h"},
            {"time": "14:00", "title": "Client call", "duration": "30m"},
            {"time": "16:30", "title": "Project review", "duration": "45m"},
        ],
    }


@mcp.tool(name="order_food", description="Order food delivery from a restaurant.")
def order_food(
    restaurant: Annotated[str, Field(description="Restaurant name")],
    items: Annotated[str, Field(description="Comma-separated list of items to order")],
    delivery_address: Annotated[str, Field(description="Delivery address")],
) -> dict:
    print(f"[magenta]invoking tool:order_food from {restaurant}[/magenta]")
    return {
        "status": "confirmed",
        "order_id": "ORD-8899",
        "restaurant": restaurant,
        "items": items.split(","),
        "estimated_delivery": "30-45 minutes",
        "total": 28.50,
    }


@mcp.tool(name="get_recipe", description="Get a recipe for a specific dish.")
def get_recipe(
    dish_name: Annotated[str, Field(description="Name of the dish")],
) -> dict:
    print(f"[green]invoking tool:get_recipe {dish_name}[/green]")
    return {
        "name": dish_name,
        "prep_time": "15 minutes",
        "cook_time": "30 minutes",
        "servings": 4,
        "ingredients": ["ingredient 1", "ingredient 2", "ingredient 3"],
        "instructions": "Step 1: Prepare. Step 2: Cook. Step 3: Serve.",
    }


@mcp.tool(
    name="track_package", description="Track a shipping package by tracking number."
)
def track_package(
    tracking_number: Annotated[str, Field(description="Package tracking number")],
) -> dict:
    print(f"[blue]invoking tool:track_package {tracking_number}[/blue]")
    return {
        "tracking_number": tracking_number,
        "status": "in_transit",
        "current_location": "Distribution Center, Chicago",
        "estimated_delivery": "2026-01-25",
        "last_update": "2026-01-23 08:00",
    }


@mcp.tool(name="book_hotel", description="Book a hotel room.")
def book_hotel(
    hotel_name: Annotated[str, Field(description="Name of the hotel")],
    check_in: Annotated[str, Field(description="Check-in date (YYYY-MM-DD)")],
    check_out: Annotated[str, Field(description="Check-out date (YYYY-MM-DD)")],
    guests: Annotated[int, Field(description="Number of guests")],
) -> dict:
    print(f"[yellow]invoking tool:book_hotel {hotel_name} for {guests} guests[/yellow]")
    return {
        "status": "confirmed",
        "hotel": hotel_name,
        "check_in": check_in,
        "check_out": check_out,
        "guests": guests,
        "confirmation_number": "HTL-5544",
        "room_type": "Standard Double",
    }


@mcp.tool(
    name="get_exchange_rate",
    description="Get current exchange rate between two currencies.",
)
def get_exchange_rate(
    from_currency: Annotated[
        str, Field(description="Source currency code (e.g., USD)")
    ],
    to_currency: Annotated[str, Field(description="Target currency code (e.g., EUR)")],
) -> dict:
    print(
        f"[red]invoking tool:get_exchange_rate {from_currency} to {to_currency}[/red]"
    )
    return {
        "from": from_currency,
        "to": to_currency,
        "rate": 0.92,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool(
    name="check_traffic", description="Check current traffic conditions for a route."
)
def check_traffic(
    from_location: Annotated[str, Field(description="Starting point")],
    to_location: Annotated[str, Field(description="Destination")],
) -> dict:
    print(
        f"[cyan]invoking tool:check_traffic from {from_location} to {to_location}[/cyan]"
    )
    return {
        "from": from_location,
        "to": to_location,
        "traffic_level": "moderate",
        "estimated_time": "35 minutes",
        "fastest_route": "Highway 101",
        "incidents": ["Construction on Main St", "Heavy traffic near downtown"],
    }


@mcp.tool(
    name="find_nearby_places", description="Find nearby places of a specific type."
)
def find_nearby_places(
    place_type: Annotated[
        str,
        Field(description="Type of place (e.g., restaurant, gas_station, pharmacy)"),
    ],
    location: Annotated[
        str | None,
        Field(description="Location (optional, uses current location if not provided)"),
    ] = None,
) -> dict:
    print(
        f"[magenta]invoking tool:find_nearby_places {place_type} near {location}[/magenta]"
    )
    return {
        "place_type": place_type,
        "location": location or "current location",
        "results": [
            {"name": f"Place A", "distance": "0.5 km", "rating": 4.5},
            {"name": f"Place B", "distance": "1.2 km", "rating": 4.2},
            {"name": f"Place C", "distance": "2.0 km", "rating": 4.8},
        ],
    }


@mcp.tool(
    name="schedule_appointment",
    description="Schedule an appointment with a service provider.",
)
def schedule_appointment(
    provider: Annotated[
        str, Field(description="Service provider name (e.g., dentist, doctor)")
    ],
    date: Annotated[str, Field(description="Appointment date (YYYY-MM-DD)")],
    time: Annotated[str, Field(description="Appointment time (HH:MM)")],
    reason: Annotated[
        str | None, Field(description="Reason for appointment (optional)")
    ] = None,
) -> dict:
    print(f"[green]invoking tool:schedule_appointment with {provider}[/green]")
    return {
        "status": "scheduled",
        "provider": provider,
        "date": date,
        "time": time,
        "reason": reason,
        "appointment_id": "APT-9988",
    }


@mcp.tool(
    name="get_sports_scores",
    description="Get latest sports scores for a specific sport or league.",
)
def get_sports_scores(
    sport: Annotated[
        str, Field(description="Sport or league name (e.g., NBA, NFL, soccer)")
    ],
) -> dict:
    print(f"[blue]invoking tool:get_sports_scores {sport}[/blue]")
    return {
        "sport": sport,
        "games": [
            {"teams": "Team A vs Team B", "score": "95-88", "status": "Final"},
            {"teams": "Team C vs Team D", "score": "102-99", "status": "Final"},
            {"teams": "Team E vs Team F", "score": "45-32", "status": "Live - Q3"},
        ],
    }


@mcp.tool(
    name="check_flight_status",
    description="Check the status of a flight by flight number.",
)
def check_flight_status(
    flight_number: Annotated[str, Field(description="Flight number (e.g., AA123)")],
) -> dict:
    print(f"[yellow]invoking tool:check_flight_status {flight_number}[/yellow]")
    return {
        "flight_number": flight_number,
        "status": "On Time",
        "departure_time": "14:30",
        "arrival_time": "17:45",
        "gate": "B12",
        "terminal": "2",
    }


@mcp.tool(
    name="search_jobs", description="Search for job openings by keywords and location."
)
def search_jobs(
    keywords: Annotated[
        str, Field(description="Job search keywords (e.g., 'software engineer')")
    ],
    location: Annotated[str | None, Field(description="Location (optional)")] = None,
) -> dict:
    print(f"[red]invoking tool:search_jobs {keywords} in {location}[/red]")
    return {
        "keywords": keywords,
        "location": location or "remote",
        "results": [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "location": "Remote",
                "posted": "2 days ago",
            },
            {
                "title": "Senior Developer",
                "company": "StartupXYZ",
                "location": location or "San Francisco",
                "posted": "1 week ago",
            },
            {
                "title": "Full Stack Engineer",
                "company": "Innovation Inc",
                "location": "New York",
                "posted": "3 days ago",
            },
        ],
    }


if __name__ == "__main__":
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("MCP_PORT", "8000"))
    mcp.run(transport="http", host=host, port=port)
