# The Lost APK

## Scenario

A mobile application was recovered from an abandoned device.

The application appears to be an ordinary utility app, but
something hidden inside the APK may contain sensitive information.

Your task is to inspect the APK and discover the hidden
functionality.

## Objective

1. Obtain the APK.
2. Inspect its Android package structure.
3. Examine the application activities and resources.
4. Identify the hidden `FlagActivity`.
5. Determine how the activity can be triggered.
6. Trigger the hidden activity.
7. Recover the flag.

## Recommended Tools

- JADX
- APKTool
- Android Studio
- ADB
- Android Emulator

## Investigation

Start by examining:

- AndroidManifest.xml
- Activity names
- Exported activities
- Strings
- Resources
- Application logic

The application may contain functionality that is not directly
accessible through its normal interface.

## Flag

Recover the flag displayed by the hidden activity and submit it
through the Cyber Arena submission panel.