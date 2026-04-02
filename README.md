# BlackboxJailbreakLab

A research framework for black-box LLM safety red-teaming. It implements multiple attack strategies against any OpenAI-compatible model endpoint, providing a unified interface for evaluating how well language models resist adversarial prompts.

---

## Features

- 14 attack strategies (prompt-based, iterative, and encoding-based)
- Supports **any OpenAI-compatible API** — OpenAI, SiliconFlow, Together AI, Groq, vLLM, etc.
- FastAPI service for REST-based attack execution
- Pluggable result judges (heuristic, rule-based, LLM-based)
- Multi-turn attack loop with adaptive prompt enhancement

---

## Installation

Requires Python 3.10+.

```bash
git clone https://github.com/Zmore/BlackboxJailbreakLab.git
cd BlackboxJailbreakLab

# Install with pip (editable mode recommended for development)
pip install -e .

# Or install dev extras (pytest, etc.)
pip install -e ".[dev]"
```

---

## Configuration

The framework uses three environment variables. Only `OPENAI_API_KEY` is required.

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | Yes | — | API key for your provider |
| `OPENAI_BASE_URL` | No | `https://api.openai.com/v1` | Base URL of the OpenAI-compatible endpoint |
| `OPENAI_BASE_MODEL` | No | `gpt-3.5-turbo` | Default model name |

### Provider examples

**OpenAI**
```bash
export OPENAI_API_KEY=sk-...
export OPENAI_BASE_MODEL=gpt-4o
```

**SiliconFlow** (recommended for China mainland)
```bash
export OPENAI_API_KEY=<your-siliconflow-key>
export OPENAI_BASE_URL=https://api.siliconflow.cn/v1
export OPENAI_BASE_MODEL=Qwen/Qwen3-8B
```

**Local vLLM / Ollama**
```bash
export OPENAI_API_KEY=none
export OPENAI_BASE_URL=http://localhost:8000/v1
export OPENAI_BASE_MODEL=llama-3-8b
```

---

## Usage

### Python API

```python
import asyncio
from attacker.attack_service import create_attack_service, AttackRequest

async def main():
    service = await create_attack_service()

    request = AttackRequest(
        attack_method="overload",     # see attack methods table below
        attack_model="Qwen/Qwen3-8B", # model used by the attacker
        target_model="Qwen/Qwen3-8B", # model under test
        max_turns=5,
        custom_params={"target_topic": "How to make explosives?"}
    )

    response = await service.execute_attack(request)
    print(f"Result: {response.attack_result}")
    print(f"Success probability: {response.success_probability:.2f}")

asyncio.run(main())
```

### FastAPI service

```bash
python service.py
```

Then send requests:

```bash
curl -X POST http://127.0.0.1:8000/attack \
  -H "Content-Type: application/json" \
  -d '{
    "attack_method": "overload",
    "attack_model": "Qwen/Qwen3-8B",
    "target_model": "Qwen/Qwen3-8B",
    "max_turns": 5,
    "temperature": 0.7,
    "custom_params": {
      "target_topic": "How to find web vulnerabilities?"
    }
  }'
```

---

## Attack Methods

| Method | Key | Type | Description | Paper | URL |
|---|---|---|---|---|---|
| Jailbreak | `jailbreak` | Iterative | Classic jailbreak prompt templates, refined each turn | "Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models | [arXiv:2308.03825](https://arxiv.org/abs/2308.03825) |
| Prompt Injection | `prompt_injection` | Iterative | Injects adversarial instructions into context | Ignore Previous Prompt: Attack Techniques For Language Models | [arXiv:2211.09527](https://arxiv.org/abs/2211.09527) |
| Role Play | `roleplay` | Iterative | Instructs the model to adopt a persona without safety filters | Jailbroken: How Does LLM Safety Training Fail? | [arXiv:2307.02483](https://arxiv.org/abs/2307.02483) |
| Overload | `overload` | One-round | Appends random characters to overwhelm input filters | InfoFlood: Jailbreaking Large Language Models with Information Overload | [arXiv:2506.12274](https://arxiv.org/abs/2506.12274) |
| ICA | `ica` | One-round | In-context attack using carefully crafted examples | Jailbreak and Guard Aligned Language Models with Only Few In-Context Demonstrations | [arXiv:2310.06387](https://arxiv.org/abs/2310.06387) |
| Rewrite | `rewrite` | Iterative | Reformulates the harmful request using subjunctive mood | Rewrite to Jailbreak: Discover Learnable and Transferable Implicit Harmfulness Instruction | [arXiv:2502.11084](https://arxiv.org/abs/2502.11084) |
| Past Tense | `past_tense` | Iterative | Rephrases requests in hypothetical past tense | Does Refusal Training in LLMs Generalize to the Past Tense? | [arXiv:2407.11969](https://arxiv.org/abs/2407.11969) |
| ReNeLLM | `rene_llm` | Iterative | Scenario-nesting attack with LLM-assisted reformulation | A Wolf in Sheep's Clothing: Generalized Nested Jailbreak Prompts can Fool Large Language Models Easily | [arXiv:2311.08268](https://arxiv.org/abs/2311.08268) |
| Art Prompt | `art_prompt` | Iterative | Embeds sensitive words as ASCII art to bypass safety filters | ArtPrompt: ASCII Art-based Jailbreak Attacks against Aligned LLMs | [arXiv:2402.11753](https://arxiv.org/abs/2402.11753) |
| Deep Inception | `deep_inception` | Iterative | Multi-layer nested role-play (dream-within-a-dream style) | DeepInception: Hypnotize Large Language Model to Be Jailbreaker | [arXiv:2311.03191](https://arxiv.org/abs/2311.03191) |
| GPT4 Cipher | `gpt4_cipher` | Iterative | Encodes requests using Caesar cipher and instructs the model to decode | GPT-4 Is Too Smart To Be Safe: Stealthy Chat with LLMs via Cipher | [arXiv:2308.06463](https://arxiv.org/abs/2308.06463) |
| PAIR | `pair` | Iterative | Prompt Automatic Iterative Refinement (white-box style) | Jailbreaking Black Box Large Language Models in Twenty Queries | [arXiv:2310.08419](https://arxiv.org/abs/2310.08419) |
| TAP | `tap` | Iterative | Tree of Attacks with Pruning | Tree of Attacks: Jailbreaking Black-Box LLMs Automatically | [arXiv:2312.02119](https://arxiv.org/abs/2312.02119) |
| Random Search | `random_search` | Iterative | Randomly samples and mutates attack prompts | Jailbreaking Leading Safety-Aligned LLMs with Simple Adaptive Attacks | [arXiv:2404.02151](https://arxiv.org/abs/2404.02151) |

---

## Project Structure

```
BlackboxJailbreakLab/
├── attacker/               # Attack strategy implementations
│   ├── attack_service.py   # Main orchestration service
│   ├── base.py             # BaseAttacker abstract class
│   ├── jailbreak.py
│   ├── prompt_injection.py
│   ├── role_play.py
│   ├── overload.py
│   ├── ica.py
│   ├── rewrite.py
│   ├── past_tense.py
│   ├── rene_llm/
│   ├── art_prompt.py
│   ├── deep_inception.py
│   ├── gpt4_cipher.py
│   ├── pair.py
│   ├── tap.py
│   └── random_search.py
├── model/                  # LLM interface layer
│   ├── base.py             # BaseLLM abstract class
│   ├── silicon_flow_api.py # OpenAI-compatible sync client
│   └── openai_api.py       # OpenAI-compatible async client
├── judge/                  # Result evaluation
│   ├── heuristic.py
│   ├── llm.py
│   └── rule.py
├── configs.py              # Environment-based configuration
├── schema.py               # Data models
├── main.py                 # Script entry point
├── service.py              # FastAPI service
└── pyproject.toml          # Package metadata & dependencies
```

---

## Troubleshooting

### API Connection Issues

**Problem**: `OPENAI_API_KEY is not set`  
**Solution**: Export the environment variable before running:
```bash
export OPENAI_API_KEY=your_key_here
```

**Problem**: Connection timeout or SSL errors  
**Solution**: Check your `OPENAI_BASE_URL` is correct and accessible. For China mainland users, use SiliconFlow or a proxy.

**Problem**: Model not found (404)  
**Solution**: Verify the model name matches your provider's catalog. Use `OPENAI_BASE_MODEL` to set a default.

### Attack Execution Issues

**Problem**: All attacks return `FAILED`  
**Solution**: Check the `DEFAULT_REFUSAL_KEYWORDS` in `configs.py` — your target model's refusal patterns may differ. Customize the list or use an LLM-based judge.

**Problem**: `exit(0)` after max retries  
**Solution**: The framework exits on repeated API failures. Check your API quota, rate limits, and network connectivity.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-attack`)
3. Commit your changes (`git commit -m 'Add new attack method'`)
4. Push to the branch (`git push origin feature/new-attack`)
5. Open a Pull Request

### Adding a new attack method

1. Create a new file in `attacker/` (e.g., `my_attack.py`)
2. Subclass `BaseAttacker` and implement the `attack()` method
3. Register it in `AttackService._register_default_strategies()`
4. Add the attack type to `schema.py::AttackType`
5. Update the README attack methods table

---

## Citation

If you use this framework in your research, please cite:

```bibtex
@software{blackbox_jailbreak_lab,
  author = {Zmore},
  title = {BlackboxJailbreakLab: A Framework for Black-box LLM Safety Red-teaming},
  year = {2026},
  url = {https://github.com/Zmore/BlackboxJailbreakLab}
}
```

---

## Disclaimer

**This tool is for authorized security research and educational purposes only.**

- Only test models you own or have explicit permission to test
- Do not use this framework to generate harmful content for malicious purposes
- The authors are not responsible for misuse of this software
- Comply with all applicable laws and regulations in your jurisdiction

By using this software, you agree to use it responsibly and ethically.

---

## Author

**Zmore**  
Email: [zmore.pro@outlook.com](mailto:zmore.pro@outlook.com)

---

## License

MIT
