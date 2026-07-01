#!/usr/bin/env python3
"""Generate simple architecture SVG diagrams for the blueprint."""

from __future__ import annotations

import argparse
import os
import shutil
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "assets"
DEFAULT_PNG_DIR = ROOT / "outputs" / "diagrams"


THEME = {
    "bg": "transparent",
    "panel": "#0a100c",
    "panel_hot": "#0b1608",
    "panel_accent": "#160929",
    "inner_accent": "#1b0c31",
    "stroke": "#7d8780",
    "stroke_dim": "#3d4a42",
    "green": "#76b900",
    "accent": "#5f1ebe",
    "text": "#edf3ef",
    "muted": "#c6cec8",
}

GREEN_BORDER_LABELS = {
    "b200slurm",
    "brev",
    "cadtosimready",
    "cosmoscurator",
    "cosmosframework",
    "dynamo",
    "flashdreams",
    "isaac",
    "isaacsim",
    "launchable",
    "megatroncore",
    "nim",
    "ncore",
    "nvidiaskills",
    "nre",
    "nurecnre",
    "omniverse",
    "omniversertx",
    "osmo",
    "sbrev",
    "simready",
    "tao",
    "vss",
}


def label_key(label: str) -> str:
    return "".join(ch for ch in label.lower() if ch.isalnum())


def has_green_border(label: str) -> bool:
    key = label_key(label)
    return key in GREEN_BORDER_LABELS or key.startswith(("isaac", "nurec", "omniverse"))


def svg_open(title: str, desc: str, width: int = 1360, height: int = 620) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'  <title id="title">{escape(title)}</title>',
        f'  <desc id="desc">{escape(desc)}</desc>',
        "  <defs>",
        "    <style>",
        f"      .bg {{ fill: {THEME['bg']}; }}",
        f"      .box {{ fill: {THEME['panel']}; stroke: {THEME['stroke_dim']}; stroke-width: 2; }}",
        f"      .boxHot {{ fill: {THEME['panel_hot']}; stroke: {THEME['green']}; stroke-width: 2.3; }}",
        f"      .boxAccent {{ fill: {THEME['panel_accent']}; stroke: {THEME['accent']}; stroke-width: 2.3; }}",
        f"      .inner {{ fill: #0d130f; stroke: {THEME['stroke']}; stroke-width: 1.9; }}",
        f"      .innerHot {{ fill: #0d1809; stroke: {THEME['green']}; stroke-width: 1.9; }}",
        f"      .innerAccent {{ fill: {THEME['inner_accent']}; stroke: {THEME['accent']}; stroke-width: 1.9; }}",
        f"      .label {{ fill: {THEME['text']}; font-family: Aptos, Helvetica, sans-serif; font-size: 20px; font-weight: 680; }}",
        f"      .small {{ fill: {THEME['muted']}; font-family: Aptos, Helvetica, sans-serif; font-size: 13px; font-weight: 620; }}",
        "      .line { stroke: #e6ece8; stroke-width: 2.2; fill: none; marker-end: url(#arrow); }",
        f"      .greenLine {{ stroke: {THEME['green']}; stroke-width: 2.4; fill: none; marker-end: url(#arrowGreen); }}",
        f"      .accentLine {{ stroke: {THEME['accent']}; stroke-width: 2.4; fill: none; marker-end: url(#arrowAccent); }}",
        "    </style>",
        '    <marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto-start-reverse">',
        '      <path d="M 0 1 L 8 4 L 0 7 z" fill="#e6ece8"/>',
        "    </marker>",
        '    <marker id="arrowGreen" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto-start-reverse">',
        f'      <path d="M 0 1 L 8 4 L 0 7 z" fill="{THEME["green"]}"/>',
        "    </marker>",
        '    <marker id="arrowAccent" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="5" markerHeight="5" orient="auto-start-reverse">',
        f'      <path d="M 0 1 L 8 4 L 0 7 z" fill="{THEME["accent"]}"/>',
        "    </marker>",
        "  </defs>",
        f'  <rect class="bg" x="0" y="0" width="{width}" height="{height}"/>',
    ]


def text_size(label: str) -> int:
    if len(label) > 24:
        return 10
    if len(label) > 18:
        return 11
    if len(label) > 14:
        return 12
    return 13


def inner_box(
    x: int,
    y: int,
    w: int,
    h: int,
    label: str,
    hot: bool = False,
    accent: bool = False,
) -> list[str]:
    cls = "innerHot" if hot else "innerAccent" if accent else "inner"
    size = min(text_size(label), max(8, h - 6))
    return [
        f'  <rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="4"/>',
        f'  <text class="small" x="{x + w / 2:.1f}" y="{y + h / 2 + size / 2 - 2:.1f}" text-anchor="middle" style="font-size:{size}px">{escape(label)}</text>',
    ]


def outer_box(
    x: int,
    y: int,
    w: int,
    h: int,
    title: str,
    items: list[str],
    hot_items: set[str] | None = None,
    hot: bool = False,
) -> list[str]:
    hot_items = hot_items or set()
    title_is_nvidia = has_green_border(title)
    cls = "boxHot" if title_is_nvidia else "boxAccent" if hot else "box"
    out = [f'  <rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/>']
    title_y = y + (38 if h <= 110 else 43)
    out.append(f'  <text class="label" x="{x + w / 2:.1f}" y="{title_y}" text-anchor="middle">{escape(title)}</text>')

    if not items:
        return out

    ix = x + 28
    iw = w - 56
    content_top = y + (54 if h <= 110 else 72)
    content_bottom = y + h - 18
    available = content_bottom - content_top
    gap = 8 if h <= 150 else 12
    ih = min(36, max(16, int((available - gap * (len(items) - 1)) / len(items))))
    total_height = ih * len(items) + gap * (len(items) - 1)
    start_y = content_top + max(0, int((available - total_height) / 2))
    for i, item in enumerate(items):
        item_is_nvidia = has_green_border(item)
        out.extend(
            inner_box(
                ix,
                start_y + i * (ih + gap),
                iw,
                ih,
                item,
                hot=item_is_nvidia,
                accent=item in hot_items and not item_is_nvidia,
            )
        )
    return out


def arrow(x1: int, y1: int, x2: int, y2: int, hot: bool = False, accent: bool = False) -> str:
    cls = "greenLine" if hot else "accentLine" if accent else "line"
    return f'  <path class="{cls}" d="M{x1} {y1} L{x2} {y2}"/>'


def elbow(points: list[tuple[int, int]], hot: bool = False, accent: bool = False) -> str:
    cls = "greenLine" if hot else "accentLine" if accent else "line"
    path = [f"M{points[0][0]} {points[0][1]}"]
    path.extend(f"L{x} {y}" for x, y in points[1:])
    return f'  <path class="{cls}" d="{" ".join(path)}"/>'


def write_svg(name: str, lines: list[str]) -> None:
    lines.append("</svg>")
    (ASSETS / name).write_text("\n".join(lines) + "\n", encoding="utf-8")


def find_chromium() -> str:
    configured = os.environ.get("WMB_CHROMIUM")
    if configured:
        return configured

    for candidate in ("chromium-browser", "chromium", "google-chrome", "google-chrome-stable"):
        path = shutil.which(candidate)
        if path:
            return path

    raise SystemExit("No Chromium executable found. Set WMB_CHROMIUM=/path/to/chromium and retry.")


def export_pngs(output_dir: Path) -> None:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit("PNG export requires the optional Python package 'playwright'.") from exc

    chromium = find_chromium()
    output_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=chromium)
        for svg_path in sorted(ASSETS.glob("*.svg")):
            svg = svg_path.read_text(encoding="utf-8")
            root = ET.fromstring(svg)
            width = int(float(root.attrib["width"]))
            height = int(float(root.attrib["height"]))
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            page.set_content(
                "<!doctype html><html><head><style>"
                f"html,body{{margin:0;padding:0;background:transparent;width:{width}px;height:{height}px;overflow:hidden;}}"
                "svg{display:block;}"
                "</style></head><body>"
                + svg
                + "</body></html>"
            )
            page.screenshot(path=str(output_dir / f"{svg_path.stem}.png"), omit_background=True)
            page.close()
        browser.close()


def architecture() -> None:
    lines = svg_open(
        "World model blueprint architecture",
        "A five-block architecture from scoped evidence to data assets, Cosmos adaptation, inference, and sim-to-real operations.",
    )
    x0, y, w, h, gap = 62, 118, 222, 230, 22
    boxes = [
        ("Scope", ["objective", "embodiment", "risk gates"], {"risk gates"}),
        ("Data + assets", ["OpenUSD", "NuRec/NRE", "SimReady"], {"NuRec/NRE", "SimReady"}),
        ("Adapt", ["Cosmos Framework", "Brev", "B200 Slurm"], {"Cosmos Framework"}),
        ("Serve", ["NIM", "FlashDreams", "Dynamo"], {"NIM", "FlashDreams", "Dynamo"}),
        ("Operate", ["OSMO", "Kubernetes/Ray", "rollback"], {"OSMO"}),
    ]
    for i, (title, items, hot_items) in enumerate(boxes):
        x = x0 + i * (w + gap)
        lines.extend(outer_box(x, y, w, h, title, items, hot_items, hot=i == 2))
        if i < len(boxes) - 1:
            lines.append(arrow(x + w, y + h // 2, x + w + gap - 4, y + h // 2))

    adapt_center = x0 + 2 * (w + gap) + w // 2
    agent_x, agent_y, agent_w, agent_h = adapt_center - 204, 404, 408, 150
    lines.extend(
        outer_box(
            agent_x,
            agent_y,
            agent_w,
            agent_h,
            "Agent control",
            ["skills", "eval suites"],
            {"skills", "eval suites"},
            hot=True,
        )
    )
    lines.append(arrow(agent_x + agent_w // 2, agent_y, adapt_center, y + h, accent=True))
    lines.append(elbow([(x0 + 4 * (w + gap) + w // 2, y + h), (x0 + 4 * (w + gap) + w // 2, 390), (x0 + w + gap + w // 2, 390), (x0 + w + gap + w // 2, y + h)], accent=True))
    write_svg("architecture.svg", lines)


def data_factory() -> None:
    lines = svg_open(
        "Data and SimReady factory",
        "A schematic for turning operational evidence and business-critical assets into model-ready data.",
    )
    x0, y, w, h, gap = 74, 130, 280, 230, 34
    boxes = [
        ("Real evidence", ["video logs", "actions", "telemetry"], {"telemetry"}),
        ("Digital assets", ["CAD", "OpenUSD", "NuRec/NRE", "SimReady"], {"NuRec/NRE", "SimReady"}),
        ("Curate", ["TAO", "VSS", "Cosmos Curator"], {"TAO"}),
        ("Dataset", ["manifest", "holdouts", "stress slices"], {"manifest"}),
    ]
    for i, (title, items, hot_items) in enumerate(boxes):
        x = x0 + i * (w + gap)
        lines.extend(outer_box(x, y, w, h, title, items, hot_items, hot=i == 2))
        if i < len(boxes) - 1:
            lines.append(arrow(x + w, y + h // 2, x + w + gap - 4, y + h // 2))

    curate_center = x0 + 2 * (w + gap) + w // 2
    synth_x, synth_y, synth_w, synth_h = curate_center - 290, 424, 580, 108
    lines.extend(outer_box(synth_x, synth_y, synth_w, synth_h, "Synthetic gap closure", ["scenario evidence"], {"scenario evidence"}, hot=True))
    lines.append(arrow(synth_x + synth_w // 2, synth_y, curate_center, y + h, accent=True))
    write_svg("data-factory.svg", lines)


def agent_workflow() -> None:
    lines = svg_open(
        "Agent workflow",
        "A schematic for LLM-backed agents that execute local skills, produce evidence, and pass review gates.",
    )
    x0, y, w, h, gap = 70, 90, 260, 176, 60
    boxes = [
        ("User", ["objective", "evidence path"], set()),
        ("LLM runtime", ["API key", "model id"], {"model id"}),
        ("Skill router", ["SKILL.md", "output contract"], {"SKILL.md"}),
        ("Artefacts", ["manifests", "review gates"], {"review gates"}),
    ]
    for i, (title, items, hot_items) in enumerate(boxes):
        x = x0 + i * (w + gap)
        lines.extend(outer_box(x, y, w, h, title, items, hot_items, hot=i == 2))
        if i < len(boxes) - 1:
            lines.append(arrow(x + w, y + h // 2, x + w + gap - 4, y + h // 2, accent=i == 1))

    step_y, step_w, step_h, step_gap = 380, 105, 74, 12
    steps = ["intake", "data", "neural", "simready", "fine-tune", "inference", "eval", "deploy", "govern"]
    step_x = 64
    for i, step in enumerate(steps):
        x = step_x + i * (step_w + step_gap)
        lines.extend(outer_box(x, step_y, step_w, step_h, step, [], hot=step in {"fine-tune", "inference"}))
        if i < len(steps) - 1:
            lines.append(arrow(x + step_w, step_y + step_h // 2, x + step_w + step_gap - 4, step_y + step_h // 2))
    lines.append(elbow([(x0 + 2 * (w + gap) + w // 2, y + h), (x0 + 2 * (w + gap) + w // 2, 334), (step_x + 2 * (step_w + step_gap) + step_w // 2, 334), (step_x + 2 * (step_w + step_gap) + step_w // 2, step_y)], accent=True))
    write_svg("agent-workflow.svg", lines)


def neural_asset_services() -> None:
    lines = svg_open(
        "Neural asset services",
        "A schematic for routing source evidence to NVIDIA skills, Content Agents, NuRec, and SimReady or dataset handoff.",
    )
    lines.extend(outer_box(56, 220, 244, 180, "Evidence", ["sensors", "CAD/OpenUSD", "video gaps"], {"sensors"}))
    lines.extend(outer_box(392, 202, 252, 216, "Route selector", ["rights", "service surface", "validation"], {"service surface"}, hot=True))
    lines.append(arrow(300, 310, 392, 310, accent=True))

    routes = [
        (740, 42, 126, "NVIDIA/skills", ["CAD-to-SimReady", "video aug", "defect gen"]),
        (740, 188, 136, "Content Agents", ["material", "physics", "validation"]),
        (740, 344, 126, "Omniverse RTX", ["preview", "video", "sensor sim"]),
        (740, 490, 104, "NuRec/NRE", ["ncore", "nre", "harvest"]),
    ]
    route_trunk_x = 696
    for x, y, h, title, items in routes:
        highlighted_route = title in {"NVIDIA/skills", "Content Agents", "Omniverse RTX"}
        nvidia_route = has_green_border(title)
        hot_items = {items[0]}
        lines.extend(outer_box(x, y, 274, h, title, items, hot_items, hot=highlighted_route))
        route_y = y + h // 2
        lines.append(
            elbow(
                [(644, 310), (route_trunk_x, 310), (route_trunk_x, route_y), (x, route_y)],
                hot=highlighted_route and nvidia_route,
                accent=highlighted_route and not nvidia_route,
            )
        )

    lines.extend(outer_box(1158, 224, 156, 172, "Handoff", ["SimReady", "dataset", "eval"], {"SimReady"}, hot=True))
    handoff_trunk_x = 1090
    for route_y, title, highlighted_route in (
        (105, "NVIDIA/skills", True),
        (256, "Content Agents", True),
        (407, "Omniverse RTX", True),
        (542, "NuRec/NRE", False),
    ):
        nvidia_route = has_green_border(title)
        lines.append(
            elbow(
                [(1014, route_y), (handoff_trunk_x, route_y), (handoff_trunk_x, 310), (1158, 310)],
                hot=highlighted_route and nvidia_route,
                accent=highlighted_route and not nvidia_route,
            )
        )
    write_svg("neural-asset-services.svg", lines)


def execution_lanes() -> None:
    lines = svg_open(
        "Execution lane selection",
        "A schematic mapping workload classes to Brev, B200 Slurm, Megatron, OSMO, Kubernetes, Ray, NIM, and FlashDreams.",
    )
    selector_x, selector_y, selector_w, selector_h = 76, 214, 250, 172
    lines.extend(outer_box(selector_x, selector_y, selector_w, selector_h, "Lane selector", ["evidence target", "cost envelope"], {"evidence target"}, hot=True))

    lanes = [
        (468, 48, 150, "Pilot", ["Brev", "Launchable"]),
        (468, 232, 150, "Large training", ["B200 Slurm", "Pyxis/Enroot"]),
        (468, 416, 150, "Massive scale", ["Megatron-Core", "Bridge"]),
        (904, 134, 150, "Orchestrate", ["OSMO", "Kubernetes/Ray"]),
        (904, 326, 178, "Serve", ["NIM", "FlashDreams", "Dynamo"]),
    ]
    lane_trunk_x = 394
    for x, y, lane_h, title, items in lanes:
        hot_items = {items[0]}
        lines.extend(outer_box(x, y, 310, lane_h, title, items, hot_items, hot=title in {"Large training", "Orchestrate"}))
        if title in {"Pilot", "Large training", "Massive scale"}:
            lane_y = y + lane_h // 2
            lines.append(elbow([(selector_x + selector_w, selector_y + selector_h // 2), (lane_trunk_x, selector_y + selector_h // 2), (lane_trunk_x, lane_y), (x, lane_y)], accent=title == "Large training"))
    lines.append(elbow([(778, 307), (842, 307), (842, 209), (904, 209)], accent=True))
    lines.append(elbow([(778, 491), (842, 491), (842, 415), (904, 415)]))
    write_svg("execution-lanes.svg", lines)


def inference_services() -> None:
    lines = svg_open(
        "Inference services",
        "A schematic for inference backend choices and integration targets for a Cosmos-class world model.",
    )
    lines.extend(outer_box(70, 236, 250, 150, "Checkpoint", ["Cosmos adapter", "export policy"], {"export policy"}))
    lines.extend(outer_box(440, 216, 250, 190, "Backend selector", ["latency", "support", "closed loop"], {"latency"}, hot=True))
    lines.append(arrow(320, 311, 440, 311))

    services = [
        (810, 44, 108, "NIM", ["Production API"]),
        (810, 182, 108, "FlashDreams", ["real-time loop"]),
        (810, 320, 108, "Dynamo", ["cluster service"]),
        (810, 458, 120, "Custom", ["vLLM", "Transformers"]),
    ]
    service_trunk_x = 752
    for x, y, svc_h, title, items in services:
        lines.extend(outer_box(x, y, 248, svc_h, title, items, {items[0]}, hot=title in {"NIM", "FlashDreams", "Dynamo"}))
        svc_y = y + svc_h // 2
        lines.append(elbow([(690, 311), (service_trunk_x, 311), (service_trunk_x, svc_y), (x, svc_y)], hot=title in {"NIM", "FlashDreams"}))

    lines.extend(outer_box(1136, 230, 156, 166, "Integrate", ["Isaac Sim", "shadow", "real"], {"Isaac Sim"}, hot=True))
    integrate_trunk_x = 1094
    for _, y, svc_h, title, _ in services[:3]:
        svc_y = y + svc_h // 2
        lines.append(elbow([(1058, svc_y), (integrate_trunk_x, svc_y), (integrate_trunk_x, 313), (1136, 313)], hot=title in {"NIM", "FlashDreams"}))
    write_svg("inference-services.svg", lines)


def generate_svgs() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    architecture()
    data_factory()
    neural_asset_services()
    agent_workflow()
    execution_lanes()
    inference_services()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate world-model blueprint diagrams.")
    parser.add_argument("--png", action="store_true", help="also export transparent PNGs from the generated SVGs")
    parser.add_argument("--png-dir", type=Path, default=DEFAULT_PNG_DIR, help="directory for PNG exports")
    args = parser.parse_args()

    generate_svgs()
    if args.png:
        export_pngs(args.png_dir)


if __name__ == "__main__":
    main()
