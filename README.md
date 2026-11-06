# Costa y Cebo

**Estado: versión 0.1 alfa.** Funcionalidad completa para uso personal; pendiente de pulir la comodidad de uso.

Planificador de pesca recreativa desde costa para toda España: eliges un punto en el mapa, el día y la especie, y te da la mejor ventana horaria, el cebo, la marea, el parte de mar y viento, avisos de seguridad, los periodos solunares y la talla mínima. La jornada se puede añadir al calendario.

## Estructura

```
public/index.html      Página publicada (generada, no editar a mano)
public/sw.js           Service worker para usarla sin conexión (generado)
public/manifest.webmanifest, public/icons/  Datos e iconos de la app instalable
src/sw.src.js          Fuente del service worker
src/index.src.html     Código fuente de la página (HTML, CSS y JS)
src/data/tp.js         Predictor armónico de mareas (@neaps/tide-predictor, empaquetado)
src/data/stations.json Constantes armónicas de 45 mareógrafos españoles
src/data/zones.json    Límites oficiales de reservas y zonas protegidas (GeoJSON)
src/data/coast.json    Costa simplificada de respaldo si no carga el mapa del IGN
build.py               Une fuente y datos en public/index.html
wrangler.jsonc         Configuración del Worker de Cloudflare
```

## Hacer cambios

1. Edita `src/index.src.html`.
2. Genera la página: `python build.py`
3. Commit y push. Cloudflare Pages publica `public/` automáticamente en https://costaycebo.pages.dev/.

La dirección pública, el título y la descripción para compartir están en `src/site.json`. `public/og.png` es la imagen que sale al compartir el enlace.

Para probar en local basta con abrir `public/index.html` en el navegador.

## Datos y licencias

- **Mareas:** constantes armónicas TICON-4 (Hart-Davis, M., Dettmering, D., Seitz, F., 2025, SEANOE, https://doi.org/10.17882/109129), vía la base de datos Neaps (https://github.com/openwatersio/tide-database). Licencia **CC BY-NC 4.0**: uso no comercial y con atribución.
- **Parte de mar y viento:** Open-Meteo (https://open-meteo.com), datos CC BY 4.0. La API es gratuita para uso no comercial; un uso comercial requiere plan de pago.
- **Fondos:** EMODnet Bathymetry (capas `emodnet:mean_multicolour` y `emodnet:contours`, y profundidad por punto), propiedad de la UE, CC BY 4.0. Malla de ~100–250 m: aproximado junto a la costa.
- **Predictor de mareas:** `@neaps/tide-predictor` (MIT).
- **Mapa base y ortofoto:** Instituto Geográfico Nacional (IGN Base y PNOA), CC BY 4.0 scne.es. Mapa con Leaflet (BSD-2-Clause).
- **Costa de respaldo:** Natural Earth (dominio público), vía `world-atlas`.
- **Tallas mínimas:** RD 560/1995, RD 347/2011 y Reglamento (UE) 2019/1241. Orientativas; en aguas interiores manda la norma autonómica.
- **Reservas marinas:** límites oficiales de Os Miñarzos (Decreto 87/2007), Ría de Cedeira (Decreto 28/2009 y plan de gestión 2023) e Illas Atlánticas (coordenadas oficiales del Parque y Ley 15/2002). La ZEP I de Cedeira y los cierres por tierra son aproximados. El resto de reservas aparecen como punto hasta añadir sus límites.

Las mareas son astronómicas y el parte es una previsión de modelo: orientativos, no usar para navegación.
