"""
简单水电解模拟器 (H2O -> H2 + O2)

2 H2O(l) -> 2 H2(g) + O2(g)

使用法拉第定律：
  Q = I * t
  n_e = Q / F

对上述反应：
  4 mol 电子 -> 2 mol H2O 消耗 -> 2 mol H2 + 1 mol O2

=>  n_H2  = n_e / 2
    n_O2  = n_e / 4
    n_H2O = n_e / 2
"""

import math
import numpy as np
try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

FARADAY_CONST = 96485.33212      # C/mol e-
MOLAR_MASS_H2O = 18.01528        # g/mol
R_GAS = 0.082057366080960        # L·atm/(mol·K)


def simulate_electrolysis(
    current_a: float,
    total_time_s: float,
    dt_s: float = 1.0,
    temperature_c: float = 25.0,
    pressure_atm: float = 1.0,
    efficiency: float = 1.0,
):
    """
    模拟恒定电流电解水的过程。

    参数：
        current_a      : 电流 (A)
        total_time_s   : 总电解时间 (s)
        dt_s           : 时间步长 (s)
        temperature_c  : 温度 (°C)
        pressure_atm   : 压强 (atm)
        efficiency     : 电解效率 (0~1)

    返回：
        一个字典，包含时间序列和各物理量的 numpy 数组
    """

    # 时间序列
    t = np.arange(0, total_time_s + dt_s, dt_s)

    # 总电荷 Q = I * t
    Q = current_a * t * efficiency  # C （效率<1时等效减少有效电荷）

    # 电子物质的量 n_e = Q / F
    n_e = Q / FARADAY_CONST  # mol of e-

    # 根据反应式换算气体摩尔数
    n_H2 = n_e / 2.0   # mol
    n_O2 = n_e / 4.0   # mol

    # H2O 消耗摩尔数（与产生 H2 相同，也 = n_e/2）
    n_H2O = n_e / 2.0
    m_H2O_g = n_H2O * MOLAR_MASS_H2O

    # 温度转为 K
    T_K = temperature_c + 273.15

    # 理想气体状态方程：V = nRT / P
    V_H2_L = n_H2 * R_GAS * T_K / pressure_atm
    V_O2_L = n_O2 * R_GAS * T_K / pressure_atm

    return {
        "time_s": t,
        "n_e_mol": n_e,
        "n_H2_mol": n_H2,
        "n_O2_mol": n_O2,
        "n_H2O_mol": n_H2O,
        "m_H2O_g": m_H2O_g,
        "V_H2_L": V_H2_L,
        "V_O2_L": V_O2_L,
    }


def print_final_result(result):
    """打印模拟结束时的关键结果。"""
    t = result["time_s"][-1]

    n_H2 = result["n_H2_mol"][-1]
    n_O2 = result["n_O2_mol"][-1]
    n_H2O = result["n_H2O_mol"][-1]
    m_H2O = result["m_H2O_g"][-1]

    V_H2 = result["V_H2_L"][-1]
    V_O2 = result["V_O2_L"][-1]

    print("===== 电解结束结果 =====")
    print(f"总时间: {t:.1f} s")
    print(f"H2  产生: {n_H2:.6f} mol,  约 {V_H2:.3f} L")
    print(f"O2  产生: {n_O2:.6f} mol,  约 {V_O2:.3f} L")
    print(f"H2O 消耗: {n_H2O:.6f} mol, 约 {m_H2O:.3f} g")
    print("========================")


def plot_result(result):
    """画出 H2 和 O2 体积随时间变化曲线。"""
    t = result["time_s"]
    V_H2 = result["V_H2_L"]
    V_O2 = result["V_O2_L"]

    if plt is None:
        return
    plt.figure()
    plt.plot(t, V_H2, label="H2 体积 (L)")
    plt.plot(t, V_O2, label="O2 体积 (L)")
    plt.xlabel("时间 (s)")
    plt.ylabel("体积 (L)")
    plt.title("水电解产生气体体积随时间的变化")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # 你可以根据需要修改这里的参数来做“实验”
    current_a = 2.0       # 电流 2 A
    total_time_s = 600.0  # 总时间 600 s = 10 分钟
    dt_s = 1.0            # 每 1 秒计算一次
    temperature_c = 25.0  # 室温
    pressure_atm = 1.0    # 标准大气压
    efficiency = 1.0      # 理论上 100% 电解效率

    result = simulate_electrolysis(
        current_a=current_a,
        total_time_s=total_time_s,
        dt_s=dt_s,
        temperature_c=temperature_c,
        pressure_atm=pressure_atm,
        efficiency=efficiency,
    )

    print_final_result(result)
    plot_result(result)