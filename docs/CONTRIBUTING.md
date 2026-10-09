# Contributing to ZPHISHING APEX

## Code of Conduct

Be respectful, inclusive, and professional.

## How to Contribute

### Reporting Bugs

1. Check existing issues
2. Create new issue with:
   - Clear title
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details

### Suggesting Features

1. Check existing feature requests
2. Create new issue with:
   - Clear title
   - Detailed description
   - Use cases
   - Proposed implementation

### Pull Requests

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Update documentation
6. Submit pull request

## Development Setup

```bash
git clone https://github.com/wormshadow/zphishing-apex.git
cd zphishing-apex
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings
- Add comments

## Testing

```bash
pytest tests/
pytest --cov=zphishing tests/
```

## Documentation

- Update README.md
- Add docstrings
- Update API documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
