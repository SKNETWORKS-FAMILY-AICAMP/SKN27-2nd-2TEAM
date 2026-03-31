import matplotlib.pyplot as plt

# ─────────────────────────────────────────
# Accuracy & Loss 시각화
# ─────────────────────────────────────────
def plot_accuracy_loss(results: dict) -> None:
    """Accuracy & Loss 막대 그래프 시각화"""

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # Accuracy 그래프
    axes[0].bar(['Accuracy'], [results['accuracy']], color='steelblue', width=0.4)
    axes[0].set_ylim(0, 1)
    axes[0].set_title('Accuracy')
    axes[0].set_ylabel('Score')
    for bar in axes[0].patches:
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f"{results['accuracy']*100:.2f}%", ha='center', fontsize=12)

    # Loss 그래프
    axes[1].bar(['Loss'], [results['loss']], color='tomato', width=0.4)
    axes[1].set_ylim(0, 1)
    axes[1].set_title('Loss')
    axes[1].set_ylabel('Score')
    for bar in axes[1].patches:
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                    f"{results['loss']*100:.2f}%", ha='center', fontsize=12)

    plt.suptitle('Model Accuracy & Loss', fontsize=14)
    plt.tight_layout()
    plt.show()