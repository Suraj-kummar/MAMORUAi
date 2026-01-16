# Contributing to MamoruAI

Thank you for your interest in contributing to MamoruAI! We welcome contributions from the community to help make Web3 security more accessible and robust.

## 🌟 How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Environment details (OS, Node version, Docker version)

### Suggesting Features

We love new ideas! When suggesting a feature:
- Explain the use case
- Describe the proposed solution
- Consider edge cases and security implications

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** following our coding standards
4. **Write tests** for new functionality
5. **Submit a pull request** with a clear description

## 🛠️ Development Setup

```bash
# Fork and clone
git clone https://github.com/yourusername/MamoruAI.git
cd MamoruAI

# Install dependencies
cd frontend && npm install
cd ../engine && pip install -r requirements.txt

# Start development environment
docker-compose up
```

## 📝 Coding Standards

### TypeScript/React
- Use functional components with hooks
- Follow ESLint rules (run `npm run lint`)
- Use TypeScript strict mode
- Prefer named exports over default exports

### Python
- Follow PEP 8 style guide
- Use type hints for function signatures
- Run `black` for code formatting
- Use `mypy` for static type checking

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add support for Base chain scanning
fix: resolve Slither timeout issue
docs: update ARCHITECTURE.md with WebSocket info
test: add unit tests for AI service
```

## 🧪 Testing

```bash
# Frontend tests
cd frontend
npm run test

# Engine tests
cd engine
pytest tests/
```

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Every contribution, no matter how small, helps make Web3 safer. We appreciate your efforts!
