# import libraries
from concurrent.futures import process
import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()
# set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal
endpoint = os.environ.get('ENDPOINT')
key = os.environ.get('KEY')

def format_bounding_box(bounding_box):
    if not bounding_box:
        return "N/A"
    return ", ".join(["[{}, {}]".format(p.x, p.y) for p in bounding_box])

def analyze_layout():
    # sample form document
    formUrl = "https://filestorage4321.blob.core.windows.net/source/lord_nelson_place(single).pdf"
    # create your `DocumentAnalysisClient` instance and `AzureKeyCredential` variable
    document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    poller = document_analysis_client.begin_analyze_document_from_url(
            "prebuilt-layout", formUrl)
    result = poller.result()

    for idx, style in enumerate(result.styles):
        print(
            "Document contains {} content".format(
                "handwritten" if style.is_handwritten else "no handwritten"
            )
        )

    for page in result.pages:
        for line_idx, line in enumerate(page.lines):
            print(
            "...Line # {} has text content '{}'".format(
            line_idx,
            line.content.encode("utf-8")
            )
        )

        for selection_mark in page.selection_marks:
            print(
            "...Selection mark is '{}' and has a confidence of {}".format(
            selection_mark.state,
            selection_mark.confidence
            )
        )

    for table_idx, table in enumerate(result.tables):
        print(
            "Table # {} has {} rows and {} columns".format(
            table_idx, table.row_count, table.column_count
            )
        )
            
        for cell in table.cells:
            print(
                "...Cell[{}][{}] has content '{}'".format(
                cell.row_index,
                cell.column_index,
                cell.content.encode("utf-8"),
                )
            )

    print("----------------------------------------")


if __name__ == "__main__":
    analyze_layout()