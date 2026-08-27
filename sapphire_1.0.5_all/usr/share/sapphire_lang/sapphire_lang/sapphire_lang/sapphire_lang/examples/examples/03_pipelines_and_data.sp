// 03_pipelines_and_data.sp - Process Piping & Data Automation

fn main() {
    print("ðŸš€ Demonstrating Native Process Piping & Data Transformation...");

    // 1. Process Execution & Filtering
    let files = $ dir /b
                |> lines()
                |> filter(file -> file.contains(".py") or file.contains(".sp"));

    print("Filtered Source Files in Directory:");
    for f in files {
        print("  ðŸ“„ {f}");
    }

    // 2. Data Transformation (JSON & CSV)
    let records = [
        {"task": "Backup DB", "status": "COMPLETED", "duration_sec": 42},
        {"task": "Clear Temp Cache", "status": "COMPLETED", "duration_sec": 12},
        {"task": "Security Scan", "status": "RUNNING", "duration_sec": 120}
    ];

    let json_str = data.to_json(records);
    fs.write("./task_report.json", json_str);
    print("ðŸ’¾ Saved task_report.json to disk.");

    let read_back_json = fs.read("./task_report.json") |> data.parse_json();
    print("Loaded {read_back_json.length} tasks from JSON file.");

    fs.remove("./task_report.json");
    print("ðŸ§¹ Cleanup completed.");
}

main();

