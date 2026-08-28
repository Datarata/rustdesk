# Local Rust Crates Guide

`libs/` contains workspace crates used by the Rust core. These are not generic vendored copies: changes can affect protocol compatibility, capture, input, clipboard, packaging, or platform behavior across the whole application.

## Crate Map

- `hbb_common`: shared configuration, protobuf protocol types, networking/streams, TLS, proxying, password security, keyboard data, filesystem transfer helpers, logging, and common re-exports.
- `scrap`: screen capture and display enumeration for DXGI/Windows, Quartz/macOS, X11, Wayland, and Android; optional features add hardware codecs and VRAM paths.
- `enigo`: platform-specific keyboard and pointer injection.
- `clipboard`: clipboard file-transfer protocol/context and platform implementations.
- `virtual_display`: Windows virtual display control; `virtual_display/dylib` builds its dynamic-library component.
- `remote_printer`: Windows remote-printer integration.
- `portable`: Windows portable package builder executable.
- `libxdo-sys-stub`: local crates.io patch used so Wayland-only systems do not require libxdo.

The root `Cargo.toml` defines workspace membership and feature forwarding. Check it before changing crate features or dependencies.

## Protocol and Configuration

- `hbb_common/protos/message.proto` defines peer session/service messages.
- `hbb_common/protos/rendezvous.proto` defines rendezvous/relay messages.
- `hbb_common/build.rs` generates Rust modules into Cargo `OUT_DIR`; edit `.proto` sources, not generated Rust output.
- `hbb_common/src/config.rs` is the central option/configuration implementation. Search all readers and writers before renaming a key or changing its default/serialization.
- Protocol changes must be traced through both `src/client*` and `src/server/connection.rs`, with compatibility considered for older peers and servers.

## Editing and Verification

- Preserve target and feature gates in each crate. Capture/input/clipboard code often compiles only on one OS or display server.
- Keep unsafe/native boundaries small and explain non-obvious safety invariants near the code.
- Avoid expanding `hbb_common` re-exports without a clear cross-crate need.
- Prefer `cargo check -p <crate>` and `cargo test -p <crate>` for iteration, followed by a dependent root-crate check when feasible.
- For `hbb_common` protocol/config changes, a local crate check alone is insufficient; check the root `rustdesk` crate or the affected callers too.
