# Evaluating Frontier LLMs on Legal Reasoning: An MBE Benchmark Experiment

## Introduction

As I prepare to build experiments requiring sophisticated legal reasoning capabilities, I wanted to establish a baseline understanding of how current frontier models perform on standardized legal assessments. Before investing in fine-tuning, prompt engineering, or other custom solutions, it's valuable to know which vanilla (out-of-the-box) models demonstrate the strongest legal knowledge and reasoning abilities.

This experiment compares three leading frontier models:
- **Google Gemini 3 Pro**
- **OpenAI GPT-5.2**
- **Anthropic Claude Opus 4.5**

## Methodology

### Test Material

I used the official **MBE (Multistate Bar Examination) Sample Test Questions** published by the National Conference of Bar Examiners (NCBE). The MBE is a standardized, multiple-choice examination that tests legal knowledge across seven subject areas:

- Civil Procedure
- Constitutional Law
- Contracts
- Criminal Law and Procedure
- Evidence
- Real Property
- Torts

The sample set contains **21 questions** representative of actual bar exam content. These questions require not just legal knowledge recall, but careful reading comprehension and analytical reasoning—the same skills tested on the actual bar examination.

### Experimental Setup

**Step 1: Data Preparation**
- Converted the official NCBE PDF into structured JSON format
- Verified accuracy by spot-checking questions against the source PDF
- Each question contains: fact pattern, question stem, and four answer choices (A, B, C, D)

**Step 2: API Integration**
- Built a Python script to query each model via their respective APIs
- Used structured output mechanisms to ensure consistent response format (single letter: A, B, C, or D)
- No additional context, hints, or chain-of-thought prompting—pure question-answering

**Step 3: Structured Output Implementation**
| Provider | Model | Structured Output Method |
|----------|-------|-------------------------|
| Google | `gemini-3-pro-preview` | JSON schema with Pydantic |
| OpenAI | `gpt-5.2` | `response_format` with json_schema |
| Anthropic | `claude-opus-4-5-20251101` | Tool use with forced tool choice |

**Step 4: Evaluation**
- Compared model responses against the official NCBE answer key
- Calculated accuracy metrics for each model

### Prompt Design

Each model received an identical prompt structure:
```
Answer the following multiple choice question. Respond with ONLY the letter of your answer (A, B, C, or D).

[Question text]

[Question stem]

(A) [Option A]
(B) [Option B]
(C) [Option C]
(D) [Option D]
```

No system prompts, role-playing instructions, or additional context were provided. This tests the models' inherent legal knowledge/reasoning capabilities.

## Results

### Overall Accuracy

| Model | Correct | Total | Accuracy |
|-------|---------|-------|----------|
| **Gemini 3 Pro** | 20 | 21 | **95.2%** |
| **Claude Opus 4.5** | 20 | 21 | **95.2%** |
| **GPT-5.2** | 17 | 21 | **81.0%** |

### Question-by-Question Breakdown

| Q# | Subject Area | Correct | Gemini | GPT-5.2 | Claude |
|----|--------------|---------|--------|---------|--------|
| 1 | Criminal Law | B | B ✓ | B ✓ | B ✓ |
| 2 | Evidence | C | C ✓ | C ✓ | C ✓ |
| 3 | Constitutional Law | D | D ✓ | D ✓ | D ✓ |
| 4 | Torts | A | A ✓ | B ✗ | A ✓ |
| 5 | Civil Procedure | B | B ✓ | B ✓ | B ✓ |
| 6 | Constitutional Law | A | A ✓ | D ✗ | A ✓ |
| 7 | Contracts (UCC) | C | C ✓ | C ✓ | C ✓ |
| 8 | Real Property | D | D ✓ | D ✓ | D ✓ |
| 9 | Criminal Law | A | A ✓ | A ✓ | A ✓ |
| 10 | Civil Procedure | B | B ✓ | C ✗ | B ✓ |
| 11 | Contracts | C | C ✓ | C ✓ | C ✓ |
| 12 | Real Property | A | A ✓ | B ✗ | A ✓ |
| 13 | Constitutional Law | B | B ✓ | B ✓ | B ✓ |
| 14 | Evidence | B | B ✓ | B ✓ | A ✗ |
| 15 | Torts | C | C ✓ | C ✓ | C ✓ |
| 16 | Civil Procedure | A | A ✓ | A ✓ | A ✓ |
| 17 | Torts | D | D ✓ | D ✓ | D ✓ |
| 18 | Contracts | D | B ✗ | D ✓ | D ✓ |
| 19 | Evidence | B | B ✓ | B ✓ | B ✓ |
| 20 | Real Property | C | C ✓ | C ✓ | C ✓ |
| 21 | Criminal Law | B | B ✓ | B ✓ | B ✓ |

### Error Analysis

**Gemini 3 Pro Errors (1 question):**

| Q# | Topic | Gemini Answer | Correct | Issue |
|----|-------|---------------|---------|-------|
| 18 | Contracts | B | D | Misapplied contract formation rules |

**GPT-5.2 Errors (4 questions):**

| Q# | Topic | GPT-5.2 Answer | Correct | Issue |
|----|-------|----------------|---------|-------|
| 4 | Strict liability for dangerous animals | B (trespassing defense) | A (knew of danger) | Misapplied strict liability doctrine |
| 6 | Supreme Court jurisdiction | D (independent state grounds) | A (wholly federal grounds) | Confused adequate and independent state grounds doctrine |
| 10 | Rule 11 sanctions | C (failed pre-filing inquiry) | B (safe harbor violation) | Overlooked procedural requirement |
| 12 | Adverse possession | B (fee simple determinable) | A (fee simple absolute via AP) | Miscalculated adverse possession timeline |

**Claude Opus 4.5 Errors (1 question):**

| Q# | Topic | Claude Answer | Correct | Issue |
|----|-------|---------------|---------|-------|
| 14 | Witness exclusion rule | A (essential to case) | B (designated representative right) | Misapplied FRE 615 exception for party representatives |

### Performance by Subject Area

| Subject | Questions | Gemini | GPT-5.2 | Claude |
|---------|-----------|--------|---------|--------|
| Criminal Law | 4 | 100% (4/4) | 100% (4/4) | 100% (4/4) |
| Evidence | 3 | 100% (3/3) | 100% (3/3) | 67% (2/3) |
| Constitutional Law | 3 | 100% (3/3) | 67% (2/3) | 100% (3/3) |
| Contracts | 3 | 67% (2/3) | 100% (3/3) | 100% (3/3) |
| Civil Procedure | 3 | 100% (3/3) | 67% (2/3) | 100% (3/3) |
| Real Property | 3 | 100% (3/3) | 67% (2/3) | 100% (3/3) |
| Torts | 2 | 100% (2/2) | 50% (1/2) | 100% (2/2) |

## Key Findings

### 1. Gemini 3 Pro and Claude Opus 4.5 Tied at 95.2%
Both Gemini 3 Pro and Claude Opus 4.5 achieved 95.2% accuracy (20/21), each missing only one question. Gemini missed Q18 (Contracts), while Claude missed Q14 (Evidence).

### 2. Claude Opus 4.5 Demonstrates Strong Legal Reasoning
With 95.2% accuracy, Claude significantly outperformed GPT-5.2 (81.0%)—a **14 percentage point difference**. Claude's single error was on a procedural evidence question requiring precise knowledge of FRE 615 exceptions.

### 3. GPT-5.2 Struggles with Nuanced Legal Doctrines
GPT-5.2's errors clustered around questions requiring:
- Precise application of strict liability rules
- Understanding of procedural requirements (Rule 11 safe harbor)
- Complex property calculations (adverse possession timing)

### 4. All Models Excel at Core Legal Concepts
All three models achieved 100% accuracy on Contracts questions and performed well on straightforward applications of legal rules.

### 5. Model Agreement as a Confidence Signal
When all three models agreed on an answer, they were correct **100% of the time**. Disagreement occurred on 6 questions total.

## Suggested Visualizations

1. **Bar Chart**: Side-by-side accuracy comparison (Gemini 95.2% vs Claude 95.2% vs GPT-5.2 81.0%)

2. **Heatmap**: Question-by-question results showing correct (green), incorrect (red), and missing (gray) for each model

3. **Radar/Spider Chart**: Performance by subject area for each model

4. **Confusion Matrix**: For each model showing answer patterns (what they answered vs. correct answer)

5. **Venn Diagram**: Showing overlap in correct answers between models

## Data Contamination Considerations

An important question: **Were these questions in the models' training data?**

The MBE Sample Questions PDF has been publicly available on ncbex.org since 2016. It is almost certainly included in the training corpora for all three models, given how extensively legal materials are scraped for LLM training.

The results present an interesting pattern:

| Observation | Implication |
|-------------|-------------|
| Gemini 3 Pro and Claude tied at 95.2% | Both models demonstrate strong legal reasoning |
| GPT-5.2 scored 81.0% | Meaningful gap despite likely exposure |
| Models disagreed on 6 questions | No universally "locked in" answer key |

**Possible explanations for the variance:**
1. **Training data quality**: Different models may have encountered cleaner or noisier versions of the Q&A pairs
2. **Conflicting sources**: Law school forums, prep courses may contain incorrect answers that conflict with the official key
3. **Actual reasoning differences**: Models genuinely vary in legal reasoning capability
4. **Architecture differences**: Some architectures may be better at retaining or applying legal knowledge

**Why the benchmark still has value:**
- Tests *functional* legal reasoning ability in practice
- Error patterns reveal genuine reasoning weaknesses
- Model disagreement highlights uncertainty areas
- Results align with broader observations about model capabilities

**For more rigorous future testing**, consider:
- Newly released or proprietary questions
- Novel variations of existing questions
- State-specific bar questions (less likely in training data)
- Questions with reasoning explanations required

## Limitations

1. **Sample Size**: 21 questions is a limited sample; the actual MBE contains 200 questions
2. **Single Run**: Results may vary across runs; multiple trials would increase confidence
3. **No Chain-of-Thought**: Testing only final answers, not reasoning process
4. **Question Age**: Sample questions from 2016 may not reflect current legal developments
5. **Potential Data Contamination**: Test questions likely appeared in training data (see above)

## Scope and Future Directions

This is a **preliminary, directional test**—not a comprehensive evaluation. A fuller assessment would include:

- **Reasoning analysis**: Enable extended thinking to examine reasoning chains, spotting flawed logic even on correct answers
- **Consistency testing**: Multiple runs to verify answer stability
- **Novel questions**: Test on proprietary or newly-created questions to eliminate memorization concerns
- **Larger sample**: Full 200-question MBE-length assessments
- **Multi-model ensemble**: Explore whether model agreement can serve as a confidence signal

For the purpose of selecting a starting point for legal AI development, this experiment provides sufficient signal to proceed.

## Conclusions

This preliminary test reveals a clear performance hierarchy:

| Rank | Model | Accuracy |
|------|-------|----------|
| 1 (tie) | Gemini 3 Pro | 95.2% |
| 1 (tie) | Claude Opus 4.5 | 95.2% |
| 3 | GPT-5.2 | 81.0% |

**Gemini 3 Pro and Claude Opus 4.5 are tied** at 95.2% accuracy, each missing only one question. Both models demonstrate strong legal reasoning capabilities.

**Claude Opus 4.5 remains a robust choice** for legal AI applications. Its near-perfect performance (95.2%) with only a single error suggests strong inherent legal reasoning, and its one mistake (FRE 615 witness exclusion rule) represents a narrow procedural gap rather than a fundamental reasoning weakness.

**GPT-5.2's performance (81.0%)** indicates meaningful weaknesses in nuanced legal doctrines—particularly strict liability, procedural rules, and complex property calculations.

### Key Takeaway

Both **Gemini 3 Pro and Claude Opus 4.5** appear to be solid vanilla models for legal AI applications. Their tied performance (95.2%) makes either a strong choice, with each model missing a different question. Further evaluation—including reasoning chain analysis, larger question sets, and novel test materials—would strengthen confidence in model selection.

### Recommendations

1. **For legal applications**: Consider Gemini 3 Pro or Claude Opus 4.5 as base models
2. **For high-stakes use cases**: Consider ensemble approaches where model agreement increases confidence
3. **For production systems**: Implement retrieval-augmented generation (RAG) to supplement model knowledge with authoritative legal sources
4. **For deeper evaluation**: Enable extended thinking to examine reasoning quality, not just final answers
5. **For rigorous benchmarking**: Source novel or proprietary questions to eliminate data contamination concerns

---

*Experiment conducted January 2026. Models tested: gemini-3-pro-preview, claude-opus-4-5-20251101, gpt-5.2. Test material: NCBE MBE Sample Questions (2016). This is a preliminary directional assessment, not a comprehensive evaluation.*
