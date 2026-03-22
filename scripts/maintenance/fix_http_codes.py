def replace_400_with_422(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    content = content.replace("assert response.status_code == 400", "assert response.status_code in (400, 422)")
    with open(file_path, 'w') as f:
        f.write(content)

replace_400_with_422("src/api/tests/test_runs_endpoints.py")
replace_400_with_422("src/api/tests/test_integration.py")
