import os
import shlex
import subprocess
import time

targets = [
    ('postgresql18', 'docker/Dockerfile_postgresql18', 'audit_cis_postgresql_18.py', 'rapport_cis_postgresql_18.html', 'test_pg18', 15, ['-e', 'POSTGRES_PASSWORD=rootpass']),
    ('mongodb7', 'docker/Dockerfile_mongodb7', 'audit_cis_mongodb_7.py', 'rapport_cis_mongodb_7.html', 'test_mongo7', 20, []),
    ('mongodb8', 'docker/Dockerfile_mongodb8', 'audit_cis_mongodb_8.py', 'rapport_cis_mongodb_8.html', 'test_mongo8', 20, []),
    ('cassandra40', 'docker/Dockerfile_cassandra40', 'audit_cis_cassandra_40.py', 'rapport_cis_cassandra_40.html', 'test_cassandra40', 45, []),
    ('cassandra41', 'docker/Dockerfile_cassandra41', 'audit_cis_cassandra_41.py', 'rapport_cis_cassandra_41.html', 'test_cassandra41', 45, []),
    ('cassandra50', 'docker/Dockerfile_cassandra50', 'audit_cis_cassandra_50.py', 'rapport_cis_cassandra_50.html', 'test_cassandra50', 45, []),
]

for name, df, script, report, tag, wait, extra_args in targets:
    print(f"\n==================================================")
    print(f"Generating report for {name} ({report})...")

    # Build image
    print(f"  Building {df}...")
    subprocess.run(["docker", "build", "-f", df, "-t", f"{tag}:report", "."], check=True)

    # Clean previous container
    subprocess.run(["docker", "rm", "-f", f"{tag}_run"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Run container
    print(f"  Starting container {tag}_run...")
    run_cmd = ["docker", "run", "-d"] + extra_args + ["--name", f"{tag}_run", f"{tag}:report"]
    subprocess.run(run_cmd, check=True)

    print(f"  Waiting {wait}s for database initialization...")
    time.sleep(wait)

    # Execute audit script
    print(f"  Running audit script {script}...")
    subprocess.run(["docker", "exec", f"{tag}_run", "python3", f"/datas/{script}"])

    # Copy report
    report_dest = os.path.join("reports", report)
    print(f"  Copying report {report} to {report_dest}...")
    cp_res = subprocess.run(["docker", "cp", f"{tag}_run:/datas/{report}", report_dest])
    if cp_res.returncode != 0:
        # Fallback using stdout
        with open(report_dest, "w", encoding="utf-8") as rf:
            subprocess.run(["docker", "exec", f"{tag}_run", "cat", f"/datas/{report}"], stdout=rf)

    # Cleanup container
    subprocess.run(["docker", "rm", "-f", f"{tag}_run"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if os.path.exists(report_dest):
        size = os.path.getsize(report_dest)
        print(f"  ✅ Report {report_dest} generated successfully ({size} bytes)")
    else:
        print(f"  ❌ Report {report_dest} generation failed")

print("\n🎉 All missing reports processing completed!")
