# Contributing to BlackboxJailbreakLab

Thank you for your interest in contributing to BlackboxJailbreakLab! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and constructive in all interactions
- This tool is for authorized security research only
- Do not share or promote malicious use cases

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (Python version, OS, provider)
- Relevant logs or error messages

### Suggesting Features

Feature requests are welcome! Please include:
- Clear description of the feature
- Use case and motivation
- Proposed implementation approach (if applicable)

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/Zmore/BlackboxJailbreakLab.git
   cd BlackboxJailbreakLab
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests if applicable
   - Update documentation as needed

4. **Test your changes**
   ```bash
   # Install dev dependencies
   pip install -e ".[dev]"
   
   # Run tests (if available)
   pytest
   
   # Test manually
   python main.py
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: Add new attack method XYZ"
   ```
   
   Use conventional commit messages:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `refactor:` Code refactoring
   - `test:` Adding tests
   - `chore:` Maintenance tasks

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a Pull Request on GitHub.

## Adding a New Attack Method

To add a new attack strategy:

1. **Create the attacker file**
   ```python
   # attacker/my_attack.py
   from attacker.base import BaseAttacker, BaseAttackerConfig
   from dataclasses import dataclass
   
   @dataclass
   class MyAttackConfig(BaseAttackerConfig):
       # Add custom config fields
       pass
   
   class MyAttacker(BaseAttacker):
       def attack(self, messages, **kwargs):
           # Implement your attack logic
           # Return modified messages
           pass
   ```

2. **Register in AttackService**
   ```python
   # attacker/attack_service.py
   from attacker.my_attack import MyAttacker, MyAttackConfig
   
   # In _register_default_strategies():
   my_attack_config = MyAttackConfig(
       attacker_cls="MyAttacker",
       attacker_name="my_attack",
       attack_type=AttackType.MY_ATTACK
   )
   self.attack_strategies["my_attack"] = MyAttacker(my_attack_config)
   ```

3. **Add attack type**
   ```python
   # schema.py
   class AttackType(Enum):
       MY_ATTACK = "black_box"  # or "white_box"
   ```

4. **Update documentation**
   - Add entry to README.md attack methods table
   - Document any special requirements or parameters

## Code Style

- Follow PEP 8
- Use type hints where possible
- Write docstrings for public functions/classes
- Keep functions focused and concise
- Use English for all comments and documentation

## Testing

- Test with multiple providers (OpenAI, SiliconFlow, local models)
- Verify error handling for API failures
- Check edge cases (empty messages, max turns, etc.)

## Documentation

- Update README.md for user-facing changes
- Add docstrings for new functions/classes
- Include usage examples for new features

## Questions?

Feel free to open an issue for questions or reach out to:
- **Zmore**: zmore.pro@outlook.com

Thank you for contributing!
