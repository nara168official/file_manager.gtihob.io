from pathlib import Path

# Use the same path logic as in your app
upload_folder = Path.home() / "Documents" / "file_uploads"
print(f"Files will be saved to: {upload_folder}")