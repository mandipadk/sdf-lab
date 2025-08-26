from __future__ import annotations
import random, datetime
from typing import Dict, Any, List

# Two demo tools with JSON Schemas
TOOLS = [
    {
        "name": "get_weather",
        "schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string"},
                "date": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"}
            },
            "required": ["city", "date"],
            "additionalProperties": False
        }
    },
    {
        "name": "get_time",
        "schema": {
            "type": "object",
            "properties": {
                "timezone": {"type": "string"}
            },
            "required": ["timezone"],
            "additionalProperties": False
        }
    }
]

CITIES = ["Paris","Tokyo","New York","Kathmandu","Delhi","London"]
ZONES = ["UTC","Europe/Paris","Asia/Tokyo","America/New_York","Asia/Kathmandu"]

def _date_str(offset_days: int = 0) -> str:
    d = datetime.date.today() + datetime.timedelta(days=offset_days)
    return d.strftime("%Y-%m-%d")

def _weather_result(city: str, date: str) -> Dict[str, Any]:
    temp = random.randint(-3, 35)
    cond = random.choice(["sunny","cloudy","rain","showers","windy"])
    return {"temp_c": temp, "condition": cond, "city": city, "date": date}

def _time_result(tz: str) -> Dict[str, Any]:
    # Fake current time string
    return {"timezone": tz, "now": "12:34"}

def generate_tools(n: int = 30, seed: int = 123, params: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    random.seed(seed)
    out: List[Dict[str, Any]] = []
    for i in range(n):
        tool = random.choice(TOOLS)
        if tool["name"] == "get_weather":
            city = random.choice(CITIES)
            date = _date_str(random.randint(0, 3))
            prompt = f"Get the weather for {city} on {date} and tell me if I should carry an umbrella."
            call = {"name": "get_weather", "arguments": {"city": city, "date": date}}
            res = _weather_result(city, date)
            text = f"In {city} on {date}, it will be {res['condition']} around {res['temp_c']}°C. Carry an umbrella if it is rainy."
        else:
            tz = random.choice(ZONES)
            prompt = f"What time is it now in timezone '{tz}'?"
            call = {"name":"get_time","arguments":{"timezone": tz}}
            res = _time_result(tz)
            text = f"The current time in {tz} is approximately {res['now']}."
        out.append({
            "prompt": prompt,
            "tools": [tool],
            "assistant_call": call,
            "assistant_result": res,
            "assistant_response": text,
            "meta": {"domain":"tools","template":"tools_v1","seed": seed+i, "valid": True}
        })
    return out
