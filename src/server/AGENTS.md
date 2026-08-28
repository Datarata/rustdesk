# Host Server and Services Guide

This directory implements the controlled/host side of RustDesk sessions. It is security- and concurrency-sensitive because remote messages can cause local display capture, input, clipboard, file, terminal, printer, and system actions.

## Structure

- `connection.rs`: per-connection authentication, authorization, message dispatch, session state, and feature coordination. Treat changes here as cross-cutting.
- `service.rs`: generic publish/subscribe service infrastructure and service lifecycle.
- `video_service.rs`, `video_qos.rs`, `display_service.rs`: capture source selection, frame delivery, display state, and adaptive video behavior.
- `audio_service.rs`: host audio capture and streaming.
- `input_service.rs`: remote input processing; Linux-specific paths also involve `uinput.rs`, `rdp_input.rs`, and `wayland.rs`.
- `clipboard_service.rs`: clipboard synchronization; file clipboard behavior may also involve `src/clipboard.rs`, `src/clipboard_file.rs`, and `libs/clipboard`.
- `terminal_service.rs`, `terminal_helper.rs`: remote terminal sessions and platform support.
- `printer_service.rs`: Windows remote printing behind Flutter/platform gates.
- `portable_service.rs`: Windows portable/elevated service integration.
- `login_failure_check.rs`: login throttling/policy support.
- `dbus.rs`: Linux desktop/session integration.

## Invariants

- Authenticate first and verify the relevant permission before performing any remote-requested action. Do not rely only on UI visibility or client-side checks.
- Preserve connection cleanup: subscriptions, wakelocks, temporary services, child processes, and global connection registries must be released on every exit path.
- Keep protocol handling tolerant of peers on compatible older versions. New fields should normally have safe defaults, and unsupported messages should fail safely.
- Validate remote lengths, paths, indices, identifiers, and enum values before using them locally.
- Do not hold `Server`, connection, session, or service locks across `.await` or callbacks that can re-enter server code.
- A shared service and a per-connection service have different lifetimes. Follow the existing neighboring pattern instead of registering a new service by analogy alone.
- Log operational failures without logging passwords, secrets, authentication material, clipboard contents, or other sensitive payloads.

## Verification

For a service change, exercise its subscribe/start/update/unsubscribe or connection/cleanup sequence. For protocol changes, inspect and test both the send and receive path. Authentication, permission, file path, terminal, or elevation changes need focused negative tests in addition to the successful path.
