from app.core.bootstrap import analysis_service


query = "What are the strengths, weaknesses, opportunities, and threats for Acme Retail Solutions based on its Q1 to Q3 2026 performance?"


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