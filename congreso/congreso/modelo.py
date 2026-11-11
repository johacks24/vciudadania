"""Modelo de datos (pydantic). El esquema se define ANTES del código (regla del proyecto).

Origen del esquema: JSON oficial por votación del opendata del Congreso,
verificado el 10/11/2026 (ver docs/lotes/20261110_fundamentos-y-spike/notas.md).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

# Valores observados del campo "voto" (distribución verificada sobre la sesión 202:
# 4.084 Sí, 2.020 No, 810 Abstención, 86 No vota). Si aparece uno nuevo, la validación
# lo detectará como descuadre y lo veremos en la distribución de valores.
SENTIDOS = {"Sí": "afavor", "No": "enContra", "Abstención": "abstenciones", "No vota": "noVotan"}


class Informacion(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    sesion: int
    numero_votacion: int = Field(alias="numeroVotacion")
    fecha: str
    titulo: str
    texto_expediente: str = Field(alias="textoExpediente")
    titulo_subgrupo: str = Field(default="", alias="tituloSubGrupo")
    texto_subgrupo: str = Field(default="", alias="textoSubGrupo")


class Totales(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    asentimiento: str
    presentes: int
    afavor: int
    en_contra: int = Field(alias="enContra")
    abstenciones: int
    no_votan: int = Field(alias="noVotan")


class VotoIndividual(BaseModel):
    asiento: str
    diputado: str
    grupo: str
    voto: str


class RegistroVotacion(BaseModel):
    """Un registro de votación del opendata del Congreso."""

    informacion: Informacion
    totales: Totales
    votaciones: list[VotoIndividual]
    fuente_url: str = ""

    @property
    def id(self) -> str:
        return f"Leg{self.informacion.sesion}-{self.informacion.numero_votacion:03d}"

    @property
    def sin_voto_individual(self) -> bool:
        """Suplicatorios (secreto) y asentimiento: solo se publican totales."""
        return len(self.votaciones) == 0

    def contar_por_sentido(self) -> dict[str, int]:
        cuenta = {"Sí": 0, "No": 0, "Abstención": 0, "No vota": 0, "otro": 0}
        for v in self.votaciones:
            if v.voto in cuenta:
                cuenta[v.voto] += 1
            else:
                cuenta["otro"] += 1
        return cuenta

    def validar(self) -> list[str]:
        """Discrepancias entre el detalle individual y los totales oficiales.

        Vacío = validación correcta. Para registros sin voto individual no hay
        nada que cuadrar: devolvemos vacío (categoría, no error).
        """
        if self.sin_voto_individual:
            return []
        c = self.contar_por_sentido()
        t = self.totales
        d: list[str] = []
        if c["Sí"] != t.afavor:
            d.append(f"Sí: detalle {c['Sí']} ≠ oficial {t.afavor}")
        if c["No"] != t.en_contra:
            d.append(f"No: detalle {c['No']} ≠ oficial {t.en_contra}")
        if c["Abstención"] != t.abstenciones:
            d.append(f"Abstención: detalle {c['Abstención']} ≠ oficial {t.abstenciones}")
        if c["No vota"] != t.no_votan:
            d.append(f"No vota: detalle {c['No vota']} ≠ oficial {t.no_votan}")
        if c["otro"]:
            d.append(f"valores de voto no catalogados: {c['otro']}")
        registrados = len(self.votaciones)
        esperados = t.presentes + t.no_votan
        if registrados != esperados:
            d.append(f"votos registrados {registrados} ≠ presentes+noVotan {esperados}")
        return d

    def resumen_por_grupo(self) -> list[dict]:
        """Recuento por grupo parlamentario, ordenado por nº de votos emitidos."""
        grupos: dict[str, dict[str, int]] = {}
        for v in self.votaciones:
            g = grupos.setdefault(v.grupo, {"Sí": 0, "No": 0, "Abstención": 0, "No vota": 0, "otro": 0})
            clave = v.voto if v.voto in g else "otro"
            g[clave] += 1
        return sorted(
            ({"grupo": k, **v} for k, v in grupos.items()),
            key=lambda r: -(r["Sí"] + r["No"] + r["Abstención"]),
        )
