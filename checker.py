import argparse
import json
import re
from pathlib import Path

FALLBACK_FACTUAL_KEYWORDS = {
    "claims": [
        "reported",
        "according to",
        "studies",
        "research",
        "survey",
        "experts",
        "evidence",
        "data",
        "claimed",
    ],
    "contradictions": [
        "never",
        "always",
        "impossible",
        "cannot",
        "can't",
        "won't",
        "must",
        "should",
    ],
}


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def sentence_tokens(text: str) -> list[str]:
    text = normalize_text(text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def score_sentence(sentence: str) -> dict[str, object]:
    lower = sentence.lower()
    tokens = sentence_tokens(sentence)
    score = 1.0
    reasons: list[str] = []

    if any(keyword in lower for keyword in FALLBACK_FACTUAL_KEYWORDS["claims"]):
        score -= 0.25
        reasons.append("Contains claim language")

    if any(keyword in lower for keyword in FALLBACK_FACTUAL_KEYWORDS["contradictions"]):
        score -= 0.2
        reasons.append("Contains absolute/contradictory modality")

    if sentence.count("?"):
        score -= 0.1
        reasons.append("Question-like phrasing")

    if len(sentence) > 220:
        score -= 0.15
        reasons.append("Long sentence with potential uncertainty")

    score = max(0.0, min(1.0, score))
    return {
        "text": sentence,
        "score": round(score, 2),
        "reasons": reasons,
    }


def analyze_text(text: str) -> dict[str, object]:
    sentences = sentence_tokens(text)
    return {
        "sentence_count": len(sentences),
        "sentences": [score_sentence(sentence) for sentence in sentences],
    }


def load_input(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def save_report(report: dict[str, object], path: Path) -> None:
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Hallucination Checker")
    parser.add_argument("--input", "-i", required=True, help="Input text file path")
    parser.add_argument("--output", "-o", default="report.json", help="Output JSON report path")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    text = load_input(input_path)
    report = analyze_text(text)
    save_report(report, Path(args.output))
    print(f"Report saved to {args.output}")


if __name__ == "__main__":
    main()
