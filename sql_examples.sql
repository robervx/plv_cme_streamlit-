-- Example SQL views/queries (adjust to your schema)

-- Monthly interventions
SELECT
  CONVERT(date, DATEFROMPARTS(YEAR(fecha_inicio), MONTH(fecha_inicio), 1)) AS mes_inicio,
  distrito,
  unidad,
  tipo,
  COUNT(*) AS total_intervenciones,
  SUM(CASE WHEN tiene_acta = 1 THEN 1 ELSE 0 END) AS total_actas,
  SUM(CASE WHEN tiene_denuncia = 1 THEN 1 ELSE 0 END) AS total_denuncias
FROM dbo.intervenciones
GROUP BY DATEFROMPARTS(YEAR(fecha_inicio), MONTH(fecha_inicio), 1), distrito, unidad, tipo;

-- Monthly infringements
SELECT
  CONVERT(date, DATEFROMPARTS(YEAR(fecha), MONTH(fecha), 1)) AS mes_inicio,
  distrito,
  tipologia,
  COUNT(*) AS total_infracciones
FROM dbo.infracciones
GROUP BY DATEFROMPARTS(YEAR(fecha), MONTH(fecha), 1), distrito, tipologia;

-- Monthly HR
SELECT
  CONVERT(date, DATEFROMPARTS(YEAR(fecha), MONTH(fecha), 1)) AS mes_inicio,
  unidad,
  SUM(CASE WHEN estado='operativo' THEN 1 ELSE 0 END) AS efectivos_operativos,
  COUNT(*) AS plantilla_total
FROM dbo.rrhh_hist
GROUP BY DATEFROMPARTS(YEAR(fecha), MONTH(fecha), 1), unidad;
