import demistomock as demisto
from CommonServerPython import *

from CommonServerUserPython import *


def main():
    get_users_response: list = demisto.executeCommand("getUsers", {"onCall": True})
    # Get Away Users
    away_users_response = demisto.executeCommand("GetAwayUsers", {})
    if is_error(away_users_response) or not away_users_response:
        return_error(f"Failed to get away users: {get_error(away_users_response)!s}")
    away_users: list[Dict] = away_users_response[0].get("EntryContext", {}).get("AwayUsers", [])
    away_user_names: list[str] = [away_user.get("username", "") for away_user in away_users] if away_users else []
    all_users = get_users_response[0]["Contents"]
    not_away_users = [user for user in all_users if user["username"] not in away_user_names]

    if is_error(get_users_response):
        demisto.error(f"Failed to get users on call: {get_error(get_users_response)!s}")
    else:
        number_widget = NumberWidget(len(not_away_users))
        return_results(number_widget)


if __name__ in ("__builtin__", "builtins", "__main__"):
    main()
