# Platform Layer Guide

This directory provides desktop OS implementations exported through `mod.rs`. Keep common call sites platform-neutral and contain OS details here when practical.

## Platform Map

- `windows.rs`, `windows.cc`, `win_device.rs`, `windows/`: Windows services, sessions, devices, privileges, display/input, and native APIs.
- `macos.rs`, `macos.mm`, `privileges_scripts/`: macOS APIs, Objective-C++ glue, permissions, launch agents/daemons, and privileged operations.
- `linux.rs`, `linux_desktop_manager.rs`, `gtk_sudo.rs`, `delegate.rs`: Linux display/session detection, desktop management, privilege UI, and delegated operations.
- `mod.rs`: conditional exports and shared platform-facing types/helpers.

## Editing Rules

- Keep `#[cfg]` conditions aligned between declarations, imports, exports, dependencies, and callers.
- Do not make an OS-specific type leak into code compiled for other targets. Use a common wrapper or gate the entire call path.
- Match ownership and allocation rules across Rust/C++/Objective-C++ FFI. Document who allocates, frees, and owns callbacks or handles.
- Release native handles and restore changed system state on error and shutdown paths.
- Treat privilege escalation, service installation, credentials, input injection, screen capture, and privacy mode as security-sensitive.
- Linux behavior may differ across X11, Wayland, headless sessions, and display managers. Check the relevant runtime branch rather than assuming one Linux desktop model.
- Preserve the unaffected platforms; avoid speculative edits to a platform path that cannot be validated.

## Verification

Run the narrow Rust check available for the target and inspect every changed `cfg` branch. Native glue changes require the corresponding platform build; if that is unavailable, state exactly which compilation/runtime path remains unverified.
