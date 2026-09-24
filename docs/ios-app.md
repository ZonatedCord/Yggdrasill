# iOS App — WLED Native

A native iPhone/iPad app to discover and control WLED devices on the local network.

---

## Overview

Yggdrasill's iOS app is a fork of [Moustachauve/WLED-iOS](https://github.com/Moustachauve/WLED-iOS) (GPL v3), restyled with **Apple's Liquid Glass** design language (iOS 26). Published fork: [ZonatedCord/WLED-iOS](https://github.com/ZonatedCord/WLED-iOS) (`origin`; `upstream` = Moustachauve/WLED-iOS). Embedded here as a **git submodule** tracking the `liquid-glass-redesign` branch — clone Yggdrasill with `--recurse-submodules` to pull it in.

The app communicates with WLED firmware running on the ESP32 via:
- **WebSocket** — real-time state sync
- **WLED JSON API** — device discovery and control
- **mDNS** — automatic device detection on LAN

---

## Architecture

```
WLED-iOS/
├── wled/
│   ├── Model/          # Data models (Device, LEDState, Palette, …)
│   ├── ViewModel/      # ObservableObjects for SwiftUI bindings
│   ├── View/           # SwiftUI views — Liquid Glass redesign here
│   ├── Service/        # Network layer (WebSocket, HTTP, mDNS)
│   └── WLEDNativeApp.swift   # App entry point
├── Data/               # CoreData schema (wled_native_data.xcdatamodeld)
└── wled.xcodeproj
```

Pattern: **MVVM**. Models in `Model/`, view models in `ViewModel/`, views in `View/`.

---

## Liquid Glass redesign

The fork replaces the original flat UI with Apple's **Liquid Glass** material system (introduced iOS 26):

- Device list cards use `.glassEffect()` with specular highlights
- Controls use glass-backed sliders and toggles
- Color picker adopts radial blur behind glass panels
- Light/dark mode: glass adapts automatically to ambient lightness
- Requires **iOS 26+** deployment target (verify in `Info.plist`)

---

## Build

1. Open `WLED-iOS/wled.xcodeproj` in **Xcode 16+**
2. Set a valid development team in Signing & Capabilities
3. Build to a physical device or simulator (iOS 26+)

---

## Dependencies

No external package managers. Pure Swift / SwiftUI + CoreData.

---

## License

GPL v3 — inherited from upstream. See `WLED-iOS/LICENSE`. Cannot be changed.
