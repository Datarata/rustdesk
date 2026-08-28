# Flutter UI Guide

`flutter/` is the current RustDesk UI for desktop, mobile, and web. It talks to the Rust core through `flutter_rust_bridge` on native targets and through the web bridge on web.

## Application Structure

- `lib/main.dart`: application entry point and desktop launch-mode dispatcher. Desktop may launch the main window, connection manager, installer, or separate remote/file/camera/port-forward/terminal windows.
- `lib/common.dart`: broad shared UI/runtime helpers. Prefer a focused existing module for new logic when one exists.
- `lib/common/`: reusable widgets, shared state, formatting, and account/server helpers.
- `lib/desktop/pages/`: desktop page composition; `desktop/screen/` owns top-level windows/screens; `desktop/widgets/` contains desktop-specific components.
- `lib/mobile/pages/`, `lib/mobile/widgets/`: mobile navigation, sessions, settings, and touch controls.
- `lib/models/`: session and feature state. `model.dart` contains the central `FFI` and core session/rendering models; focused files own server, file, input, peer, terminal, account, and other state.
- `lib/models/platform_model.dart`: conditional native/web selection and the shared `bind` access point.
- `lib/models/native_model.dart`: native `PlatformFFI`, dynamic library/method-channel integration, and event routing.
- `lib/models/web_model.dart`, `lib/web/`: browser bridge and web-specific implementations.
- `lib/utils/`: multi-window, platform-channel, HTTP, image, and scaling helpers.
- `lib/plugin/`: plugin-facing UI and event handling.
- `test/`: Flutter unit/widget tests.

## Rust Boundary

- `../src/flutter_ffi.rs` defines the native bridge API.
- `../src/flutter.rs` owns Rust-side sessions and Rust-to-Dart event streams.
- `lib/generated_bridge*` is generated and may be absent until bridge generation; never edit it manually.
- Regenerate with the pinned `flutter_rust_bridge_codegen` flow in `run.sh` or `../.github/workflows/bridge.yml` when `flutter_ffi.rs` changes.
- Conditional imports must maintain a compatible API between native and web implementations. A method added to native `PlatformFFI` may need a web implementation or an explicitly safe unsupported behavior.

## UI and State Rules

- Keep platform checks centralized through the existing helpers in `common.dart`/platform models.
- Do not place session business logic in widgets when an existing model owns that state.
- Register event handlers with a stable, unique handler name and unregister them when the owner is disposed.
- Respect desktop multi-window isolation. Globals are per Dart engine/window and are not automatically shared state.
- Preserve input coordinate transforms, display indices, scaling, and modifier state when touching remote input or rendering.
- Avoid blocking the UI isolate; use futures/streams and existing model notification patterns.
- Reuse existing dialogs, controls, theme values, and localization functions before adding variants.

## Verification

Run commands from this directory:

- `dart format --output=none --set-exit-if-changed lib test` for a formatting check.
- `flutter analyze` for static analysis.
- `flutter test` for the test suite, or `flutter test test/<focused_test>.dart` while iterating.

Do not run a full platform build unless the change crosses plugins, native embedding, FFI, assets, or packaging. Those builds require the matching Rust library and platform toolchain.
