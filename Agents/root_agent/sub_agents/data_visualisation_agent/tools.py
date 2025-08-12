import matplotlib.pyplot as plt
import os
from typing import List
import pandas as pd
from google.adk.tools import agent_tool

# Ensure the 'charts' directory exists
CHARTS_DIR = os.path.join(os.path.dirname(__file__), 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

def create_bar_chart(
    labels: List[str],
    values: List[float],
    title: str = "Bar Chart",
    x_label: str = "X-axis",
    y_label: str = "Y-axis"
) -> str:
    """
    Creates a bar chart and saves it as a PNG file.

    Args:
        labels: A list of strings for the x-axis labels.
        values: A list of floats for the y-axis values.
        title: The title of the chart.
        x_label: The label for the x-axis.
        y_label: The label for the y-axis.

    Returns:
        The file path of the generated chart image.
    """
    plt.figure()
    plt.bar(labels, values)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    
    file_path = os.path.join(CHARTS_DIR, f"{title.replace(' ', '_')}.png")
    plt.savefig(file_path)
    plt.close()
    
    return f"Chart saved at: {file_path}"

def create_table_chart(
    data: List[List[str]],
    columns: List[str],
    title: str = "Table"
) -> str:
    """
    Creates a table chart and saves it as a PNG file.

    Args:
        data: A list of lists representing the table rows.
        columns: A list of strings for the column headers.
        title: The title of the table.

    Returns:
        The file path of the generated chart image.
    """
    plt.figure(figsize=(8, len(data) * 0.5))
    ax = plt.subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    
    table = ax.table(cellText=data, colLabels=columns, loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)
    
    plt.title(title)
    
    file_path = os.path.join(CHARTS_DIR, f"{title.replace(' ', '_')}.png")
    plt.savefig(file_path, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    
    return f"Table chart saved at: {file_path}"

if __name__ == "__main__":
    # This block of code will only run when you execute this script directly.
    # It will NOT run when the agent imports these functions.
    print("--- Testing visualization tools ---")

    # 1. Test the bar chart tool
    print("\nTesting create_bar_chart...")
    bar_labels = ["Apples", "Bananas", "Oranges"]
    bar_values = [10, 15, 7]
    bar_result = create_bar_chart(
        labels=bar_labels,
        values=bar_values,
        title="Fruit Sales",
        x_label="Fruit",
        y_label="Quantity Sold"
    )
    print(f"Bar chart test complete. {bar_result}")

    # 2. Test the table chart tool
    print("\nTesting create_table_chart...")
    table_columns = ["Product", "Price", "In Stock"]
    table_data = [
        ["Laptop", "$1200", "Yes"],
        ["Mouse", "$25", "Yes"],
        ["Keyboard", "$75", "No"]
    ]
    table_result = create_table_chart(
        data=table_data,
        columns=table_columns,
        title="Inventory"
    )
    print(f"Table chart test complete. {table_result}")

    print("\n\nAll tests finished. Check the 'charts' directory for the output images.")
