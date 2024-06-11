from pathlib import Path

import pandas as pd


def pd_to_csv(
    *,
    path: Path,
    data: pd.DataFrame,
) -> None:
    data.to_csv(path_or_buf=path, index=False, encoding="utf-8")
