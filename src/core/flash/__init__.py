from typing import Any

from starlette.requests import Request


def flash_message(request: Request, msg: str, errors: dict[str, str] | None = None, category: str = "default") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []

    # Add main message (optional)
    if msg:
        request.session["_messages"].append({"message": msg, "category": category})

    # Add field-specific errors
    if errors:
        if isinstance(errors, dict):
            for field, err_msg in errors.items():
                full_msg = f"{field.capitalize()}: {err_msg}"
                request.session["_messages"].append({"message": full_msg, "category": category})
        else:
            request.session["_messages"].append({"message": errors, "category": category})



def get_flash_messages(request: Request) -> list:
    return request.session.pop("_messages") if "_messages" in request.session else []
