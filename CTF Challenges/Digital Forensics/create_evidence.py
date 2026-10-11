from PIL import Image
from PIL.PngImagePlugin import PngInfo

# Create a simple evidence image
img = Image.new("RGB", (900, 500), "white")

# Add forensic metadata
metadata = PngInfo()
metadata.add_text("Case", "DF-2026-017")
metadata.add_text("Evidence", "Recovered from compromised workstation")
metadata.add_text("Investigator", "Unknown")
metadata.add_text("Comment", "Inspect the file carefully")

# Save the PNG
img.save(
    "evidence.png",
    pnginfo=metadata
)

# Append hidden forensic evidence
with open("evidence.png", "ab") as f:
    f.write(
        b"\n\nFORENSIC_NOTE:\n"
        b"The missing evidence was hidden here.\n"
        b"TECH{missing_evidence}\n"
    )

print("evidence.png created successfully!")