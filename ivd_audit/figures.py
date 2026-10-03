"""Publication-oriented figures generated without external plotting libraries."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


WIDTH = 1800
HEIGHT = 1200
BG = "#FFFFFF"
INK = "#172033"
MUTED = "#667085"
GRID = "#D9E1EA"
BLUE = "#2166AC"
RED = "#C43D4B"
ORANGE = "#D97706"
TEAL = "#0F766E"
GRAY = "#98A2B3"


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    path = Path("C:/Windows/Fonts") / name
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _canvas(width: int = WIDTH, height: int = HEIGHT) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (width, height), BG)
    return image, ImageDraw.Draw(image)


def _save(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path.with_suffix(".png"), dpi=(300, 300))
    image.save(path.with_suffix(".pdf"), "PDF", resolution=300.0)


def _text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[float, float],
    value: str,
    size: int,
    *,
    bold: bool = False,
    fill: str = INK,
    anchor: str = "la",
) -> None:
    draw.text(xy, value, font=_font(size, bold=bold), fill=fill, anchor=anchor)


def _vertical_text(
    image: Image.Image,
    xy: tuple[float, float],
    value: str,
    size: int,
    *,
    bold: bool = False,
    fill: str = INK,
) -> None:
    font = _font(size, bold=bold)
    bounds = font.getbbox(value)
    width = bounds[2] - bounds[0] + 6
    height = bounds[3] - bounds[1] + 6
    layer = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    layer_draw = ImageDraw.Draw(layer)
    layer_draw.text((3 - bounds[0], 3 - bounds[1]), value, font=font, fill=fill)
    rotated = layer.rotate(90, expand=True)
    x, y = xy
    image.paste(
        rotated,
        (int(x - rotated.width / 2), int(y - rotated.height / 2)),
        rotated,
    )


def _arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str = MUTED,
    width: int = 5,
) -> None:
    draw.line([start, end], fill=color, width=width)
    x, y = end
    draw.polygon([(x, y), (x - 14, y - 9), (x - 14, y + 9)], fill=color)


def draw_workflow(path: Path) -> None:
    image, draw = _canvas()
    _text(draw, (70, 45), "A reproducibility gate for cross-cohort omics claims", 42, bold=True)
    _text(
        draw,
        (70, 105),
        "Every step is a stopping rule, not a post hoc sensitivity analysis.",
        23,
        fill=MUTED,
    )
    labels = [
        ("1", "Inventory", "Tissue, platform,\nendpoint, n"),
        ("2", "Harmonise", "Same direction,\nsame endpoint"),
        ("3", "Check", "Depth, global shift,\nconfounding"),
        ("4", "Re-estimate", "Independent unit,\nmatched strata"),
        ("5", "Test", "Module direction\nand gene signs"),
        ("6", "Report", "Replicated only if\nboth layers pass"),
    ]
    x0, y0 = 70, 245
    box_w, gap = 250, 25
    for i, (number, title, detail) in enumerate(labels):
        x = x0 + i * (box_w + gap)
        fill = "#EEF5FB" if i < 5 else "#EAF6F3"
        outline = BLUE if i < 5 else TEAL
        draw.rounded_rectangle(
            [x, y0, x + box_w, y0 + 235],
            radius=18,
            fill=fill,
            outline=outline,
            width=3,
        )
        draw.ellipse([x + 18, y0 + 18, x + 62, y0 + 62], fill=outline)
        _text(draw, (x + 40, y0 + 40), number, 22, bold=True, fill=BG, anchor="mm")
        _text(draw, (x + 18, y0 + 92), title, 28, bold=True)
        draw.multiline_text(
            (x + 18, y0 + 138),
            detail,
            font=_font(22),
            fill=MUTED,
            spacing=8,
        )
        if i < len(labels) - 1:
            _arrow(draw, (x + box_w + 7, y0 + 118), (x + box_w + gap - 7, y0 + 118))

    y1 = 570
    draw.line([(70, y1), (1730, y1)], fill=GRID, width=3)
    examples = [
        (
            "Fails global shift",
            "Do not centre away a\nwhole-matrix loading artifact.",
            RED,
        ),
        (
            "Fails confound gate",
            "If grade is inseparable from\nprocessing, stratify or stop.",
            ORANGE,
        ),
        (
            "Fails gene concordance",
            "A strong module in one cohort\nis not replication.",
            BLUE,
        ),
    ]
    for i, (title, body, color) in enumerate(examples):
        x = 95 + i * 560
        draw.line([(x, y1 + 35), (x, y1 + 245)], fill=color, width=10)
        _text(draw, (x + 35, y1 + 45), title, 28, bold=True, fill=color)
        draw.multiline_text(
            (x + 35, y1 + 100),
            body,
            font=_font(22),
            fill=INK,
            spacing=10,
        )

    draw.rounded_rectangle(
        [70, 930, 1730, 1120],
        radius=18,
        fill="#F8FAFC",
        outline=GRID,
        width=2,
    )
    _text(draw, (105, 970), "Minimum reportable unit", 28, bold=True)
    _text(draw, (105, 1028), "Module direction", 22, fill=MUTED)
    _text(draw, (390, 1025), "+", 30, bold=True, fill=MUTED)
    _text(draw, (440, 1028), "gene-level sign concordance", 22, fill=MUTED)
    _text(draw, (840, 1025), "+", 30, bold=True, fill=MUTED)
    _text(draw, (890, 1028), "independent internal reliability", 22, fill=MUTED)
    _text(draw, (1330, 1025), "+", 30, bold=True, fill=MUTED)
    _text(draw, (1380, 1028), "technical diagnostics", 22, fill=MUTED)
    _save(image, path)


def _panel_label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], label: str) -> None:
    _text(draw, xy, label, 30, bold=True)


def _bar(
    draw: ImageDraw.ImageDraw,
    *,
    x: int,
    y: int,
    width: int,
    height: int,
    value: float,
    max_value: float,
    color: str,
    label: str,
    value_text: str,
) -> None:
    _text(draw, (x, y), label, 21, fill=INK)
    bar_y = y + 34
    draw.rounded_rectangle(
        [x, bar_y, x + width, bar_y + height],
        radius=7,
        fill="#EDF1F5",
    )
    filled = int(width * min(max(value / max_value, 0), 1))
    if filled:
        draw.rounded_rectangle(
            [x, bar_y, x + filled, bar_y + height],
            radius=7,
            fill=color,
        )
    _text(draw, (x + width + 18, bar_y + height / 2), value_text, 21, bold=True, anchor="lm")


def draw_ecm_paradox(
    summary: pd.DataFrame,
    reliability: pd.DataFrame,
    path: Path,
) -> None:
    image, draw = _canvas()
    _text(draw, (70, 40), "ECM module significance does not reproduce at gene level", 39, bold=True)
    _text(
        draw,
        (70, 93),
        "GSE23130 is internally reproducible for ECM, yet its direction is not shared with GSE70362.",
        22,
        fill=MUTED,
    )
    for x, label in ((70, "A"), (960, "B")):
        _panel_label(draw, (x, 145), label)

    _text(draw, (70, 185), "ECM directional fraction", 27, bold=True)
    bars = [
        ("GSE23130 all samples", 0.871, RED),
        ("GSE23130 LCM, I-IV", 0.774, ORANGE),
        ("GSE70362 AF, all", 0.467, BLUE),
        ("GSE70362 AF, I-IV", 0.467, BLUE),
    ]
    for i, (label, value, color) in enumerate(bars):
        _bar(
            draw,
            x=70,
            y=245 + i * 112,
            width=690,
            height=30,
            value=value,
            max_value=1.0,
            color=color,
            label=label,
            value_text=f"{100 * value:.1f}%",
        )
    for fraction in (0.5,):
        x = 70 + int(690 * fraction)
        draw.line([(x, 230), (x, 690)], fill=INK, width=2)
        _text(draw, (x + 8, 700), "50%", 18, fill=INK)

    _text(draw, (960, 185), "Cross-cohort gene-level sign concordance", 27, bold=True)
    values = [
        ("All available samples", float(summary.iloc[0]["ecm_sign_concordance"]), ORANGE),
        ("Grade I-IV, LCM-only", float(summary.iloc[1]["ecm_sign_concordance"]), RED),
    ]
    for i, (label, value, color) in enumerate(values):
        _bar(
            draw,
            x=960,
            y=245 + i * 150,
            width=670,
            height=36,
            value=value,
            max_value=0.75,
            color=color,
            label=label,
            value_text=f"{100 * value:.1f}%",
        )
    x = 960 + int(670 * (0.5 / 0.75))
    draw.line([(x, 225), (x, 530)], fill=INK, width=2)
    _text(draw, (x + 8, 540), "chance = 50%", 18, fill=INK)

    _text(draw, (960, 625), "Internal split-half Spearman rho", 27, bold=True)
    rel = reliability.copy()
    rel["key"] = rel["cohort"] + " | " + rel["gene_space"]
    rows = [
        ("GSE70362_AF_I_IV | all", "GSE70362 AF I-IV, all genes", BLUE),
        ("GSE70362_AF_I_IV | ECM", "GSE70362 AF I-IV, ECM", BLUE),
        ("GSE23130_LCM_all | all", "GSE23130 LCM, all genes", RED),
        ("GSE23130_LCM_all | ECM", "GSE23130 LCM, ECM", RED),
    ]
    for i, (key, label, color) in enumerate(rows):
        value = float(rel.loc[rel["key"].eq(key), "median_spearman"].iloc[0])
        _bar(
            draw,
            x=960,
            y=685 + i * 105,
            width=660,
            height=26,
            value=max(value, 0),
            max_value=0.6,
            color=color,
            label=label,
            value_text=f"{value:.2f}",
        )
    _save(image, path)


def draw_msigdb_audit(audit: pd.DataFrame, summary: dict[str, object], path: Path) -> None:
    image, draw = _canvas()
    _text(draw, (70, 40), "Most one-cohort module signals fail the gene-level gate", 39, bold=True)
    _text(
        draw,
        (70, 93),
        "Hallmark, KEGG and Reactome modules with at least 10 genes measured in both cohorts.",
        22,
        fill=MUTED,
    )
    _panel_label(draw, (70, 150), "A")
    _panel_label(draw, (1190, 150), "B")
    left, top, plot_w, plot_h = 120, 210, 970, 760
    draw.rectangle([left, top, left + plot_w, top + plot_h], outline=GRID, width=2)
    for i in range(6):
        y = top + plot_h - int(plot_h * i / 5)
        draw.line([(left, y), (left + plot_w, y)], fill="#EFF2F5", width=1)
        _text(draw, (left - 20, y), f"{i / 5:.1f}", 17, fill=MUTED, anchor="rm")
    for i in range(6):
        x = left + int(plot_w * i / 5)
        draw.line([(x, top), (x, top + plot_h)], fill="#EFF2F5", width=1)
        _text(draw, (x, top + plot_h + 18), f"{i / 5:.1f}", 17, fill=MUTED, anchor="ma")
    _text(draw, (left + plot_w / 2, top + plot_h + 62), "Maximum cohort directional imbalance", 22, fill=INK, anchor="ma")
    _vertical_text(
        image,
        (52, top + plot_h / 2),
        "Gene-level sign concordance",
        22,
    )

    x = np.maximum(
        np.abs(audit["cohort_a_fraction_up"].to_numpy(dtype=float) - 0.5),
        np.abs(audit["cohort_b_fraction_up"].to_numpy(dtype=float) - 0.5),
    )
    y = audit["gene_concordance"].to_numpy(dtype=float)
    categories = np.full(len(audit), 0, dtype=int)
    categories[audit["significant_in_cohort_a"] ^ audit["significant_in_cohort_b"]] = 1
    categories[audit["significant_in_cohort_a"] & audit["significant_in_cohort_b"]] = 2
    categories[audit["gene_level_replicated"]] = 3
    colors = np.array([GRAY, RED, ORANGE, TEAL], dtype=object)
    sizes = np.array([7, 9, 12, 16])
    for category in (0, 1, 2, 3):
        mask = categories == category
        for xi, yi in zip(x[mask], y[mask]):
            px = left + int(plot_w * min(xi / 0.5, 1))
            py = top + plot_h - int(plot_h * min(max(yi, 0), 1))
            radius = int(sizes[category])
            draw.ellipse(
                [px - radius, py - radius, px + radius, py + radius],
                fill=colors[category],
                outline=BG,
                width=1,
            )
    chance_y = top + plot_h - int(plot_h * 0.5)
    draw.line([(left, chance_y), (left + plot_w, chance_y)], fill=INK, width=2)
    _text(draw, (left + plot_w - 8, chance_y - 10), "50%", 18, fill=INK, anchor="rs")

    _text(draw, (1190, 200), "Audit outcome", 26, bold=True)
    counts = [
        ("Modules tested", int(summary["n_modules_tested"]), GRAY),
        ("Significant in one cohort only", int(summary["n_significant_one_sided"]), RED),
        ("Significant in both cohorts", int(summary["n_significant_both"]), ORANGE),
        ("Nominal module + gene gate", int(summary["n_gene_level_replicated"]), BLUE),
        ("Passed FDR gate", int(summary["n_replicated_fdr"]), TEAL),
    ]
    max_count = max(item[1] for item in counts)
    for i, (label, value, color) in enumerate(counts):
        yy = 260 + i * 145
        _text(draw, (1190, yy), label, 23, fill=INK)
        draw.rounded_rectangle([1190, yy + 38, 1700, yy + 76], radius=8, fill="#EDF1F5")
        filled = int(510 * value / max_count)
        if filled:
            draw.rounded_rectangle([1190, yy + 38, 1190 + filled, yy + 76], radius=8, fill=color)
        _text(draw, (1720, yy + 57), str(value), 23, bold=True, anchor="lm")

    legend_y = 1115
    legend = [
        ("Other modules", GRAY),
        ("One-cohort significant", RED),
        ("Both cohorts significant", ORANGE),
        ("Gene-level replicated", TEAL),
    ]
    for i, (label, color) in enumerate(legend):
        x0 = 120 + i * 390
        draw.ellipse([x0, legend_y, x0 + 20, legend_y + 20], fill=color)
        _text(draw, (x0 + 32, legend_y + 10), label, 19, fill=INK, anchor="lm")
    _save(image, path)


def draw_sensitivity(
    donor_summary: pd.DataFrame,
    attenuation: pd.DataFrame,
    path: Path,
) -> None:
    image, draw = _canvas()
    _text(draw, (70, 40), "Sensitivity models do not rescue the discordant ECM direction", 39, bold=True)
    _text(
        draw,
        (70, 93),
        "Donor-level resampling, one-sample-per-donor selection and reliability-attenuation simulation.",
        22,
        fill=MUTED,
    )
    for x, label in ((70, "A"), (930, "B")):
        _panel_label(draw, (x, 145), label)

    _text(draw, (70, 185), "GSE70362 ECM directional fraction", 27, bold=True)
    donor = donor_summary.set_index("mode")
    rows = [
        (
            "One sample per donor",
            "one_sample_per_donor",
            float(donor.loc["one_sample_per_donor", "fraction_up_median"]),
            float(donor.loc["one_sample_per_donor", "fraction_up_lower"]),
            float(donor.loc["one_sample_per_donor", "fraction_up_upper"]),
            BLUE,
        ),
        (
            "Donor cluster bootstrap",
            "cluster_bootstrap",
            float(donor.loc["cluster_bootstrap", "fraction_up_median"]),
            float(donor.loc["cluster_bootstrap", "fraction_up_lower"]),
            float(donor.loc["cluster_bootstrap", "fraction_up_upper"]),
            ORANGE,
        ),
    ]
    for index, (label, _, median, lower, upper, color) in enumerate(rows):
        y = 285 + index * 170
        _text(draw, (70, y), label, 22)
        x0, x1 = 180, 830
        draw.line([(x0, y + 65), (x1, y + 65)], fill=GRID, width=3)
        chance = x0 + int((x1 - x0) * 0.5)
        draw.line([(chance, y + 35), (chance, y + 95)], fill=INK, width=2)
        lo = x0 + int((x1 - x0) * lower)
        hi = x0 + int((x1 - x0) * upper)
        med = x0 + int((x1 - x0) * median)
        draw.line([(lo, y + 65), (hi, y + 65)], fill=color, width=10)
        draw.ellipse([med - 12, y + 53, med + 12, y + 77], fill=color)
        _text(draw, (med, y + 120), f"{100 * median:.1f}%", 20, bold=True, anchor="ma")
    _text(draw, (505, 640), "50% reference", 18, fill=MUTED, anchor="ma")

    _text(draw, (930, 185), "Gene-level concordance", 27, bold=True)
    for index, (label, key, color) in enumerate(
        [
            ("One sample per donor", "one_sample_per_donor", BLUE),
            ("Donor cluster bootstrap", "cluster_bootstrap", ORANGE),
        ]
    ):
        median = float(donor.loc[key, "concordance_median"])
        lower = float(donor.loc[key, "concordance_lower"])
        upper = float(donor.loc[key, "concordance_upper"])
        y = 285 + index * 170
        _text(draw, (930, y), label, 22)
        x0, x1 = 1040, 1690
        draw.line([(x0, y + 65), (x1, y + 65)], fill=GRID, width=3)
        chance = x0 + int((x1 - x0) * 0.5)
        draw.line([(chance, y + 35), (chance, y + 95)], fill=INK, width=2)
        lo = x0 + int((x1 - x0) * lower)
        hi = x0 + int((x1 - x0) * upper)
        med = x0 + int((x1 - x0) * median)
        draw.line([(lo, y + 65), (hi, y + 65)], fill=color, width=10)
        draw.ellipse([med - 12, y + 53, med + 12, y + 77], fill=color)
        _text(draw, (med, y + 120), f"{100 * median:.1f}%", 20, bold=True, anchor="ma")
    _text(draw, (1365, 640), "50% reference", 18, fill=MUTED, anchor="ma")

    _text(draw, (70, 720), "Reliability-attenuation simulation", 27, bold=True)
    left, top, width, height = 150, 790, 850, 280
    draw.rectangle([left, top, left + width, top + height], outline=GRID, width=2)
    for value in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = top + height - int(height * value)
        draw.line([(left, y), (left + width, y)], fill="#EFF2F5", width=1)
        _text(draw, (left - 15, y), f"{100 * value:.0f}%", 16, fill=MUTED, anchor="rm")
    x_vals = attenuation["true_correlation"].to_numpy(dtype=float)
    y_vals = attenuation["mean"].to_numpy(dtype=float)
    points = [
        (
            left + int(width * x_value),
            top + height - int(height * y_value),
        )
        for x_value, y_value in zip(x_vals, y_vals)
    ]
    draw.line(points, fill=TEAL, width=5)
    for point_x, point_y in points:
        draw.ellipse(
            [point_x - 8, point_y - 8, point_x + 8, point_y + 8],
            fill=TEAL,
        )
    observed = float(attenuation["observed_ecm_sign_concordance"].iloc[0])
    observed_y = top + height - int(height * observed)
    draw.line([(left, observed_y), (left + width, observed_y)], fill=RED, width=4)
    _text(draw, (left + width + 20, observed_y), "observed 23.3%", 18, fill=RED, anchor="lm")
    _text(draw, (left + width / 2, top + height + 45), "Latent true correlation", 21, fill=INK, anchor="ma")
    _vertical_text(
        image,
        (52, top + height / 2),
        "Expected concordance",
        21,
    )
    _save(image, path)


def draw_calibration(
    cross_half: pd.DataFrame,
    power: pd.DataFrame,
    weighted: pd.Series,
    path: Path,
) -> None:
    image, draw = _canvas()
    _text(draw, (70, 40), "Controls show that cross-cohort failure is not a broken measurement pipeline", 37, bold=True)
    _text(
        draw,
        (70, 93),
        "Within-cohort halves provide a positive control; simulation quantifies power.",
        22,
        fill=MUTED,
    )
    for x, label in ((70, "A"), (1030, "B")):
        _panel_label(draw, (x, 145), label)

    _text(draw, (70, 185), "ECM gene concordance", 27, bold=True)
    values = [
        (
            "Cross-cohort",
            0.23333333333333334,
            0.23333333333333334,
            0.23333333333333334,
            RED,
        ),
        (
            "GSE70362 cross-half",
            float(cross_half.iloc[0]["concordance_median"]),
            float(cross_half.iloc[0]["concordance_lower"]),
            float(cross_half.iloc[0]["concordance_upper"]),
            BLUE,
        ),
        (
            "GSE23130 cross-half",
            float(cross_half.iloc[1]["concordance_median"]),
            float(cross_half.iloc[1]["concordance_lower"]),
            float(cross_half.iloc[1]["concordance_upper"]),
            TEAL,
        ),
    ]
    for index, (label, med, low, high, color) in enumerate(values):
        y = 270 + index * 150
        _text(draw, (70, y), label, 21)
        x0, x1 = 330, 900
        draw.line([(x0, y + 60), (x1, y + 60)], fill=GRID, width=3)
        chance = x0 + int((x1 - x0) * 0.5)
        draw.line([(chance, y + 30), (chance, y + 90)], fill=INK, width=2)
        lx = x0 + int((x1 - x0) * low)
        hx = x0 + int((x1 - x0) * high)
        mx = x0 + int((x1 - x0) * med)
        draw.line([(lx, y + 60), (hx, y + 60)], fill=color, width=10)
        draw.ellipse([mx - 12, y + 48, mx + 12, y + 72], fill=color)
        _text(draw, (mx, y + 112), f"{100 * med:.1f}%", 20, bold=True, anchor="ma")

    _text(draw, (1030, 185), "Power of nominal 30-gene sign test", 27, bold=True)
    left, top, width, height = 1120, 270, 560, 400
    draw.rectangle([left, top, left + width, top + height], outline=GRID, width=2)
    for value in (0.0, 0.25, 0.5, 0.75, 1.0):
        y = top + height - int(height * value)
        draw.line([(left, y), (left + width, y)], fill="#EFF2F5", width=1)
        _text(draw, (left - 15, y), f"{100 * value:.0f}%", 16, fill=MUTED, anchor="rm")
    for index, row in power.iterrows():
        x = left + int(width * float(row["true_correlation"]))
        y = top + height - int(height * float(row["power_nominal_n"]))
        draw.ellipse([x - 10, y - 10, x + 10, y + 10], fill=BLUE)
        if index:
            previous = power.iloc[index - 1]
            px = left + int(width * float(previous["true_correlation"]))
            py = top + height - int(height * float(previous["power_nominal_n"]))
            draw.line([(px, py), (x, y)], fill=BLUE, width=4)
    _text(
        draw,
        (left + width / 2, top + height + 45),
        "Latent true correlation",
        21,
        fill=INK,
        anchor="ma",
    )
    _text(
        draw,
        (left - 80, top + height / 2),
        "Power",
        21,
        fill=INK,
        anchor="mm",
    )

    _text(draw, (70, 770), "Effect-aware concordance", 27, bold=True)
    weighted_rows = [
        ("Unweighted", float(weighted["unweighted"]), RED),
        ("Effect-size weighted", float(weighted["weighted"]), ORANGE),
        ("Top-half effects", float(weighted["top_half"]), BLUE),
    ]
    for index, (label, value, color) in enumerate(weighted_rows):
        y = 840 + index * 95
        _text(draw, (70, y), label, 21)
        draw.rounded_rectangle([360, y - 2, 1200, y + 28], radius=7, fill="#EDF1F5")
        filled = int(840 * value)
        if filled:
            draw.rounded_rectangle(
                [360, y - 2, 360 + filled, y + 28],
                radius=7,
                fill=color,
            )
        _text(draw, (1230, y + 13), f"{100 * value:.1f}%", 20, bold=True, anchor="lm")
    chance = 360 + int(840 * 0.5)
    draw.line([(chance, 820), (chance, 1110)], fill=INK, width=2)
    _save(image, path)


def draw_pairwise_concordance(pairwise: pd.DataFrame, path: Path) -> None:
    image, draw = _canvas(1800, 1120)
    _text(draw, (70, 40), "Tissue cohort pairs cluster near chance concordance", 39, bold=True)
    _text(
        draw,
        (70, 93),
        "Protein-coding gene symbols shared by each pair; effects centred within cohort.",
        22,
        fill=MUTED,
    )
    data = pairwise.sort_values("gene_concordance").reset_index(drop=True)
    left, top = 520, 175
    plot_w = 1080
    row_h = 52
    for i, row in data.iterrows():
        y = top + i * row_h
        draw.line([(left, y), (left + plot_w, y)], fill="#EDF1F5", width=1)
        value = float(row["gene_concordance"])
        x = left + int(plot_w * (value - 0.2) / 0.6)
        draw.line([(x - 17, y), (x + 17, y)], fill=BLUE, width=4)
        draw.ellipse([x - 10, y - 10, x + 10, y + 10], fill=BLUE)
        _text(
            draw,
            (left - 22, y),
            f"{row['cohort_a']} vs {row['cohort_b']}",
            18,
            fill=INK,
            anchor="rm",
        )
        _text(draw, (left + plot_w + 18, y), f"{100 * value:.1f}%", 18, bold=True, anchor="lm")
    for fraction in (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8):
        x = left + int(plot_w * (fraction - 0.2) / 0.6)
        draw.line([(x, top - 20), (x, top + row_h * len(data) - 5)], fill="#CDD5DF", width=1)
        _text(draw, (x, top - 32), f"{100 * fraction:.0f}%", 18, fill=MUTED, anchor="ma")
    chance_x = left + int(plot_w * (0.5 - 0.2) / 0.6)
    draw.line(
        [(chance_x, top - 42), (chance_x, top + row_h * len(data) + 5)],
        fill=INK,
        width=2,
    )
    _text(
        draw,
        (left + plot_w / 2, top + row_h * len(data) + 60),
        "Gene-level sign concordance",
        23,
        fill=INK,
        anchor="ma",
    )
    _save(image, path)
