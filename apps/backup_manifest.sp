// Production-style example: deterministic backup manifest
let files = fs.list_dir(".");
let manifest = {
    "generated_by": "Sapphire",
    "file_count": files.length,
    "files": files
};
fs.write("backup_manifest.json", data.to_json(manifest));
print("Backup manifest written: backup_manifest.json");
