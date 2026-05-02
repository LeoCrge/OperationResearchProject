import pandas as pd
import matplotlib.pyplot as plt


def plot_complexity_study():
    print("Loading data from complexity_results.csv...")
    try:
        df = pd.read_csv('complexity_results1-400.csv')
    except FileNotFoundError:
        print("Error: 'complexity_results.csv' not found. Run your benchmark first!")
        return

    worst_cases = df.groupby('Matrix_Size_N').max().reset_index()

    plt.figure(figsize=(10, 6))


    plt.scatter(df['Matrix_Size_N'], df['NW_Time_Seconds'],
                alpha=0.3, color='blue', label='North-West (All Trials)', s=15)
    plt.scatter(df['Matrix_Size_N'], df['BH_Time_Seconds'],
                alpha=0.3, color='green', label='Balas-Hammer (All Trials)', s=15)

    plt.plot(worst_cases['Matrix_Size_N'], worst_cases['NW_Time_Seconds'],
             color='darkblue', marker='o', linewidth=2, label='NW Worst-Case Envelope')
    plt.plot(worst_cases['Matrix_Size_N'], worst_cases['BH_Time_Seconds'],
             color='darkgreen', marker='s', linewidth=2, label='BH Worst-Case Envelope')


    plt.xscale('log')
    plt.yscale('log')

    plt.title('Algorithm Complexity: North-West vs Balas-Hammer')
    plt.xlabel('Matrix Size (n) - Log Scale')
    plt.ylabel('Execution Time (seconds) - Log Scale')

    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()

    plt.savefig('complexity_plot.png', dpi=300, bbox_inches='tight')
    print("Plot saved as 'complexity_plot.png'.")
    plt.show()


if __name__ == "__main__":
    plot_complexity_study()