import os
from datetime import datetime
from typing import List, Optional
import pandas as pd


class AgendaStore:
    def __init__(self, path: Optional[str] = None):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        data_dir = os.path.join(base_dir, "data")
        os.makedirs(data_dir, exist_ok=True)
        self.path = path or os.path.join(data_dir, "agenda.xlsx")
        self.columns = ["Evento", "Fecha", "Hora"]
        self._ensure_file()

    def _ensure_file(self) -> None:
        if not os.path.exists(self.path):
            df = pd.DataFrame(columns=self.columns)
            df.to_excel(self.path, index=False, engine="openpyxl")
        else:
            df = pd.read_excel(self.path, engine="openpyxl")
            missing = [c for c in self.columns if c not in df.columns]
            if missing:
                for c in missing:
                    df[c] = ""
                df = df[self.columns]
                df.to_excel(self.path, index=False, engine="openpyxl")

    def _read(self) -> pd.DataFrame:
        return pd.read_excel(self.path, engine="openpyxl")

    def _write(self, df: pd.DataFrame) -> None:
        df.to_excel(self.path, index=False, engine="openpyxl")

    def add_event(self, evento: str, fecha: str, hora: str) -> None:
        self._validate_fecha(fecha)
        self._validate_hora(hora)
        df = self._read()
        new_row = {"Evento": evento.strip(), "Fecha": fecha.strip(), "Hora": hora.strip()}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        self._write(df)

    def delete_event(self, evento: str, fecha: Optional[str] = None, hora: Optional[str] = None) -> int:
        df = self._read()
        mask = df["Evento"].str.strip().str.lower() == evento.strip().lower()
        if fecha:
            self._validate_fecha(fecha)
            mask = mask & (df["Fecha"].astype(str).str.strip() == fecha.strip())
        if hora:
            self._validate_hora(hora)
            mask = mask & (df["Hora"].astype(str).str.strip() == hora.strip())
        count = int(mask.sum())
        if count > 0:
            df = df.loc[~mask]
            self._write(df)
        return count

    def query_by_date(self, fecha: str) -> List[dict]:
        self._validate_fecha(fecha)
        df = self._read()
        result = df[df["Fecha"].astype(str).str.strip() == fecha.strip()]
        return result.to_dict(orient="records")

    def all_events(self) -> List[dict]:
        df = self._read()
        return df.to_dict(orient="records")

    def _validate_fecha(self, fecha: str) -> None:
        datetime.strptime(fecha, "%Y-%m-%d")

    def _validate_hora(self, hora: str) -> None:
        datetime.strptime(hora, "%H:%M")
