class BattleReport:
    """This class responds for battle report text generating"""

    def __init__(self) -> None:
        self.parsed_hq_report: list[dict[str, str | int | None]] = []
        self.parsed_map_report: list[dict[str, str | None]] = []


battle_report = BattleReport()
