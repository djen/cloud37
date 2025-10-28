# What is Overfitting? (Intuitive ML)
- Quelle: https://www.youtube.com/watch?v=wCEgUfWVLrI
- Hinweis: **Beispielausgabe** zur Demo des Tools (Timestamps & Zitate annähernd / exemplarisch).

## TL;DR (3–5 Bullet Points)
- Overfitting = Modell lernt Trainingsdaten **zu spezifisch** → schwache Generalisierung.
- Frühe Warnzeichen: Training-Fehler ↓, Val/Test-Fehler ↑ (Generalization Gap).
- Hauptursachen: zu komplexes Modell, zu wenig/unausgewogene Daten, Daten-Leakage.
- Gegenmittel: Regularisierung, Early Stopping, Data Augmentation, Cross‑Validation.
- Ziel: **Bias–Variance-Balance** für robuste Vorhersagen.

## Kernaussagen
- Overfitting tritt auf, wenn das Modell Muster **memorisiert** statt zu **verallgemeinern**.
- Der **Validierungsfehler** ist entscheidend – nur Training Accuracy ist irreführend.
- **Komplexitätskontrolle** (Regularisierung, Dropout, kleinere Modelle) reduziert Varianz.
- **Mehr und bessere Daten** (saubere Splits, Augmentation) sind oft der größte Hebel.
- Eine solide **Evaluationsstrategie** (Hold-out, k‑Fold, Stratifizierung) verhindert Selbsttäuschung.

## Struktur / Outline
1. Begriffsklärung Overfitting vs. Generalisierung
2. Sichtbare Symptome im Lernkurven‑Verlauf
3. Typische Ursachen und Beispiele
4. Praktische Gegenmaßnahmen
5. Kurzes Fazit: Balance statt Maximalfit

## Zitate mit Zeitstempel
- [00:15] „Overfitting bedeutet, dass dein Modell die Trainingsdaten **auswendig** lernt.“
- [01:02] „Schau immer auf den **Validierungsfehler**, nicht nur auf die Trainingsgenauigkeit.“
- [02:05] „Regularisierung ist ein Werkzeug, um unnötige Komplexität zu zügeln.“
- [02:40] „Mehr Daten – besonders **repräsentative** – helfen fast immer.“
- [03:10] „Gute Splits und Cross‑Validation sparen dir peinliche Überraschungen im Test.“

## Glossar (Begriffe → Kurzdefinition)
- **Generalization Gap**: Differenz zwischen Trainings‑ und Validierungsleistung.
- **Regularisierung**: Strafen (z. B. L1/L2), die große Gewichte/Komplexität eindämmen.
- **Early Stopping**: Training stoppen, sobald Val‑Fehler nicht weiter sinkt.
- **Data Leakage**: Informationen aus Validierung/Test landen versehentlich im Training.
- **k‑Fold CV**: Mehrfache, rotierende Validierung zur robusten Schätzung der Performance.

## Offene Fragen / Weiteres Nachforschen
- Wie wählt man die **richtige** Regularisierungsstärke systematisch?
- Welche **Daten‑Augmentationen** wirken bei Tabulardaten vs. Bildern/Text?
- Wie erkenne ich **Leckagen** in komplexen Feature‑Pipelines (Zeitreihen, Gruppen‑Leakage)?

## Weiterführende Links
- Bias–Variance Trade-off (erläuternder Artikel/Video)
- Checklisten zur Vermeidung von Data Leakage
- Leitfäden zu Lernkurvenanalyse & Early Stopping