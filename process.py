import os
from processor.processor import Processor

if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_path, "data")
    resource_path = os.path.join(data_path, "resources")
    input_path = os.path.join(data_path, "inputs", "1984.txt")
    output_path = os.path.join(data_path, "outputs")
    processor = Processor(
        resource_path=resource_path,
        config={}
    )
    processor.process(
        input_path=input_path,
        output_path=output_path
        )