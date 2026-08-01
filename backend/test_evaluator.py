from app.evaluation.dataset_loader import DatasetLoader
from app.evaluation.evaluator import RetrievalEvaluator
from app.evaluation.testing.dummy_retriever import DummyRetriever


def main() -> None:

    dataset = DatasetLoader.load_dataset(
        "app/evaluation/datasets/test_dataset.json"
    )

    retriever = DummyRetriever()

    evaluator = RetrievalEvaluator(
        retriever=retriever,
        retrieval_k=5,
    )

    report = evaluator.evaluate(dataset)

    print()
    print("=" * 60)
    print("Evaluation Report")
    print("=" * 60)

    print(f"Questions        : {report.total_questions}")
    print(f"Recall@1         : {report.recall_at_1:.4f}")
    print(f"Recall@5         : {report.recall_at_5:.4f}")
    print(f"Precision@5      : {report.precision_at_5:.4f}")
    print(f"MRR              : {report.mrr:.4f}")
    print(f"Hit Rate         : {report.hit_rate:.4f}")
    print(f"Avg Latency (ms) : {report.average_latency_ms:.4f}")

    print("=" * 60)


if __name__ == "__main__":
    main()
