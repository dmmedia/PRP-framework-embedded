# AGENTS.md — Zephyr RTOS / C / west

<!--
TEMPLATE INSTRUCTIONS (remove this block before committing):
This file is an AGENTS.md template for a Zephyr RTOS firmware project.
Fill in every <!-- FILL: --> placeholder with project-specific details.
Detailed guidance is provided next to each placeholder as HTML comments.
Follow HOW-TO-WRITE-AGENT.md: keep this file < 300 lines, prefer pointers
over copies, and remove any section that does not apply to your project.
-->

## Project Overview

<!-- FILL: One or two sentences describing what this firmware does and what
hardware it targets. Be specific: board name, SoC family, purpose.
Example: "Flight controller firmware for the Acme-FCS board (STM32H743).
Reads IMU, runs PID loops, and outputs PWM to four ESCs." -->
**[PROJECT_NAME]** — [short purpose statement].

Target hardware: **[BOARD_NAME]** ([SOC_FAMILY] SoC).

<!-- FILL: Mention the Zephyr version (or west manifest branch) the project
tracks. This prevents the agent from suggesting APIs that don't exist yet.
Example: "Tracks Zephyr v3.7 LTS." -->
Zephyr version: **[ZEPHYR_VERSION]** (e.g. `v3.7-branch`).

## Repository Layout

<!-- FILL: Describe the top-level folders agents will navigate.
Include every directory an agent might need to read or edit.
Typical Zephyr app structure shown below — adjust to match reality.
Example entries:
  app/          — application source (main.c, CMakeLists.txt, prj.conf)
  boards/       — custom board definitions (.yaml, .dts, Kconfig)
  drivers/      — out-of-tree drivers
  dts/          — shared DeviceTree includes / overlays
  tests/        — Twister test suites
  doc/          — architecture docs, agent_docs/ pointers below
  west.yml      — west manifest (pin all module SHAs here)
-->

```
[PROJECT_ROOT]/
    app/                  <!-- FILL: per-app source trees, one per binary -->
    boards/               <!-- FILL: present only if custom boards exist -->
    drivers/              <!-- FILL: present only if out-of-tree drivers -->
    dts/                  <!-- FILL: shared .dtsi / overlay files -->
    tests/                <!-- FILL: Twister suites -->
    west.yml              <!-- west manifest — single source of truth for deps -->
    CMakeLists.txt        <!-- FILL: root or per-app; clarify which -->
    prj.conf              <!-- FILL: default Kconfig fragment -->
```

<!-- FILL: If this is a T2 star topology (app repo + Zephyr as module),
say so explicitly. Example:
"This is a west T2 star topology: this repo is the application repository;
Zephyr and all HALs are fetched by `west update` into ../zephyr, ../modules/."
-->
West topology: **[T1 single-repo | T2 star topology]**.

## Development Environment

<!-- FILL: State the exact toolchain agents must use.
Do NOT assume the host PATH is set correctly.
Examples:
  "Use Zephyr SDK 0.16.4 installed at ~/zephyr-sdk-0.16.4."
  "Toolchain is arm-zephyr-eabi from the Zephyr SDK; do NOT use system gcc."
  "CMake ≥ 3.20 and Ninja are required."
  "Python venv is managed by west; activate with `source .venv/bin/activate`."
-->
- Toolchain: **[TOOLCHAIN_NAME + VERSION]** (e.g. Zephyr SDK 0.16.4, arm-zephyr-eabi)
- CMake: **[CMAKE_MIN_VERSION]+**
- Build backend: **Ninja** (default) or **make**
- Python: managed by west; activate venv before running west commands.

<!-- FILL: If a container / Docker image is the expected dev environment,
name it here and point to the Dockerfile or image tag.
Example: "Use the project Docker image: ghcr.io/acme/zephyr-dev:0.16.4" -->

## Build Commands

<!-- FILL: Replace BOARD and APP_DIR with real values, or keep as placeholders
with an explanatory note like "substitute your target board identifier."
List every variant an agent might need: debug, release, size-optimised, etc.
The `-- -v` suffix enables verbose Ninja output for diagnosing build failures. -->

```bash
# Configure + build (first time or after Kconfig/DTS changes)
west build -b [BOARD] [APP_DIR] --pristine

# Incremental build
west build

# Build with a specific overlay (hardware variant, debug config, etc.)
west build -b [BOARD] [APP_DIR] -- -DDTC_OVERLAY_FILE=[OVERLAY].overlay \
    -DEXTRA_CONF_FILE=[EXTRA].conf

# Build with verbose output (use when diagnosing CMake/Ninja failures)
west build -b [BOARD] [APP_DIR] -- -v
```

<!-- FILL: Add any mandatory CMake cache variables your project always needs.
Example: "-DCONFIG_MYAPP_VERSION=\"1.2.3\""
If none, delete this comment. -->

## Flash & Debug

<!-- FILL: List the exact runner(s) supported by this project.
Zephyr runners include: openocd, jlink, pyocd, stlink, nrfjprog, esptool, etc.
If multiple runners are valid, list all and note the default.
Example:
  "Default runner: openocd (SEGGER J-Link via openocd-zephyr config)."
  "Alternate: `west flash --runner=jlink` for bare J-Link probes."
-->

```bash
# Flash (uses default runner configured in board definition)
west flash

# Flash with explicit runner
west flash --runner=[RUNNER]   <!-- e.g. openocd, jlink, pyocd -->

# Attach GDB (starts openocd server + arm-zephyr-eabi-gdb)
west debug

# Start debug server only (e.g. to attach VS Code's Cortex-Debug extension)
west debugserver
```

<!-- FILL: Note any hardware prerequisites (probe model, JTAG vs SWD,
required firmware version, power requirements).
Example: "Requires SEGGER J-Link EDU Mini with firmware ≥ V7.94." -->

## Testing

<!-- FILL: Describe the test strategy.
Options: Twister (on-target or QEMU/native_sim), Unity, Ztest, host-side pytest.
Specify the QEMU target if emulation is used.
Example:
  "Unit tests use Ztest and run on native_sim (no hardware needed)."
  "Integration tests require a connected [BOARD]; tag them with `@boards [BOARD]`."
-->

```bash
# Run all tests on native simulator (no hardware required)
west twister -p native_sim -T tests/

# Run tests on target board (requires connected hardware)
west twister -p [BOARD] -T tests/ --device-testing \
    --device-serial [SERIAL_PORT]

# Run a single test suite
west twister -p native_sim -T tests/[SUITE_DIR]

# Run with coverage report (native_sim only)
west twister -p native_sim -T tests/ --coverage
```

<!-- FILL: State the minimum pass criteria before a PR is merged.
Example: "All native_sim tests must pass. On-target smoke test on [BOARD]
must pass for changes touching drivers/ or dts/." -->

## Kconfig

<!-- FILL: List project-specific Kconfig symbols agents are likely to touch.
Too many symbols → move to agent_docs/kconfig_reference.md and point here.
Example:
  CONFIG_MYAPP_SENSOR_POLL_MS  — sensor polling interval in ms (default 100)
  CONFIG_MYAPP_BLE_ENABLED     — enable BLE stack (requires CONFIG_BT=y)
-->
Key symbols:

| Symbol | Description | Default |
| --- | --- | --- |
| `CONFIG_[SYMBOL_1]` | <!-- FILL: brief description --> | `[DEFAULT]` |
| `CONFIG_[SYMBOL_2]` | <!-- FILL: brief description --> | `[DEFAULT]` |

<!-- FILL: Note which .conf fragments are layered and in what order.
Example: "prj.conf → boards/[BOARD].conf → optional debug.conf overlay." -->

## DeviceTree

<!-- FILL: Identify the canonical .dts file and any board-specific overlays.
Point agents to the exact file:line for the most-edited nodes.
Example:
  "Main DTS: boards/arm/[BOARD]/[BOARD].dts"
  "Application overlay: app/[BOARD].overlay — add peripherals here."
  "Do NOT edit Zephyr upstream .dts files; use overlays instead."
-->
- Board DTS: `[PATH_TO_BOARD_DTS]`
- Application overlay: `[PATH_TO_APP_OVERLAY]`

**NEVER** edit Zephyr upstream DTS files directly; always use `.overlay` files.

## Out-of-Tree Drivers / Modules

<!-- FILL: List any custom drivers or Zephyr modules maintained in this repo.
For each, note the compatible string and the Kconfig symbol that enables it.
Example:
  drivers/sensor/acme_imu/ — custom IMU driver, compatible "acme,imu-v2",
  enabled by CONFIG_ACME_IMU=y
If none exist, delete this section. -->

| Path | Compatible / Kconfig | Purpose |
| --- | --- | --- |
| `[DRIVER_PATH]` | `[COMPATIBLE_STRING]` / `CONFIG_[SYMBOL]` | <!-- FILL --> |

## Reference Docs

<!-- FILL: Add pointers to agent_docs/ files for topics too large for this file.
Keep this file < 300 lines by moving deep-dive content into agent_docs/.
Suggested files (create as needed):
  agent_docs/build_system.md      — CMake cache variables, multi-image builds
  agent_docs/hardware_bringup.md  — probe setup, flash layout, partition table
  agent_docs/ble_architecture.md  — BLE stack config, GATT service layout
  agent_docs/power_management.md  — PM states, wakeup sources
  agent_docs/testing_guide.md     — Twister options, QEMU variants, coverage
-->

Read the relevant doc before starting work on that area:

- `agent_docs/[TOPIC_1].md` — [brief description]
- `agent_docs/[TOPIC_2].md` — [brief description]

<!-- FILL: Add a pointer to official Zephyr docs for topics not covered above.
The agent should prefer the pinned Zephyr version docs over generic web search.
Example:
  "Official Zephyr docs for this version: https://docs.zephyrproject.org/[VER]/"
-->
Official Zephyr docs: **[ZEPHYR_DOCS_URL]** (pin to your Zephyr version).

## Constraints

<!-- FILL: Hard rules the agent must never violate.
List only rules that are non-obvious or project-specific; do not repeat
standard Zephyr/C conventions the model already knows.
Examples:
  "Do NOT enable CONFIG_HEAP_MEM_POOL on this target (< 64 kB RAM)."
  "All ISRs must complete in < 10 µs; flag any violation as a blocker."
  "The flash partition table is immutable; do not change it without explicit approval."
-->

- **[CONSTRAINT_1]**
- **[CONSTRAINT_2]**
