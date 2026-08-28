# Rust Core Guide

This file supplements the repository-level `AGENTS.md` for code under `src/`.

## Module Boundaries

- `main.rs` should stay thin. Most startup and command-mode behavior belongs in `core_main.rs` or library modules.
- `lib.rs` defines the supported module graph. Preserve its mobile, desktop, iOS, and feature gates when exposing new code.
- `client.rs` and `client/` implement the controlling side of a session. `client/io_loop.rs` owns much of the remote-session message loop; `client/file_trait.rs` contains file-manager behavior.
- `server.rs` and `server/` implement the controlled side. Follow `server/AGENTS.md` for host services and incoming connections.
- `rendezvous_mediator.rs` is about server registration and transport establishment, not remote-session UI state.
- `ipc.rs` and `ipc/` connect local processes such as the UI, service, and privileged components.
- `flutter_ffi.rs` is the callable bridge surface; `flutter.rs` owns Rust-side Flutter sessions, streams, callbacks, and rendering integration.
- `ui_session_interface.rs`, `ui_interface.rs`, and `ui_cm_interface.rs` adapt core/session behavior to frontends. Keep business logic in the core when it is not UI-specific.
- `common.rs` contains application-wide initialization and helpers. Avoid turning it into a default home for unrelated code.
- `hbbs_http/` handles account, download, record upload, and other HTTP-facing operations.
- `privacy_mode/`, `whiteboard/`, and `plugin/` are separate subsystems; keep their platform and feature gates intact.
- `ui/` is the deprecated Sciter frontend.

## Change Tracing

Before changing a session message or option, trace both sides:

1. Find the protobuf/config definition in `libs/hbb_common`.
2. Find send and receive sites in both `client` and `server/connection.rs`.
3. Check whether the value crosses IPC or Flutter FFI.
4. Check desktop/mobile and relevant platform gates.

For a new Flutter-callable API, edit `flutter_ffi.rs`, regenerate bridge outputs, then update the Dart caller. For asynchronous Rust-to-Dart events, also inspect the stream registration and event decoding in `flutter.rs` and `flutter/lib/models/`.

## Concurrency and State

- The core mixes Tokio synchronization with standard `Mutex`/`RwLock` for synchronous shared state. Confirm which one is in use before adding awaits or callbacks.
- Copy or extract the minimum state needed, release the guard, and only then `.await` or invoke code that may re-enter the subsystem.
- Long-lived session loops should have an explicit shutdown path. Preserve channel-close, connection-close, and service-stop behavior together.
- Avoid unbounded background tasks without ownership or cancellation tied to a session/service lifecycle.

## Verification

- Use `cargo fmt --all -- --check` after Rust edits.
- Prefer a focused unit test near the changed module and a targeted `cargo test`/`cargo check` command.
- Changes behind an OS `cfg` require either a check on that OS/target or a clear note that the target-specific path was not executable locally.
- FFI changes also require `flutter analyze` after bridge regeneration and Dart updates.
