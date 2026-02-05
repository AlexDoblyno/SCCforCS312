import json
import matplotlib.pyplot as plt


def compute_coefficient(observed_performance, theoretical_order):
    return [time / theoretical_order(v, e) for _, v, e, time in observed_performance]


def main():

    # COMMENT AND UNCOMMENT appropriate lines as necessary

    filename = "_prepost_runtimes.json"
    # filename = '_scc_runtimes.json'

    with open(filename, "r") as f:
        runtimes = json.load(f)

    def theoretical_big_o(v, e):
        # FILL THIS IN with your theoretical time complexity
        return 1

    coeffs = compute_coefficient(runtimes, theoretical_big_o)

    # slice this list to use a subset for your estimate
    used_coeffs = coeffs[0:]

    coeff = sum(used_coeffs) / len(used_coeffs)
    print(coeff)

    plt.bar(range(len(coeffs)), coeffs)
    xlim = plt.xlim()
    plt.plot(xlim, [coeff, coeff], ls=":", c="k")
    plt.xlim(xlim)
    plt.title(f"coeff={coeff}")
    plt.show()


if __name__ == "__main__":
    main()
