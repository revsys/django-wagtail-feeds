import nox

DJANGO_VERSIONS = ["5.2", "6.0", "6.1"]
PYTHON_VERSIONS = ["3.12", "3.13", "3.14", "3.14t", "3.15", "3.15t"]

# Django versions that have no final release yet need a specifier that opts in
# to pre-releases. Naming the pre-release also lets the same spec pick up the
# final release once it ships, so these entries can just be deleted then.
DJANGO_SPECS = {
    "6.1": "django>=6.1rc1,<6.2",
}

# Django 6.1 removed django.utils.cache.cc_delim_re, which Django REST
# Framework still imports. Wagtail pulls DRF in for wagtail.api, so every 6.1
# session fails on import before reaching our code. Drop these once DRF ships a
# 6.1-compatible release (>3.17.1) and Wagtail allows it.
INVALID_PYTHON_DJANGO_SESSIONS = [(python, "6.1") for python in PYTHON_VERSIONS]

nox.options.default_venv_backend = "uv|venv"
nox.options.reuse_existing_virtualenvs = True


@nox.session(python=PYTHON_VERSIONS, tags=["django"], venv_backend="uv")
@nox.parametrize("django", DJANGO_VERSIONS)
def tests(session: nox.Session, django: str) -> None:
    if (session.python, django) in INVALID_PYTHON_DJANGO_SESSIONS:
        session.skip()
    # Editable so pytest collects ./tests against this checkout rather than a
    # second copy installed into site-packages.
    session.install("-e", ".[test]")
    session.install(DJANGO_SPECS.get(django, f"django~={django}"))
    session.run("pytest", *session.posargs)


@nox.session(venv_backend="uv")
def lint(session: nox.Session) -> None:
    session.install(".[lint]")
    session.run("prek", "run", "--all-files", *session.posargs)


@nox.session(venv_backend="uv")
def coverage(session: nox.Session) -> None:
    # Editable, so coverage measures ./wagtail_feeds rather than a copy in
    # site-packages that it would never see reported.
    session.install("-e", ".[test]", "django")
    session.run("pytest", "--cov", "--cov-report=term-missing", *session.posargs)


@nox.session(venv_backend="none")
def tests_env(session: nox.Session) -> None:
    """Run the tests in the active environment, without building a virtualenv."""
    session.run("pytest", *session.posargs)
