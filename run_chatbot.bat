@echo off
cd /d "%~dp0"
py ai_rule_based_chatbot.py
if errorlevel 1 (
  echo.
  echo The Python launcher 'py' did not run successfully.
  echo Try this command instead:
  echo python ai_rule_based_chatbot.py
)
pause
