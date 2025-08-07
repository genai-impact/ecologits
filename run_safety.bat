@echo off
call "C:\Documents\Projets de codage\ecologits\ecologits_env\Scripts\activate.bat"
poetry export --without-hashes -f requirements.txt | safety check --stdin