from typing import List, Tuple, TypedDict, Union, Optional, Any

import pandas as pd
import requests


class TopPlayer(TypedDict):
    first_name: str
    second_name: str
    minutes: int
    roi: float
    now_cost: int
    total_points: float
    position: str
    team_name: str
    status: str


# TODO proper type this
class FPLData(TypedDict):
    events: List[Any]
    game_settings: List[Any]
    phases: List[Any]
    teams: List[Any]
    total_players: int
    elements: List[Any]
    element_types: List[Any]


def build_dream_team(
    budget: float = 100,
    star_player_limit: int = 3,
    gk: int = 2,
    df: int = 5,
    md: int = 5,
    fwd: int = 3,
) -> Tuple[List[TopPlayer], Union[float, int]]:
    """Return the best team based on their value

    :param budget: the amount that i can spend
    :param star_player_limit: how many star players i can have in one team
    :param gk: number of goalkeepers
    :param df: number of defenders
    :param md: number of midfielders
    :param fwd: number of forwards

    :return: (team, total_points) -> the players in the team  and their total points
    """

    team = []

    star_player_limit = star_player_limit
    budget = budget

    players = players_by_status(
        status=["injured", "not_available", "suspended"],
        filter_in=False,
        players=roi_top_players(),
    )
    positions = {"Goalkeeper": gk, "Defender": df, "Midfielder": md, "Forward": fwd}
    # TODO there is a change that more than 3 players are in the same team
    # figure out a way to skip if that's true
    for player in players:
        if (
            player not in team
            and budget >= player["now_cost"] / 10
            and positions[player["position"]] > 0
        ):
            team.append(player)
            budget -= player["now_cost"] / 10
            positions[player["position"]] -= 1

    total_points = sum([player["total_points"] for player in team])

    return team, total_points


def players_by_status(
    status: Union[str, List[str], Tuple[str]],
    filter_in: bool = True,
    players: Optional[Union[pd.DataFrame, List[TopPlayer]]] = None,
) -> List[TopPlayer]:
    """Return a list of players filtered by their status.

    :param status: the status of the player
    :param filter_in: whether to filter with the status of without
    :param players: list of players to be filtered

    :return: list of players
    """

    elements_df: pd.DataFrame = pd.DataFrame()

    statuses = {
        "injured": "i",
        "suspended": "s",
        "not_available": "n",
        "available": "a",
        "doubtful": "d",
    }

    if players is None:
        json: FPLData = requests.get(
            "https://fantasy.premierleague.com/api/bootstrap-static/"
        ).json()

        elements_df = pd.DataFrame(
            data=json["elements"],
            columns=[
                "first_name",
                "second_name",
                "status",
            ],
        )

    if players is not None and type(players) == list:
        elements_df = pd.DataFrame(players)

    if players is not None and type(players) == pd.DataFrame:
        elements_df = players

    if type(status) == str:
        is_status: pd.Series = (
            elements_df["status"] == statuses[status]  # type: ignore
            if filter_in
            else elements_df["status"] != statuses[status]  # type: ignore
        )

        players_list: pd.DataFrame = elements_df[is_status]

        return players_list.to_dict("records")

    if type(status) == list or tuple:
        list_of_statuses: List[str] = [statuses[s] for s in status]

        if not filter_in:
            list_of_statuses = [statuses[s] for s in statuses.keys() if s not in status]

        is_status = elements_df["status"].isin(list_of_statuses)

        players_list = elements_df[is_status]

        return players_list.to_dict("records")


def roi_top_players() -> List[TopPlayer]:
    """Get a list of players sorted by their value and most played time in FPL.

    :return: list of players
    """

    json: FPLData = requests.get(
        "https://fantasy.premierleague.com/api/bootstrap-static/"
    ).json()

    elements_df: pd.DataFrame = pd.DataFrame(
        data=json["elements"],
        columns=[
            "first_name",
            "second_name",
            "team",
            "element_type",
            "now_cost",
            "minutes",
            "value_season",
            "total_points",
            "status",
        ],
    )
    elements_types_df = pd.DataFrame(json["element_types"])
    teams_df = pd.DataFrame(data=json["teams"])
    elements_df["position"] = elements_df.element_type.map(
        elements_types_df.set_index("id").singular_name
    )

    elements_df["team_name"] = elements_df.team.map(teams_df.set_index("id").name)

    elements_df["roi"] = elements_df["value_season"].astype(float)

    players_df: pd.DataFrame = elements_df.filter(
        [
            "first_name",
            "second_name",
            "minutes",
            "roi",
            "now_cost",
            "total_points",
            "position",
            "team_name",
            "status",
        ],
        axis=1,
    ).sort_values(["minutes", "roi"], ascending=False)

    return players_df.to_dict("records")


def transfer():
    # TODO

    raise NotImplementedError
