from pathlib import Path
from source.pipeline import run_pipeline

data_dir = Path("data")
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

for txt_file in sorted(data_dir.glob("*.txt")):
    print(f"\n=== Processing {txt_file.name} ===")
    text = txt_file.read_text()
    try:
        job = run_pipeline(text)
        out_path = output_dir / f"{txt_file.stem}.json"
        out_path.write_text(job.model_dump_json(indent=2))
        print(f"Saved → {out_path}")
    except RuntimeError as e:
        print(f"❌ {txt_file.name}: {e}")