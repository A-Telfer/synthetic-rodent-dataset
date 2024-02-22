from pathlib import Path
import pickle 
import matplotlib.pyplot as plt

project_folder = Path(__file__).parents[3].absolute()
data_folder = project_folder / "data/tests/demo"
print(data_folder)

for i, frame in enumerate(sorted(data_folder.glob("*.png"))):
    with open(data_folder / f"{frame.stem}.pkl", "rb") as f:
        data = pickle.load(f)

    plt.figure(figsize=(10, 5))
    plt.imshow(plt.imread(frame))
    for label, loc in data.items():
        x, y = loc
        print(x, y)
        plt.scatter(x, y, s=10, cmap="viridis", alpha=0.7, label=label)

    plt.legend()
    plt.ylabel(f"Frame {i}")
    plt.xticks([])
    plt.yticks([])

plt.show()