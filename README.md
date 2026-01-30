# MBE Legal Reasoning Benchmark

Evaluating frontier LLM models on official MBE (Multistate Bar Examination) sample questions.

> **Note:** This is a very small sample test (21 questions). Take the results with a grain of salt. See [EXPERIMENT_WRITEUP.md](EXPERIMENT_WRITEUP.md) for limitations and data contamination considerations.

## Results

| Model | Accuracy | Notes |
|-------|----------|-------|
| Gemini 3 Pro | 100% (21/21) | Perfect score |
| Claude Opus 4.5 | 95.2% (20/21) | 1 mistake |
| GPT-5.2 | 76.2% (16/21) | 5 mistakes |

See [EXPERIMENT_WRITEUP.md](EXPERIMENT_WRITEUP.md) for detailed analysis.

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and add your API keys:
   ```bash
   cp .env.example .env
   ```

## Usage

```bash
python mbe_api_test.py
```

The script queries all three models on 21 MBE questions and compares responses against the official answer key.

## Files

- `mbe_api_test.py` - Main test script
- `mbe_sample_questions.json` - 21 official NCBE sample questions
- `MBE Sample Test Questions.pdf` - Original NCBE PDF with answer key (page 6)
- `EXPERIMENT_WRITEUP.md` - Detailed methodology and analysis

## Models Tested

- **Gemini 3 Pro** (`gemini-3-pro-preview`) - JSON schema structured output
- **GPT-5.2** (`gpt-5.2`) - JSON schema structured output
- **Claude Opus 4.5** (`claude-opus-4-5-20251101`) - Tool-based structured output

## Personal Impression

I've been obsessed with Opus 4.5 and considered it quite a superior model for my daily research tasks. These results suggest Gemini 3 Pro deserves a closer look.
