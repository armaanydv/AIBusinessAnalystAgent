from app.core.bootstrap import analysis_service


query = (
    "What trends can be observed in revenue "
    "from Q1 2026 to Q3 2026?"
)


result = analysis_service.analyze(query)


print("\n================ ANALYSIS RESULT ================\n")

print("Analysis Type:")
print(result.analysis_type)

print("\nFindings:")
for finding in result.findings:
    print(f"- {finding}")

print("\nConclusions:")
for conclusion in result.conclusions:
    print(f"- {conclusion}")

print("\nSupporting Evidence:")
for evidence in result.supporting_evidence:
    print(f"- {evidence}")

print("\n==================================================")