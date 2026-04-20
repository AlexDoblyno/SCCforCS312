import json
import matplotlib.pyplot as plt
import math


def main():
    # 取消注释你需要跑的文件，注释掉另一个
    filename = "_prepost_runtimes.json"
    #filename = '_scc_runtimes.json'

    with open(filename, "r") as f:
        runtimes = json.load(f)

    # 1. 设置理论时间复杂度 O(V log V + E)
    def theoretical_big_o(v, e):
        if v <= 1:
            return 1  # 防止 math.log2(0) 报错
        return v * math.log2(v) + e

    _, vv, ee, times = zip(*runtimes)

    # 2. 自动计算拟合系数（关键修复！）
    # 通过 实际总时间 / 理论总时间，得到一个极小的系数（约 0.0001 级别）
    # 这样就能把高达十几万的理论值，平滑地缩放回二十几秒的实际区间
    theoretical_times = [theoretical_big_o(v, e) for v, e in zip(vv, ee)]
    coeff = sum(times) / sum(theoretical_times)
    print(f"[{filename}] 计算出的动态拟合系数 (coeff): {coeff:.8f}")

    # 画散点图（实际运行时间）
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(vv, ee, times, marker="o")

    # 应用拟合系数计算每个点的理论高度
    predicted_runtime = [coeff * theoretical_big_o(v, e) for _, v, e, _ in runtimes]

    # 画理论拟合线
    ax.plot(vv, ee, predicted_runtime, c="k", ls=":", lw=2, alpha=0.5)

    # 3. 更新图例、标签和标题
    ax.legend(["Observed", "Theoretical O(V log V + E)"])
    ax.set_xlabel("|V|")
    ax.set_ylabel("|E|")
    ax.set_zlabel("Runtime (sec)")

    # 根据文件名自动调整标题
    title_prefix = "SCC" if "scc" in filename else "Pre/Post"
    ax.set_title(f"Time for {title_prefix} on Graph")

    # 视角设置
    ax.view_init(elev=10, azim=-60)

    fig.show()

    # 4. 自动保存图片，防止相互覆盖
    output_filename = filename.replace('.json', '.svg')
    fig.savefig(output_filename)
    print(f"图表已成功保存为: {output_filename}")


if __name__ == "__main__":
    main()