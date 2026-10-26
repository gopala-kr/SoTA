# pipeline.py — the refinery as a batch job (sketch for a datatrove-style
# library; class names follow Hugging Face datatrove's documented blocks,
# but check them against the version you install).
from datatrove.executor import SlurmPipelineExecutor
from datatrove.pipeline.readers import WarcReader
from datatrove.pipeline.extractors import Trafilatura
from datatrove.pipeline.filters import LanguageFilter, GopherQualityFilter, GopherRepetitionFilter, URLFilter
from datatrove.pipeline.writers import JsonlWriter

SlurmPipelineExecutor(
    job_name="refinery-cc-2026-10",
    pipeline=[
        WarcReader("s3://maestro-raw/cc/2026-10/", glob_pattern="*.warc.gz"),
        URLFilter(),                       # blocklists: adult, malware, opted-out domains
        Trafilatura(favour_precision=True),  # HTML -> main text
        LanguageFilter(languages=["en"]),
        GopherRepetitionFilter(),
        GopherQualityFilter(),             # the rules in quality_filter.py
        JsonlWriter("s3://maestro-clean/cc/2026-10/"),
    ],
    tasks=2000, time="12:00:00", partition="exp",   # CPU-heavy: runs on the pre-emptible partition
    logging_dir="s3://maestro-logs/refinery/cc-2026-10/",
).run()
