# GitHub Setup Guide

This guide will help you set up the GoTo Connect Authentication Library for development and contribution.

## 🚀 Quick Setup for Users

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/gotoconnect-auth.git
cd gotoconnect-auth
```

### 2. Install Dependencies

```bash
# Install the library and dependencies
python install.py

# Or manually:
pip install -e .
```

### 3. Configure Your Credentials

Create a `.env` file in the project root:

```env
GOTO_CLIENT_ID=YOUR_CLIENT_ID_HERE
GOTO_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
GOTO_REDIRECT_URI=http://localhost:8080/callback
```

### 4. Test the Installation

```bash
# Run the basic example
python examples/basic_usage.py

# Run tests
python -m pytest tests/ -v
```

## 🛠️ Development Setup

### 1. Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/gotoconnect-auth.git
cd gotoconnect-auth
```

### 2. Set Up Development Environment

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install additional development tools
pip install black flake8 mypy
```

### 3. Configure Pre-commit Hooks (Optional)

```bash
# Install pre-commit
pip install pre-commit

# Install the git hook scripts
pre-commit install
```

### 4. Set Up Your Credentials

Create a `.env` file for testing:

```env
GOTO_CLIENT_ID=YOUR_CLIENT_ID_HERE
GOTO_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
GOTO_REDIRECT_URI=http://localhost:8080/callback
```

**Important**: Never commit your `.env` file with real credentials!

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=gotoconnect_auth --cov-report=html

# Run specific test file
python -m pytest tests/test_auth.py -v

# Run with verbose output
python -m pytest tests/ -v -s
```

## 📝 Code Quality

### Linting and Formatting

```bash
# Format code with black
black gotoconnect_auth/ tests/ examples/

# Check code style with flake8
flake8 gotoconnect_auth/ tests/ examples/

# Type checking with mypy
mypy gotoconnect_auth/
```

### Pre-commit Checks

If you installed pre-commit hooks, they will run automatically on commit. Otherwise, run manually:

```bash
pre-commit run --all-files
```

## 🔧 Making Changes

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write your code
- Add tests for new functionality
- Update documentation if needed

### 3. Test Your Changes

```bash
# Run the test suite
python -m pytest tests/ -v

# Run the examples
python examples/basic_usage.py
python examples/meeting_manager.py

# Check code quality
black gotoconnect_auth/ tests/ examples/
flake8 gotoconnect_auth/ tests/ examples/
mypy gotoconnect_auth/
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "Add feature: description of your changes"
```

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Code follows the project's style guidelines
- [ ] All tests pass
- [ ] New functionality has tests
- [ ] Documentation is updated
- [ ] No sensitive information is included

### Pull Request Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Test improvement

## Testing
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Examples still work

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No sensitive data included
```

## 🐛 Issue Reporting

When reporting issues, please include:

1. **Environment**: Python version, OS, library version
2. **Steps to reproduce**: Clear, step-by-step instructions
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Error messages**: Full error traceback if applicable
6. **Configuration**: How you're configuring the library (env vars, config file, etc.)

## 🔒 Security

### Never Commit Sensitive Information

- ✅ `.env` files with real credentials
- ✅ `config.json` files with real credentials
- ✅ API keys or secrets
- ✅ Personal information

### Safe to Commit

- ✅ Example configuration files with placeholders
- ✅ Test credentials (if clearly marked as test data)
- ✅ Documentation and examples

## 📚 Additional Resources

- [GoTo Connect Developer Portal](https://developer.goto.com/)
- [GoTo Connect API Documentation](https://developer.goto.com/api-docs)
- [Python OAuth 2.0 Guide](https://requests-oauthlib.readthedocs.io/)
- [Python Testing Best Practices](https://docs.pytest.org/)

## 🆘 Getting Help

- 📖 Check the [README.md](README.md) for basic usage
- 🐛 Open an issue for bugs or problems
- 💬 Start a discussion for questions
- 📧 Contact maintainers for urgent issues 