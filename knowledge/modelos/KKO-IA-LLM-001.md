---
id: KKO-IA-LLM-001
format_version: 0.1.0
version: 0.1.0
title: "Modelos de lenguaje de gran tamaño (LLM)"
domain: artificial-intelligence
status: draft
created: "2026-10-22"
updated: "2026-10-22"
human_review_required: true
publication_approved: false
audiences: [citizen, professional, technical]
course_lessons: [L05]
book_chapters: [C05]
source_refs:
  - https://arxiv.org/abs/1706.03762
  - https://arxiv.org/abs/2005.14165
  - https://arxiv.org/abs/2108.07258
related_kko:
  - KKO-IA-AGENTES-001
related_kcr: []
---

# Modelos de lenguaje de gran tamaño (LLM)

> **Piloto del paso 14. Estado: borrador no validado.** Este archivo es público como propuesta técnica en una rama de revisión, pero su contenido no está aprobado para publicación editorial ni para despliegue web. Las fuentes son referencias de partida, pendientes de revisión editorial.

## Definición

Un **modelo de lenguaje de gran tamaño** (LLM) es un modelo de aprendizaje automático entrenado con grandes colecciones de texto y, según el sistema, otros datos, para procesar y generar lenguaje. Muchos LLM generativos producen texto prediciendo sucesivamente tokens condicionados por el contexto.

## Explicación para cualquier persona

Un LLM puede redactar, resumir, traducir y ayudar a programar porque aprende regularidades y relaciones complejas durante su entrenamiento. Una respuesta fluida no garantiza que los datos sean ciertos o estén actualizados.

**Ejemplo:** puede explicar un contrato en lenguaje sencillo, pero las cláusulas importantes deben comprobarse en el documento original y, cuando corresponda, por un profesional.

## Funcionamiento básico

`Texto de entrada → tokens → representaciones numéricas → procesamiento del contexto → predicción de tokens → respuesta`

La arquitectura *Transformer* introdujo mecanismos de atención que son fundamentales para muchos LLM modernos. El preentrenamiento, los ajustes posteriores y las herramientas externas pueden modificar cómo se comporta un sistema construido alrededor de un LLM. No todos los modelos comparten exactamente la misma arquitectura ni las mismas capacidades.

## Límites y riesgos

- Puede producir afirmaciones incorrectas o referencias inexistentes.
- Su comportamiento depende de datos, entrenamiento, instrucciones y contexto.
- Puede reproducir sesgos y revelar información si se usa sin controles adecuados.
- La evaluación debe distinguir calidad lingüística, exactitud factual, seguridad y adecuación a la tarea.

## Relación con KosmoTIC

- **KKO:** mantiene la definición y las referencias conceptuales del LLM.
- **KCR:** evalúa capacidades de modelos concretos para misiones; no duplica la definición.
- **Inter-IA:** selecciona y coordina capacidades según evidencia, coste y permisos.
- **PAE / PLAC / HITL:** admisión, límites operativos y revisión humana cuando corresponda.

## Fuentes de referencia

1. Vaswani et al., *Attention Is All You Need* (2017): https://arxiv.org/abs/1706.03762 — arquitectura Transformer.
2. Brown et al., *Language Models are Few-Shot Learners* (2020): https://arxiv.org/abs/2005.14165 — ejemplo de modelado generativo a gran escala.
3. Bommasani et al., *On the Opportunities and Risks of Foundation Models* (2021): https://arxiv.org/abs/2108.07258 — capacidades, riesgos y contexto de los modelos fundacionales.

## Control editorial

- [ ] Verificar fuentes y afirmaciones por revisión humana.
- [ ] Aprobar el KKO para pasar de `draft` a `validated`.
- [ ] Autorizar por separado cualquier representación publicada.

**Alcance de la prueba:** comprobar que el generador existente puede crear una **vista temporal de revisión** a partir de este segundo KKO sin modificar `docs/` ni desplegar una web. Correspondencia editorial provisional: L05 ↔ C05.
