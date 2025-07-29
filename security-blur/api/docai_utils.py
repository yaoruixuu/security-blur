from google.cloud import documentai_v1 as documentai
from google.cloud.documentai_v1 import types
from google.api_core.client_options import ClientOptions


def process_document_from_gcs(
    project_id: str,
    location: str,
    processor_id: str,
    gcs_input_uri: str,
    mime_type: str = "application/pdf"
):

    # Create a client
    client = documentai.DocumentProcessorServiceClient()

    # The full resource name of the processor
    processor_name = client.processor_path(project_id, location, processor_id)

    # Create a GcsDocument object to specify the input from GCS
    gcs_document = documentai.GcsDocument(gcs_uri=gcs_input_uri, mime_type=mime_type)

    # Configure the process request
    # Use the 'gcs_document' field to pass the GcsDocument object
    request = documentai.ProcessRequest(
        name=processor_name,
        gcs_document=gcs_document, # Pass the documentai.GcsDocument object here
    )

    result = client.process_document(request=request)
    document_object = result.document
    text = document_object.text

    block_info = []

    blocks = []
    for page in document_object.pages:
        for block in page.blocks:
            blocks.append((block.layout.text_anchor.text_segments, block.layout.confidence))

    for block in blocks:
        for seg in block[0]:
            
            start_index = seg.start_index
            end_index = seg.end_index
            txt = text[start_index : end_index ]
       
            label = classify_label(txt)
            block_info.append({"text": txt, "label": label, "confidence": block[1]})

    sanitized_text = ""
    sanitized_block_count = 0
    confidence_sum = 0

    for block in block_info:
        if block["label"] == "(U)":
            sanitized_text += block["text"]
            sanitized_block_count +=1
            confidence_sum += block["confidence"]
    
    return ({"sanitized_text": sanitized_text, "segments_removed": sanitized_block_count, "confidence_avg": confidence_sum/sanitized_block_count})


def classify_label(string):
    for label in ["(U)", "(C)", "(S)", "(TS)"]:
        if label in string:
            return label
    return "UNKNOWN"



