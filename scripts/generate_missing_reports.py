import subprocess
import os
import time

targets = [
    ('postgresql18', 'Dockerfile_postgresql18', 'audit_cis_postgresql_18.py', 'rapport_cis_postgresql_18.html', 'test_pg18', 15, '-e POSTGRES_PASSWORD=rootpass'),
    ('mongodb7', 'Dockerfile_mongodb7', 'audit_cis_mongodb_7.py', 'rapport_cis_mongodb_7.html', 'test_mongo7', 20, ''),
    ('mongodb8', 'Dockerfile_mongodb8', 'audit_cis_mongodb_8.py', 'rapport_cis_mongodb_8.html', 'test_mongo8', 20, ''),
    ('cassandra40', 'Dockerfile_cassandra40', 'audit_cis_cassandra_40.py', 'rapport_cis_cassandra_40.html', 'test_cassandra40', 45, ''),
    ('cassandra41', 'Dockerfile_cassandra41', 'audit_cis_cassandra_41.py', 'rapport_cis_cassandra_41.html', 'test_cassandra41', 45, ''),
    ('cassandra50', 'Dockerfile_cassandra50', 'audit_cis_cassandra_50.py', 'rapport_cis_cassandra_50.html', 'test_cassandra50', 45, ''),
]

for name, df, script, report, tag, wait, extra_args in targets:
    print(f"\n==================================================")
    print(f"Generating report for {name} ({report})...")

    # Build image
    print(f"  Building {df}...")
    subprocess.run(f"docker build -f {df} -t {tag}:report .", shell=True, check=True)

    # Clean previous container
    subprocess.run(f"docker rm -f {tag}_run 2>/dev/null", shell=True)

    # Run container
    print(f"  Starting container {tag}_run...")
    subprocess.run(f"docker run -d {extra_args} --name {tag}_run {tag}:report", shell=True, check=True)

    print(f"  Waiting {wait}s for database initialization...")
    time.sleep(wait)

    # Execute audit script
    print(f"  Running audit script {script}...")
    subprocess.run(f"docker exec {tag}_run python3 /datas/{script}", shell=True)

    # Copy report
    print(f"  Copying report {report}...")
    cp_res = subprocess.run(f"docker cp {tag}_run:/datas/{report} .", shell=True)
    if cp_res.returncode != 0:
        # Fallback if report name differs
        subprocess.run(f"docker exec {tag}_run cat /datas/{report} > {report}", shell=True)

    # Cleanup container
    subprocess.run(f"docker rm -f {tag}_run 2>/dev/null", shell=True)

    if os.path.exists(report):
        size = os.path.getsize(report)
        print(f"  ✅ Report {report} generated successfully ({size} bytes)")
    else:
        print(f"  ❌ Report {report} generation failed")

print("\n🎉 All missing reports processing completed!")
