from app.core.bootstrap import analysis_service


query = (
    "Compare revenue for the North region "
    "in the last quarter with the previous quarter."
)

result = analysis_service.analyze(query)

print("\n================ ANALYSIS RESULT ================\n")

print("Analysis Type:")
print(result.analysis_type)

print("\nFindings:")
for finding in result.findings:
    print("-", finding)

print("\nConclusions:")
for conclusion in result.conclusions:
    print("-", conclusion)

print("\nSupporting Evidence:")
for evidence in result.supporting_evidence:
    print("-", evidence)

print("\n==================================================\n")