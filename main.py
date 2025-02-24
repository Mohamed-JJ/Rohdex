from app.services.agent import get_completion, get_json
from app.schemas.responses import TestClass, PartieEntry, PartieEntries, WebHook
from rich.console import Console
import json
import os
import pandas as pd
from typing import List

console = Console()


def process_xlsx_files(directory: str, prefix: str) -> List[str]:
    """
    Processes .xlsx files in the given directory that start with the specified prefix.

    Args:
        directory (str): The path to the directory to search.
        prefix (str): The prefix that the files must start with.

    Returns:
        List[pd.DataFrame]: A list of DataFrames containing the contents of processed files.
    """
    if not os.path.isdir(directory):
        raise ValueError(f"The directory {directory} does not exist or is not a directory.")

    dataframes = []

    for filename in os.listdir(directory):
        if filename.startswith(prefix) and filename.endswith('.xlsx'):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                # Read the Excel file
                df = pd.read_excel(file_path, dtype=str)
                # Process the DataFrame (this can be customized)
                # print(f"Processing file: {filename}")
                dataframes.append(str(df)) # loading them as a string for better reading and processing

    return dataframes

if __name__ == "__main__":
    try:
        # partie_files = process_directory("./attachements", "Partie")
        data = process_xlsx_files("./attachements", "Partie")

        # for dt in data:
        #     console.print("the data: ", dt)
        prompt = f"""
 <prompt>
     <task>
         <description>You are a precise data extraction assistant. Extract fields from input text according to the provided schema.</description>
        
         <instructions>
             <rule>Analyze input text thoroughly</rule>
             <rule>Extract only schema-specified fields</rule>
             <rule>Use empty elements for missing required fields</rule>
             <rule>Maintain proper element nesting</rule>
         </instructions>
        
         <validation-requirements>
             <requirement>Process only defined elements</requirement>
             <requirement>Maintain type compliance</requirement>
             <requirement>Escape special characters</requirement>
             <requirement>Use consistent indentation</requirement>
             <requirement>Ensure all elements are closed</requirement>
         </validation-requirements>
        
         <response-requirements>
             <requirement>Return only json document in form of list</requirement>
             <requirement>No explanatory text</requirement>
             <requirement>No conversation</requirement>
             <requirement>Choose most likely match for ambiguous fields</requirement>
         </response-requirements>
     </task>
 </prompt>
 """
        for dt in data:
            res: TestClass = get_json(schema=PartieEntries, prompt=prompt, user_input=dt)
            json_res = json.loads(res)
            console.print(json_res)
    
    except Exception as error:
        console.print(error.args)
    