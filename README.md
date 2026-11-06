# Costa y Cebo

Planificador de pesca recreativa desde costa para toda España: eliges un punto en el mapa, el día y la especie, y te da la mejor ventana horaria, el cebo, la marea, el parte de mar y viento, avisos de seguridad, los periodos solunares y la talla mínima. La jornada se puede añadir al calendario.

## Estructura

```
public/index.html      Página publicada (generada, no editar a mano)
src/index.src.html     Código fuente de la página (HTML, CSS y JS)
src/data/tp.js         Predictor armónico de mareas (@neaps/tide-predictor, empaquetado)
src/data/stations.json Constantes armónicas de 45 mareógrafos españoles
src/data/map.json      Línea de costa simplificada para el mapa
build.py               Une fuente y datos en public/index.html
wrangler.jsonc         Configuración del Worker de Cloudflare
```

## Hacer cambios

1. Edita `src/index.src.html`.
2. Genera la página: `python build.py`
3. Commit y push. Cloudflare publica `public/` automáticamente.

Para probar en local basta con abrir `public/index.html` en el navegador.

## Datos y licencias

- **Mareas:** constantes armónicas TICON-4 (Hart-Davis, M., Dettmering, D., Seitz, F., 2025, SEANOE, https://doi.org/10.17882/109129), vía la base de datos Neaps (https://github.com/openwatersio/tide-database). Licencia **CC BY-NC 4.0**: uso no comercial y con atribución.
- **Parte de mar y viento:** Open-Meteo (https://open-meteo.com), datos CC BY 4.0. La API es gratuita para uso no comercial; un uso comercial requiere plan de pago.
- **Predictor de mareas:** `@neaps/tide-predictor` (MIT).
- **Línea de costa:** Natural Earth (dominio público), vía `world-atlas`.
- **Tallas mínimas:** RD 560/1995, RD 347/2011 y Reglamento (UE) 2019/1241. Orientativas; en aguas interiores manda la norma autonómica.
- **Reservas marinas:** posición aproximada, no límites legales. Fichas oficiales en el MAPA y en cada comunidad.

Las mareas son astronómicas y el parte es una previsión de modelo: orientativos, no usar para navegación.
