# Python Package Distribution Guidelines: gemini-cli-mcp

This document provides a step-by-step guide for maintainers to properly package, test, and publish the `gemini-cli-mcp` Python package to PyPI.

---

## 1. Versioning
- Follow [Semantic Versioning](https://semver.org/): MAJOR.MINOR.PATCH (e.g., 1.2.3)
- **Always increment the version** in `pyproject.toml` before each release. PyPI does not allow re-uploading the same version.

---

## 2. Packaging Setup
- Ensure `pyproject.toml` contains all required metadata:
  - `name`, `version`, `description`, `readme`, `authors`, `license`, `dependencies`, `requires-python`, etc.
- Define entry points for CLI tools in `[project.scripts]`.
- Remove any sensitive or local information from metadata.

---

## 3. Building the Package

### Install build tools (if needed):
```bash
pip install build
```

### Build source and wheel distributions:
```bash
python -m build
```
- This creates `.tar.gz` and `.whl` files in the `dist/` directory.

---

## 4. Checking the Distribution

### Install twine (if needed):
```bash
pip install twine
```

### Check the built distributions for errors:
```bash
twine check dist/*
```
- Ensure all checks pass before uploading.

---

## 5. Test Upload to TestPyPI (Recommended)
- [TestPyPI](https://test.pypi.org/) is a sandbox for testing uploads.

### Upload to TestPyPI:
```bash
twine upload --repository testpypi dist/*
```
- Use your TestPyPI API token for authentication.

### Test installation from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ gemini-cli-mcp
```
- Verify CLI entry points and package functionality.

---

## 6. Upload to PyPI (Production)
- Ensure you have a valid [PyPI API token](https://pypi.org/manage/account/#api-tokens).

### Upload to PyPI:
```bash
twine upload dist/*
```
- Use your PyPI API token for authentication.

### Test installation from PyPI:
```bash
pip install --upgrade gemini-cli-mcp
```
- Verify CLI entry points and package functionality.

---

## 7. API Token Security
- **Never commit API tokens or credentials to version control.**
- Use environment variables or `.pypirc` for authentication.
- Example `.pypirc`:
  ```ini
  [pypi]
  username = __token__
  password = pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
  [testpypi]
  repository = https://test.pypi.org/legacy/
  username = __token__
  password = pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
  ```

---

## 8. Release Notes & Changelog
- Update `CHANGELOG.md` or release notes for each new version.
- Summarize new features, bug fixes, and breaking changes.

---

## 9. Best Practices
- Test in a clean virtual environment before release.
- Use absolute paths for CLI entry points in documentation/examples.
- Remove any local or sensitive data from package files.
- Tag releases in version control (e.g., `git tag v1.2.3`).
- Announce new releases to users if appropriate.

---

## 10. References
- [PyPI Packaging Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [TestPyPI](https://test.pypi.org/)
- [Twine Documentation](https://twine.readthedocs.io/en/stable/)
- [PEP 621: pyproject.toml](https://peps.python.org/pep-0621/)
- [Semantic Versioning](https://semver.org/) 

---

# Smithery 배포 가이드

이 문서는 Python MCP 서버를 smithery에 배포하는 절차를 안내합니다.

## 1. 사전 준비
- Dockerfile, smithery.yaml, 코드가 server_py 디렉토리에 준비되어 있어야 합니다.
- smithery.yaml의 configSchema는 geminiApiKey를 요구하도록 작성되어야 합니다.

## 2. smithery.yaml 예시
```yaml
runtime: "container"
build:
  dockerfile: "Dockerfile"
  dockerBuildPath: "."
startCommand:
  type: "http"
  configSchema:
    type: "object"
    properties:
      geminiApiKey:
        type: "string"
        description: "Your Gemini API key"
    required: ["geminiApiKey"]
  exampleConfig:
    geminiApiKey: "gemini-api-key"
```

## 3. 배포 절차
1. 모든 변경사항을 GitHub 저장소에 push합니다.
2. smithery 웹사이트에서 GitHub 저장소를 연결하거나, 이미 등록된 서버라면 claim합니다.
3. smithery 서버 페이지의 Deployments 탭으로 이동합니다.
4. "Deploy" 버튼을 클릭하여 서버를 빌드 및 배포합니다.

## 4. 배포 후 검증
- smithery에서 MCP 서버가 검색되고, geminiApiKey를 입력하여 정상적으로 동작하는지 확인합니다.
- `/mcp` 엔드포인트가 GET, POST, DELETE를 지원하는지 테스트합니다.

## 참고
- 공식 문서: https://smithery.ai/docs/build/deployments 