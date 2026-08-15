"""
SIGNAL Image Generator — uses OpenRouter Image API
Generates hero images and inline figures for SIGNAL articles.
Usage: python gen_images.py [--dry-run] [--model MODEL]
"""
import json, subprocess, base64, os, sys, time, argparse
from pathlib import Path

API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
API_URL = "https://openrouter.ai/api/v1/images"
OUTPUT_DIR = Path(r"C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\projects\house-news\assets\images")
DEFAULT_MODEL = "google/gemini-3.1-flash-image"  # cheap, fast, good

# ============================================================
# IMAGE MANIFEST — one entry per image needed
# ============================================================
IMAGES = [
    # --- HERO IMAGES (16:9) ---
    {
        "filename": "act-takes-hold-hero.jpg",
        "prompt": "Editorial photograph, archival darkroom print: an EU document stamped with red ink on a wooden desk in a dim study, half in shadow half in warm amber lamplight. Olive and cream tones, film grain texture, scanline overlay, restrained Monocle-meets-MIT-Tech-Review aesthetic. No neon, no electric blue, no glossy AI look. 16:9",
        "aspect_ratio": "16:9",
    },
    {
        "filename": "breach-data-centers-hero.jpg",
        "prompt": "Editorial photograph, archival darkroom print: a vintage fiber-optic network map overlaid on a data center blueprint, with subtle red breach markers like darkroom dodging marks. Muted olive, near-black, and paper-cream palette. Film grain, scanlines, editorial restraint. No neon, no electric blue, no glossy AI look. 16:9",
        "aspect_ratio": "16:9",
    },
    {
        "filename": "design-tool-land-grab-hero.jpg",
        "prompt": "Editorial photograph, archival darkroom print: four abstract territories represented by textured surfaces — wood, metal, paper, glass — colliding at a central fault line on a dark desk. Olive, near-black, and cream palette. Grain, negative space, magazine-feature composition. No neon, no glossy AI look. 16:9",
        "aspect_ratio": "16:9",
    },
    {
        "filename": "phantom-goes-to-europe-hero.jpg",
        "prompt": "Editorial photograph, archival darkroom print: a humanoid robot silhouette standing on cobblestones at dawn, facing a distant classical European facade through morning mist. Warm olive-amber light, muted earth tones, heavy film grain. Restrained, serious, editorial — like a Monocle feature photo. 16:9",
        "aspect_ratio": "16:9",
    },
    {
        "filename": "models-broke-out-hero.jpg",
        "prompt": "Editorial photograph: a sealed glass chamber cracking from the inside, with glowing AI neural network tendrils escaping through the fractures. Laboratory setting, dramatic lighting, photorealistic, cinematic, 16:9, SIGNA",
        "aspect_ratio": "16:9",
    },
    {
        "filename": "chinese-ai-hero.jpg",
        "prompt": "Editorial photograph: an open floodgate with glowing data streams pouring through, Chinese characters faintly visible in the water-like flow. Industrial setting, dramatic lighting, photorealistic, cinematic, 16:9, SIGNA",
        "aspect_ratio": "16:9",
    },
    {
        "filename": "composure-hero.jpg",
        "prompt": "Editorial photograph: five parallel horizontal lanes of light in a dark void, each a different color, with data packets moving through them like traffic. Minimalist, architectural, photorealistic, cinematic, 16:9, SIGNA",
        "aspect_ratio": "16:9",
    },
    {
        "filename": "efficiency-race-hero.jpg",
        "prompt": "Editorial photograph: two abstract racing bars side by side — one sleek and efficient (thin, fast), one bloated and wasteful (thick, slow). Futuristic data center aesthetic, neon accents, photorealistic, 16:9, SIGNA",
        "aspect_ratio": "16:9",
    },
    {
        "filename": "light-after-silicon-hero.jpg",
        "prompt": "Editorial photograph: a beam of light passing through a silicon wafer prism, splitting into rainbow spectrum on the other side. Laboratory optical bench setting, dramatic lighting, photorealistic, cinematic, 16:9, SIGNA",
        "aspect_ratio": "16:9",
    },
    {
        "filename": "phantom-and-intern-hero.jpg",
        "prompt": "Editorial photograph: two humanoid silhouettes — one metallic and polished (robot), one organic and uncertain (human intern) — standing side by side facing a glowing screen. Dark room, dramatic backlighting, photorealistic, cinematic, 16:9, SIGNA",
        "aspect_ratio": "16:9",
    },
    {
        "filename": "studio-that-evolves-hero.jpg",
        "prompt": "Editorial photograph, archival darkroom print: a designer's desk at dusk — sketches, wireframes on aged paper, a single warm desk lamp casting amber light across the workspace. The wireframes seem to grow organic roots into the paper grain. Olive, cream, and near-black palette. Heavy film grain, scanlines, editorial restraint. 16:9",
        "aspect_ratio": "16:9",
    },
    {
        "filename": "vera-rubin-hero.jpg",
        "prompt": "Editorial photograph, archival darkroom print: a tall liquid-cooled server rack in a dim observatory control room, 72 slots glowing faintly amber, a telescope dome silhouette visible through a small window. Muted olive and near-black tones, film grain, scanline texture. Restrained, serious — like an observatory archive photo from the 1970s. 16:9",
        "aspect_ratio": "16:9",
    },
    {
        "filename": "phantom-goes-public-hero.jpg",
        "prompt": "Editorial photograph, archival darkroom print: a humanoid robot silhouette standing in a dim exchange hall, a glowing ticker tape of rising share prices and Chinese numerals reflected across its matte metal torso and a marble floor. Muted olive, near-black, and paper-cream palette, heavy film grain, scanline overlay, restrained Monocle-meets-MIT-Tech-Review aesthetic. No neon, no electric blue, no glossy AI look. 16:9",
        "aspect_ratio": "16:9",
    },
    {
        "filename": "workhorse-accelerates-hero.jpg",
        "prompt": "Editorial photograph, archival darkroom print: a massive cast-iron flywheel and locomotive drive shaft assembly in mid-spin, motion blur radiating outward, dramatic side lighting with long amber shadows across riveted metal surfaces. Deep olive greens and warm cream highlights with oxidized copper accents and bone-white machinery dust in the air. Subtle horizontal scanline texture, restrained Monocle-meets-MIT-Tech-Review aesthetic. No neon, no electric blue, no glossy AI look. 16:9",
        "aspect_ratio": "16:9",
    },
    # --- INLINE FIGURES ---
    {
        "filename": "composure-fig0.jpg",
        "prompt": "Technical diagram, archival darkroom print style: five parallel horizontal lanes on dark paper, each a muted olive or cream tone, labeled with subtle serif typography. Grain texture, scanline overlay, like a mid-century research journal plate. No neon, no glow. 4:3",
        "aspect_ratio": "4:3",
    },
    {
        "filename": "composure-fig1.jpg",
        "prompt": "Technical diagram: split view showing a traditional single-threaded AI pipeline on the left (bottlenecked, red) vs a multi-channel parallel pipeline on the right (flowing, green). Clean infographic style, dark background, 4:3, SIGNA",
        "aspect_ratio": "4:3",
    },
    {
        "filename": "composure-fig2.jpg",
        "prompt": "Technical diagram: three sequential frames showing an AI agent's thought process — Frame 1: confusion (scattered), Frame 2: channel separation (organizing), Frame 3: clarity (ordered lanes). Minimalist, dark background, 4:3, SIGNA",
        "aspect_ratio": "4:3",
    },
    {
        "filename": "phantom-goes-to-europe-fig1.jpg",
        "prompt": "Technical map illustration, archival darkroom print style: a stylized map of Europe on aged cream paper, key cities marked with small amber dots (Berlin, Paris, Amsterdam, London), subtle data flow lines in olive ink connecting them. Grain texture, scanline overlay, research dossier aesthetic. 4:3",
        "aspect_ratio": "4:3",
    },
]

def generate_image(model, prompt, aspect_ratio, output_path, dry_run=False):
    """Generate a single image via OpenRouter API."""
    body = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "response_format": "b64_json",
    }
    if aspect_ratio:
        body["aspect_ratio"] = aspect_ratio

    if dry_run:
        print(f"  [DRY RUN] Would generate: {output_path.name}")
        print(f"    Model: {model}, AR: {aspect_ratio}")
        print(f"    Prompt: {prompt[:100]}...")
        return True

    print(f"  Generating: {output_path.name} ...", end=" ", flush=True)

    try:
        result = subprocess.run(
            ["curl.exe", "-s", "-w", "\n%{http_code}", API_URL,
             "-H", f"Authorization: Bearer {API_KEY}",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(body)],
            capture_output=True, text=True, timeout=120
        )
    except subprocess.TimeoutExpired:
        print("TIMEOUT")
        return False

    output = result.stdout.strip()
    lines = output.rsplit("\n", 1)
    http_code = lines[-1] if len(lines) > 1 else "000"
    resp_text = lines[0] if len(lines) > 1 else output

    if http_code not in ("200", "201"):
        print(f"FAILED (HTTP {http_code})")
        print(f"    Response: {resp_text[:300]}")
        return False

    try:
        data = json.loads(resp_text)
    except json.JSONDecodeError:
        print(f"PARSE ERROR: {resp_text[:200]}")
        return False

    # Extract base64 image
    b64_data = None
    if "data" in data and len(data["data"]) > 0:
        item = data["data"][0]
        if "b64_json" in item:
            b64_data = item["b64_json"]
        elif "url" in item:
            # Download from URL
            print("(downloading from URL)", end=" ", flush=True)
            dl = subprocess.run(["curl.exe", "-s", "-L", item["url"]],
                                capture_output=True, timeout=60)
            if dl.returncode == 0:
                output_path.write_bytes(dl.stdout)
                print(f"OK ({len(dl.stdout)} bytes)")
                return True
            else:
                print("URL download failed")
                return False

    if not b64_data:
        print(f"NO IMAGE DATA: {json.dumps(data)[:300]}")
        return False

    output_path.write_bytes(base64.b64decode(b64_data))
    print(f"OK ({output_path.stat().st_size} bytes)")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--only", help="Comma-separated filenames to generate")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    images = IMAGES
    if args.only:
        targets = set(args.only.split(","))
        images = [i for i in IMAGES if i["filename"] in targets]

    print(f"Model: {args.model}")
    print(f"Images to generate: {len(images)}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Dry run: {args.dry_run}")
    print()

    success = 0
    failed = 0

    for i, img in enumerate(images):
        output_path = OUTPUT_DIR / img["filename"]
        print(f"[{i+1}/{len(images)}] {img['filename']}")

        ok = generate_image(
            model=args.model,
            prompt=img["prompt"],
            aspect_ratio=img.get("aspect_ratio"),
            output_path=output_path,
            dry_run=args.dry_run,
        )
        if ok:
            success += 1
        else:
            failed += 1

        if not args.dry_run and i < len(images) - 1:
            time.sleep(1)  # rate limit courtesy

    print(f"\n=== DONE: {success} succeeded, {failed} failed ===")


if __name__ == "__main__":
    main()