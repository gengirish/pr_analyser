@echo off
REM Set Permanent GitHub Token for Windows
REM This batch file sets the GITHUB_TOKEN environment variable permanently for the user

echo Setting up permanent GitHub token for Windows...

REM Check if a GitHub token was provided
if "%1"=="" (
    echo Error: No GitHub token provided.
    echo Usage: set_permanent_token_windows.bat your_github_token_here
    exit /b 1
)

REM Set the GITHUB_TOKEN environment variable permanently for the user
setx GITHUB_TOKEN %1
echo Set GITHUB_TOKEN environment variable permanently.
echo.
echo Important: You need to open a new command prompt for the change to take effect.
echo.
echo To verify the token is set, open a new command prompt and run:
echo echo %%GITHUB_TOKEN%%
echo.
echo To use the token immediately in the current session, also run:
echo set GITHUB_TOKEN=%1
