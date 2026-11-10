import numpy as np
from sklearn.datasets import make_moons
from pathlib import Path
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
import matplotlib.pyplot as plt

est = StatevectorEstimator()

def build_U(has_cnot): 
    x = ParameterVector("x", 2)
    th = ParameterVector("z_th", 4)

    qc = QuantumCircuit(2)

    # encoding
    qc.ry(x[0], 0)
    qc.ry(x[1], 1)

    # ansatz, 1 warstwa
    qc.ry(th[0], 0)
    qc.ry(th[1], 1)

    if has_cnot:
        qc.cx(0, 1)

    qc.ry(th[2], 0)
    qc.ry(th[3], 1)

    return qc

def forward(qc, obs, X_data, theta):
    M = len(X_data)
    params_batch = np.hstack([X_data, np.tile(theta, (M, 1))])

    job = est.run([(qc, obs, params_batch)])
    return job.result()[0].data.evs

def loss_and_grad(qc, obs, X_data, Y_data, theta):
    # forward pass 
    f_vals = forward(qc, obs, X_data, theta)
    #                                       ^^ tutaj + 0.25 biasu

    # mse
    loss = np.mean((f_vals - Y_data) ** 2)
    acc = np.mean(np.sign(f_vals) == Y_data)

    # gradient parameter-shift
    grad = np.zeros_like(theta)
    for j in range(len(theta)):
        th_plus = theta.copy()
        th_minus = theta.copy()
        th_plus[j] += np.pi / 2
        th_minus[j] -= np.pi / 2

        f_plus = forward(qc, obs, X_data, th_plus)
        f_minus = forward(qc, obs, X_data, th_minus)

        df_dth = (f_plus - f_minus) / 2.0
        # MSE' = 2*(f - y) * df_dth
        grad[j] = np.mean(2 * (f_vals - Y_data) * df_dth)

    return loss, acc, grad

def train_variant(name, has_cnot, obs, X_data, Y_data, epochs=60, lr=0.25):
    qc = build_U(has_cnot)

    rand = np.random.default_rng(42)
    theta = rand.uniform(-1.8, 1.8, 4)

    losses, accs = [], []
    for epoch in range(epochs):
        loss, acc, grad = loss_and_grad(qc, obs, X_data, Y_data, theta)
        losses.append(loss)
        accs.append(acc)
        theta -= lr * grad

    print(f"{name:25s} | Final Loss: {losses[-1]:.4f} | Final Acc: {accs[-1]*100:.1f}%")

    return {"qc": qc, "obs": obs, "theta": theta, "losses": losses, "accs": accs}


def main():
    # obserwable
    Z0 = SparsePauliOp.from_sparse_list([("Z", [0], 1.0)], num_qubits=2)
    Z0Z1 = SparsePauliOp.from_sparse_list([("ZZ", [0,1], 1.0)], num_qubits=2)
        
    
    X_raw, y_raw = make_moons(n_samples=100, noise=0.1, random_state=42)
    X = (X_raw - X_raw.min(axis = 0)) / (X_raw.max(axis = 0) - X_raw.min(axis = 0)) * np.pi
    Y = 2 * y_raw - 1

    variants = [
        ("1: Z_0 i CNOT", True, Z0),
        ("2: Z_0 bez CNOT", False, Z0),
        ("3: Z_0Z_1 i CNOT", True, Z0Z1),
        ("4: Z_0Z_1 bez CNOT", False, Z0Z1),
    ]

    results = {}

    for name, has_cnot, obs in variants:
        results[name] = train_variant(name, has_cnot, obs, X, Y)

    plot_results(results, X, Y)

def plot_results(results, X, Y):
    out_dir = Path(__file__).resolve().parent

    # loss i acc
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))

    for name, res in results.items():
        ax1.plot(res["losses"], label=name, linewidth=2)
        ax2.plot([a * 100 for a in res["accs"]], label=name, linewidth=2)

    ax1.set_title("MSE")
    ax1.set_xlabel("epoka")
    ax1.set_ylabel("loss")
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    ax2.set_title("Accuracy")
    ax2.set_xlabel("epoka")
    ax2.set_ylabel("accuracy %")
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(out_dir / "mse_and_acc.png", dpi=150)
    plt.close()

    # granice decyzyjne
    xx, yy = np.meshgrid(np.linspace(0, np.pi, 40), np.linspace(0, np.pi, 40))
    grid = np.c_[xx.ravel(), yy.ravel()]

    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    for ax, (name, res) in zip(axes.ravel(), results.items()):
        preds = forward(res["qc"], res["obs"], grid, res["theta"]).reshape(xx.shape)

        ax.contourf(xx, yy, preds, levels=np.linspace(-1, 1, 21), cmap="coolwarm", alpha=0.6)
        ax.contour(xx, yy, preds, levels=[0], colors="black", linewidths=2)
        #                bias  ^^ + 0.25 
        ax.scatter(X[:, 0], X[:, 1], c=Y, cmap="coolwarm", edgecolors="k", s=35)

        acc_end = res["accs"][-1] * 100
        loss_end = res["losses"][-1]
        ax.set_title(f"{name}\nAcc: {acc_end:.1f}% | Loss: {loss_end:.3f}")
        ax.set_xlabel("x1 [0, π]")
        ax.set_ylabel("x2 [0, π]")

    plt.tight_layout()
    plt.savefig(out_dir / "decision_boundaries.png", dpi=150)
    plt.close()

if __name__ == '__main__':
    main()



