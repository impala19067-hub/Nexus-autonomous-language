// Production-style example: bounded system health report
fn main() {
    let info = os.system_info();
    let report = {
        "platform": info.platform,
        "cpu_percent": info.cpu_usage_percent,
        "ram_percent": info.ram_percent,
        "disk_free_gb": info.disk_free_gb
    };
    print("Sapphire System Health Monitor");
    print("Platform: {report.platform}");
    print("CPU: {report.cpu_percent}%");
    print("RAM: {report.ram_percent}%");
    print("Disk free: {report.disk_free_gb} GB");
}

main();
